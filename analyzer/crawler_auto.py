# -*- coding: utf-8 -*-
"""
국내 주요 언론 자동 뉴스 본문 수집기 (v7.0)
 - JTBC: Selenium(headless)로 렌더링된 DOM에서 본문 추출
 - 조선/한겨레/KBS/MBC: JSON 또는 HTML 파싱 방식 사용
 - 광고, iframe, script 제거
"""

import re
import requests
from bs4 import BeautifulSoup

USE_SELENIUM_FOR_JTBC = True
JTBC_WAIT_SELECTOR = "#ijam_content"
JTBC_WAIT_TIMEOUT = 18

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}

# 조선일보
def get_chosun_text(url: str) -> str:
    try:
        m = re.search(r"chosun\.com/(.+?)/(\d{4})/(\d{2})/([A-Z0-9]+)/", url)
        if m:
            section, year, month, article_id = m.groups()
            json_url = (
                f"https://www.chosun.com/__data/fusion/cached/page/article/"
                f"{section}/{year}/{month}/{article_id}.json"
            )
            r = requests.get(json_url, timeout=10)
            r.raise_for_status()
            data = r.json()
            body_html = (
                data.get("props", {})
                    .get("pageProps", {})
                    .get("article", {})
                    .get("body", "")
            )
            if body_html:
                soup = BeautifulSoup(body_html, "html.parser")
                text = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))
                if len(text) > 200:
                    return clean_text(text)
    except Exception:
        pass

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        article = soup.select_one("div.article-body, section.article-body, div[data-fusion-container]")
        if article:
            text = " ".join(p.get_text(strip=True) for p in article.find_all("p"))
            return clean_text(text)
    except Exception:
        pass

    return ""

# JTBC (Selenium)
def get_jtbc_text_selenium(url: str) -> str:
    try:
        import time
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager

        chrome_opts = Options()
        chrome_opts.add_argument("--headless=new")
        chrome_opts.add_argument("--disable-gpu")
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--log-level=3")
        chrome_opts.add_argument("--window-size=1280,2000")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ijam_content"))
        )
        time.sleep(1.5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        article = soup.select_one("#ijam_content") or soup.select_one("#article_content, .article_content, article")
        if not article:
            driver.quit()
            return "__ERROR__: 본문 div를 찾지 못했습니다."

        for tag in article.select("script, iframe, figure, div.ad_area, .set_contents_image_ad, .set_contents_video_ad"):
            tag.decompose()

        texts = []
        for tag in article.find_all(["p", "span", "b"]):
            t = tag.get_text(strip=True)
            if t and not t.lower().startswith("advertisement"):
                texts.append(t)

        text = re.sub(r"\s+", " ", " ".join(texts)).strip()
        driver.quit()

        if len(text) < 100:
            return "__ERROR__: 본문 추출 실패 (짧음)"
        return text

    except Exception as e:
        try:
            driver.quit()
        except Exception:
            pass
        return f"__ERROR__: {e}"

# JTBC (Requests)
def get_jtbc_text_requests(url: str) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        article = soup.select_one("#ijam_content, #article_content, #article_content_area, .article_content")
        if not article:
            article = soup.find("div", id=lambda x: x and "jam_content" in x)
        if not article:
            return ""

        for tag in article.select("script, iframe, figure, div.ad_area, .set_contents_image_ad, .set_contents_video_ad"):
            tag.decompose()

        texts = []
        for tag in article.find_all(["p", "span", "b"]):
            t = tag.get_text(strip=True)
            if t and not t.lower().startswith("advertisement"):
                texts.append(t)

        return clean_text(" ".join(texts))
    except Exception:
        return ""

def get_jtbc_text(url: str) -> str:
    if "/article/nb" in url:
        url = url.replace("/article/nb", "/article/NB")
    if USE_SELENIUM_FOR_JTBC:
        text = get_jtbc_text_selenium(url)
        if len(text) >= 180:
            return text
        return get_jtbc_text_requests(url)
    else:
        return get_jtbc_text_requests(url)

# 한겨레
def get_hani_text(url: str) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        article = soup.select_one("div.article-text, div.text, #article-text")
        if article:
            text = " ".join(p.get_text(strip=True) for p in article.find_all("p"))
            return clean_text(text)
    except Exception:
        pass
    return ""

# KBS
def get_kbs_text(url: str) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        article = soup.select_one("div.detail-body, div.detail_body, .view_cont")
        if article:
            text = " ".join(p.get_text(strip=True) for p in article.find_all("p"))
            return clean_text(text)
    except Exception:
        pass
    return ""

# MBC
def get_mbc_text(url: str) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        article = soup.select_one("div.news_cont, div.news_body, div#content")
        if article:
            text = " ".join(p.get_text(strip=True) for p in article.find_all("p"))
            return clean_text(text)
    except Exception:
        pass
    return ""

# 통합 진입점
def get_article_text(url: str) -> str:
    url_l = url.strip().lower()
    if "chosun.com" in url_l:
        text = get_chosun_text(url)
    elif "jtbc.co.kr" in url_l:
        text = get_jtbc_text(url)
    elif "hani.co.kr" in url_l:
        text = get_hani_text(url)
    elif "kbs.co.kr" in url_l:
        text = get_kbs_text(url)
    elif "mbc.co.kr" in url_l:
        text = get_mbc_text(url)
    else:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            text = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))
            text = clean_text(text)
        except Exception:
            text = ""
    if not text or len(text) < 180:
        return f"__ERROR__: 본문 수집 실패 ({url})"
    return text

# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://example.com/test-article-1",
        "https://example.com/test-article-2",
    ]
    for u in test_urls:
        print("\nURL:", u)
        t = get_article_text(u)
        print(t[:350] + ("..." if not t.startswith("__ERROR__") else ""))
