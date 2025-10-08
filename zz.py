# -*- coding: utf-8 -*-
"""
📰 JTBC 기사 본문 추출 (Selenium 완전 렌더링 버전)
 - Cloudflare + React 렌더링 대응
 - Chrome Headless 사용
"""

import re, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def get_jtbc_article(url):
    """JTBC 뉴스 본문 수집 (Selenium 완전 렌더링)"""
    try:
        # ✅ Chrome 설정
        chrome_opts = Options()
        chrome_opts.add_argument("--headless=new")
        chrome_opts.add_argument("--disable-gpu")
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--log-level=3")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)
        driver.get(url)

        # ✅ JS 렌더링 완료 대기
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ijam_content"))
        )
        time.sleep(1.5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        article = soup.select_one("#ijam_content")

        if not article:
            return "__ERROR__: 본문 div를 찾지 못했습니다."

        # 광고, 스크립트 제거
        for tag in article.select(
            "script, iframe, figure, div.ad_area, .set_contents_image_ad, .set_contents_video_ad"
        ):
            tag.decompose()

        texts = []
        for tag in article.find_all(["p", "span", "b"]):
            t = tag.get_text(strip=True)
            if t and not t.lower().startswith("advertisement"):
                texts.append(t)

        driver.quit()

        text = clean_text(" ".join(texts))
        if len(text) < 100:
            return "__ERROR__: 본문 추출 실패 (짧음)"
        return text
    except Exception as e:
        return f"__ERROR__: {e}"

if __name__ == "__main__":
    url = "https://news.jtbc.co.kr/article/NB12265505"
    result = get_jtbc_article(url)

    print("\n📄 [JTBC 본문 추출 결과]\n")
    print(result[:600] + "..." if not result.startswith("__ERROR__") else result)
