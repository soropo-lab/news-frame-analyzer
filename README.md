# 🧠 News Frame Analyzer

국내 주요 언론 기사의 본문을 자동으로 수집하고, OpenRouter API를 활용해 기사 프레이밍과 편향 요소를 분석하는 도구입니다.  
Streamlit 기반 웹 UI를 통해 뉴스 URL만 입력하면 손쉽게 결과를 시각화할 수 있습니다.

---

## 📌 주요 기능

- ✅ JTBC / 조선일보 / 한겨레 / KBS / MBC 기사 본문 자동 수집  
- ✅ 광고, 스크립트 등 불필요한 요소 제거 후 정제된 텍스트 추출  
- ✅ OpenRouter API 기반 프레이밍/편향 분석  
- ✅ Streamlit UI를 통한 분석 결과 시각화 (모바일 대응)

---

## 🛠 설치 및 실행 방법

### 1️⃣ 저장소 클론
```bash
git clone https://github.com/soropo-lab/news-frame-analyzer.git
cd news-frame-analyzer

2️⃣ 패키지 설치
pip install -r requirements.txt

3️⃣ .env 파일 생성
루트 디렉토리에 .env 파일을 만들고 다음을 추가하세요👇

OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions
MODEL_NAME=openai/gpt-4-turbo-preview


⚠️ .env 파일은 .gitignore에 포함되어 있으며 절대 공개 저장소에 커밋하면 안 됩니다.

4️⃣ 앱 실행
streamlit run app.py
브라우저에서 http://localhost:8501
 로 접속하면 앱이 실행됩니다.

📂 폴더 구조
news-frame-analyzer/
├─ analyzer/
│  ├─ __init__.py
│  ├─ crawler_auto.py      # 뉴스 본문 수집기
│  ├─ gpt_analyzer.py      # OpenRouter API 기반 편향 분석
│  ├─ formatter.py         # 분석 결과 HTML 포맷 변환
│
├─ app.py                  # Streamlit 메인 실행 파일
├─ .env                    # API Key 환경 변수 (업로드 금지)
├─ .gitignore
├─ README.md
├─ requirements.txt
└─ LICENSE (선택)

🧪 사용 방법
app.py를 실행한 후
뉴스 기사 URL을 입력하고 “분석 시작” 클릭
기사 본문 수집 후 GPT 기반 분석 결과가 표로 출력됨

📝 Requirements
Python 3.9 이상
Streamlit
Requests
BeautifulSoup4
Selenium + webdriver-manager (JTBC 대응)
python-dotenv

⚠️ 주의사항
OpenRouter API Key는 절대 외부에 공개하지 마세요.
JTBC 기사는 React SPA 구조이므로 Selenium이 필요합니다.
기사 본문을 그대로 저장·재배포하는 것은 저작권 이슈가 있을 수 있으므로 분석 목적으로만 사용하세요.

🪪 License
이 프로젝트는 MIT 라이선스를 따릅니다.
자유롭게 포크하고 수정하여 사용 가능합니다.




# 🧠 News Frame Analyzer
A tool that automatically collects news articles from major Korean media outlets and analyzes their framing and bias using the OpenRouter API.  
With a Streamlit-based web UI, you can simply enter a news URL and visualize the analysis results instantly.

---

## 📌 Features
- ✅ Automatic article extraction from JTBC, Chosun, Hankyoreh, KBS, and MBC  
- ✅ Cleans up ads, scripts, and unnecessary tags for accurate text extraction  
- ✅ Framing and bias analysis powered by OpenRouter API  
- ✅ Streamlit UI optimized for both desktop and mobile devices

---

## 🛠 Installation & Usage

### 1️⃣ Clone the repository
```bash
git clone https://github.com/soropo-lab/news-frame-analyzer.git
cd news-frame-analyzer

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Create .env file

Create a .env file in the root directory and add the following:

OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions
MODEL_NAME=openai/gpt-4-turbo-preview


⚠️ .env is included in .gitignore and must never be committed to a public repository.

4️⃣ Run the app
streamlit run app.py


Open your browser and go to http://localhost:8501
 to use the app.

📂 Project Structure
news-frame-analyzer/
├─ analyzer/
│  ├─ __init__.py
│  ├─ crawler_auto.py      # News article crawler
│  ├─ gpt_analyzer.py      # Bias analysis using OpenRouter API
│  ├─ formatter.py         # Format GPT results into HTML tables
│
├─ app.py                  # Streamlit main app
├─ .env                    # API key (never commit this)
├─ .gitignore
├─ README.md
├─ requirements.txt
└─ LICENSE (optional)

🧪 How to Use

Run app.py

Paste a news article URL and click "Analyze"

The article will be crawled, analyzed, and displayed as a structured table

📝 Requirements

Python 3.9+

Streamlit

Requests

BeautifulSoup4

Selenium + webdriver-manager (for JTBC)

python-dotenv

⚠️ Notes

Never share or commit your OpenRouter API Key publicly.

JTBC articles use React SPA, so Selenium is required for rendering.

Do not store or redistribute raw news content — use it for analysis only to avoid copyright issues.

🪪 License

This project is licensed under the MIT License.
You are free to fork, modify, and use it for your own projects.
