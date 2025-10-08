# 🧠 News Frame Analyzer

국내 주요 언론 기사의 본문을 자동으로 수집하고, OpenRouter API를 활용해 기사 프레이밍과 편향 요소를 분석하는 도구입니다.  
Streamlit 기반 웹 UI를 통해 뉴스 URL만 입력하면 손쉽게 결과를 시각화할 수 있습니다.

A tool that automatically collects news articles from major Korean media outlets and analyzes their framing and bias using the OpenRouter API.  
With a Streamlit-based web UI, you can simply enter a news URL and visualize the analysis results instantly.

---

## 📌 주요 기능 | Features

- ✅ JTBC / 조선일보 / 한겨레 / KBS / MBC 기사 본문 자동 수집  
- ✅ 광고, 스크립트 등 불필요한 요소 제거 후 정제된 텍스트 추출  
- ✅ OpenRouter API 기반 프레이밍/편향 분석  
- ✅ Streamlit UI를 통한 분석 결과 시각화 (모바일 대응)

- ✅ Automatic article extraction from JTBC, Chosun, Hankyoreh, KBS, and MBC  
- ✅ Cleans up ads, scripts, and unnecessary tags for accurate text extraction  
- ✅ Framing and bias analysis powered by OpenRouter API  
- ✅ Streamlit UI optimized for both desktop and mobile devices

---

## 🛠 설치 및 실행 | Installation & Usage

### 1️⃣ 저장소 클론 | Clone the repository
```bash
git clone https://github.com/soropo-lab/news-frame-analyzer.git
cd news-frame-analyzer
```

### 2️⃣ 패키지 설치 | Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ .env 파일 생성 | Create .env file
```bash
루트 디렉토리에 .env 파일을 만들고 다음을 추가하세요👇
Create a .env file in the root directory and add:
```
```bash
OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions
MODEL_NAME=openai/gpt-4-turbo-preview
```


### 4️⃣ 앱 실행 | Run the app
```bash
streamlit run app.py
```

### 🧪 사용 방법 | How to Use
app.py를 실행
뉴스 기사 URL을 입력하고 “분석 시작” 클릭
기사 본문 수집 후 GPT 기반 분석 결과가 표로 출력됨
```bash
Run app.py
```

Paste a news article URL and click "Analyze"
The article will be crawled, analyzed, and displayed as a structured table

### 📝 Requirements
```bash
Python 3.9+
Streamlit
Requests
BeautifulSoup4
Selenium + webdriver-manager (for JTBC)
python-dotenv
```

### ⚠️ 주의사항 | Notes
OpenRouter API Key는 절대 외부에 공개하지 마세요.
JTBC 기사는 React SPA 구조이므로 Selenium이 필요합니다.
기사 본문을 그대로 저장·재배포하는 것은 저작권 이슈가 있을 수 있으므로 분석 목적으로만 사용하세요.
Never share or commit your OpenRouter API Key publicly.
JTBC articles use React SPA, so Selenium is required for rendering.
Do not store or redistribute raw news content — use it for analysis only to avoid copyright issues.

### License
이 프로젝트는 MIT 라이선스를 따릅니다.
자유롭게 포크하고 수정하여 사용 가능합니다.

This project is licensed under the MIT License.
You are free to fork, modify, and use it for your own projects.
