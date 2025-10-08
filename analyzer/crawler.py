# -*- coding: utf-8 -*-
"""
📰 국내 주요 언론 자동 뉴스 본문 수집기 (v6.1, 2025년 10월 기준)
 - 조선일보, JTBC, 한겨레, KBS, MBC 자동 감지
 - JSON + HTML 구조 대응
 - 광고, 스크립트, iframe, figure 자동 제거
 - Streamlit 환경에서도 멈춤 없음 (Selenium 미사용)
"""

import re
import requests
from bs4 import BeautifulSoup

# -------------------------------------------------
# 🧼 공통: 텍스트 정리 함수
# -------------------------------------------------
def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


# -------------------------------------------------
# 🌐 공통 User-Agent
# -------------------------------------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0 Safari/537.36"
}


# -------------------------------------------------
# 📰 조선일보
# -------------------------------------------------
def get_chosun_text(url):
    """조선일보 JSON + HTML"""
    # ① JSON 시도
    try:
        m = re.search(r"chosun\.com/(.+?)/(\d{4})/(\d{2})/([A-Z0-9]+)/", url)
        if m:
            section, year, month, article_id = m.groups()
            json_url = f"https://www.chosun.com/__data/fusion/cached/page/article/{section}/{year}/{month}/{article_id}.json"
            res = requests.get(json_url, timeout=10)
            res.raise_for_status()
            data = res.json()
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

    # ② HTML 시도
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        article = soup.select_one(
            "div.article-body, section.article-body, div[data-fusion-container]"
        )
        if article:
            text = " ".join(p.get_text(strip=True) for p in article.find_all("p"))
            return clean_text(text)
    except Exception:
        pass
    return ""


# -------------------------------------------------
# 📰 JTBC (2025년 10월 최신 구조 대응)
# -------------------------------------------------
def get_jtbc_text(url):
    """JTBC 뉴스 본문 수집"""
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # ✅ 최신 구조: id="ijam_content"
        article = soup.select_one(
            "#ijam_content, #article_content, #article_content_area, .article_content"
        )
        if not article:
            # id에 'jam_content'가 포함된 모든 div 탐색
            article = soup.find("div", id=lambda x: x and "jam_content" in x)
        if not article:
            return ""

        # 광고/iframe/스크립트 제거
        for tag in article.select(
            "script, iframe, figure, div.ad_area, .set_contents_video_ad, .set_contents_image_ad"
        ):
            tag.decompose()

        # ✅ span, b, p 모두 포함해서 텍스트 수집
        texts = []
        for tag in article.find_all(["p", "span", "b"]):
            t = tag.get_text(strip=True)
            if t and not t.lower().startswith("advertisement"):
                texts.append(t)

        text = " ".join(texts)
        return clean_text(text)
    except Exception as e:
        return f"__ERROR__: {e}"


# -------------------------------------------------
# 📰 한겨레
# -------------------------------------------------
def get_hani_text(url):
    """한겨레 본문"""
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        article = soup.select_one("div.article-text, div.text, #article-text")
        if article:
            text = " ".join(p.get_text(strip=True) for p in article.find_all("p"))
            return clean_text(text)
    except Exception:
        pass
    return ""


# -------------------------------------------------
# 📰 KBS
# -------------------------------------------------
def get_kbs_text(url):
    """KBS 본문"""
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        article = soup.select_one("div.detail-body, div.detail_body, .view_cont")
        if article:
            text = " ".join(p.get_text(strip=True) for p in article.find_all("p"))
            return clean_text(text)
    except Exception:
        pass
    return ""


# -------------------------------------------------
# 📰 MBC
# -------------------------------------------------
def get_mbc_text(url):
    """MBC 본문"""
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        article = soup.select_one("div.news_cont, div.news_body, div#content")
        if article:
            text = " ".join(p.get_text(strip=True) for p in article.find_all("p"))
            return clean_text(text)
    except Exception:
        pass
    return ""


# -------------------------------------------------
# 🧩 자동 감지 통합 함수
# -------------------------------------------------
def get_article_text(url):
    """URL 기반으로 언론사 감지 후 본문 자동 수집"""
    url = url.strip().lower()

    if "chosun.com" in url:
        text = get_chosun_text(url)
    elif "jtbc.co.kr" in url:
        text = get_jtbc_text(url)
    elif "hani.co.kr" in url:
        text = get_hani_text(url)
    elif "kbs.co.kr" in url:
        text = get_kbs_text(url)
    elif "mbc.co.kr" in url:
        text = get_mbc_text(url)
    else:
        # Fallback: <p> 전체 수집
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            text = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))
            text = clean_text(text)
        except Exception:
            text = ""

    if not text or len(text) < 200:
        return f"__ERROR__: 본문 수집 실패 ({url})"
    return text


# -------------------------------------------------
# 🧪 단독 테스트용 실행
# -------------------------------------------------
if __name__ == "__main__":
    urls = [
        "https://news.jtbc.co.kr/article/NB12265505",
        "https://www.chosun.com/economy/market_trend/2025/09/29/IFEAT6REQBB5NH77T7YYJ2RYX4/",
        "https://www.hani.co.kr/arti/opinion/editorial/1221403.html",
        "https://news.kbs.co.kr/news/pc/view/view.do?ncd=8370213",
        "https://imnews.imbc.com/replay/2025/nwdesk/article/6572301_36192.html",
    ]

    for url in urls:
        print(f"\n▶ {url}")
        text = get_article_text(url)
        if text.startswith("__ERROR__"):
            print(text)
        else:
            print(text[:350] + "...")
