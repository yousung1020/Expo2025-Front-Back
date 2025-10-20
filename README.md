# GLife - 산업안전 교육 관리 플랫폼

## 1. 프로젝트 소개

GLife는 산업 현장의 안전 교육을 효율적으로 관리하고, AI를 통해 실제와 같은 훈련 경험을 제공하는 웹 기반 플랫폼입니다. 관리자는 교육 과정을 생성하고 직원을 등록할 수 있으며, 대시보드를 통해 전체 현황을 직관적으로 파악할 수 있습니다.

사용자는 AI 동작 인식을 통해 소화기 사용법과 같은 안전 훈련을 수행하고, 자신의 점수를 확인하며 학습 효과를 높일 수 있습니다.

## 2. 주요 기능

*   **대시보드**: 연간/분기별 교육 일정과 전체 이수율 등 핵심 현황 시각화
*   **교육 과정 관리**: 연도 및 분기별 교육 과정 생성 및 관리
*   **직원 관리**: 엑셀 파일을 이용한 다수 직원 정보 일괄 등록 및 개별 관리
*   **수강 관리**: 과정별 수강생 등록 및 수강 여부 추적
*   **AI 기반 안전 훈련**: 센서 데이터를 활용한 동작(예: 소화기 사용) 평가 및 점수 제공

## 3. 기술 스택

### Backend
*   **Framework**: Django, Django REST Framework
*   **Authentication**: Simple JWT (JSON Web Token)
*   **Database**: MySQL
*   **AI / Data**: dtaidistance, pandas, numpy

### Frontend
*   **Framework**: React
*   **Build Tool**: Vite
*   **Styling**: Tailwind CSS
*   **Routing**: React Router
*   **HTTP Client**: Axios, Fetch API

## 4. 프로젝트 구조

```
.
├── django/      # Django 백엔드 프로젝트
│   ├── ai/          # AI 평가 로직 및 API
│   ├── courses/     # 교육 과정 관리 앱
│   ├── enrollments/ # 수강 신청 관리 앱
│   └── ...
├── react/       # React 프론트엔드 프로젝트
│   ├── src/
│   │   ├── pages/   # 각 페이지 컴포넌트
│   │   ├── components/ # 공통 UI 컴포넌트
│   │   └── lib/     # API 연동 및 인증 로직
│   └── ...
└── README.md    # 프로젝트 전체 소개
```

## 5. 로컬 환경 설정 및 실행

### Backend (Django)
1.  `django` 디렉토리로 이동합니다.
    ```bash
    cd django
    ```
2.  가상환경을 생성하고 활성화합니다.
3.  필요한 패키지를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```
4.  `.env` 파일을 생성하고 데이터베이스 및 시크릿 키 설정을 완료합니다.
5.  데이터베이스 마이그레이션을 적용합니다.
    ```bash
    python manage.py migrate
    ```
6.  개발 서버를 실행합니다.
    ```bash
    python manage.py runserver
    ```

### Frontend (React)
1.  `react` 디렉토리로 이동합니다.
    ```bash
    cd react
    ```
2.  필요한 패키지를 설치합니다.
    ```bash
    npm install
    ```
3.  `.env` 파일을 생성하고 백엔드 API 서버 주소(`VITE_API_BASE_URL`)를 설정합니다.
4.  개발 서버를 실행합니다.
    ```bash
    npm run dev
    ```
