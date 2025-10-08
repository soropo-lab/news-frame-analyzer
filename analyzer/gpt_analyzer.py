# -*- coding: utf-8 -*-
import os
import json
import requests
from dotenv import load_dotenv

# 환경 변수 로드 (.env 파일 사용)
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-3.5-turbo")

def analyze_bias(text: str) -> str:
    """
    뉴스 기사 본문을 분석하여 프레이밍, 감정 표현, 사실·의견 구분,
    정보의 균형성, 출처 신뢰도, 종합 위험도 등을 간결히 요약한다.
    """
    prompt = f"""
다음 뉴스 기사 본문을 분석하여 아래 항목을 '항목명: 내용' 형식으로 간결하게 작성해줘.

1. 프레이밍 방식 및 관점
2. 감정적 표현 및 선동 요소
3. 사실과 의견 구분의 명확성
4. 정보의 균형성 및 누락 여부
5. 출처와 근거의 신뢰도
6. 종합 위험도 평가 (낮음/보통/높음) 및 이유

[뉴스 본문]
{text[:4000]}
""".strip()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY.strip()}",
        "Content-Type": "application/json; charset=utf-8",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a strict and neutral media framing analyst."},
            {"role": "user", "content": prompt},
        ],
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    r = requests.post(OPENROUTER_URL, headers=headers, data=data, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
