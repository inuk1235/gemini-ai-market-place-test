# Facebook Marketplace Alert App (Android + Backend)

> **Note:** Automated access to Facebook Marketplace may be restricted by Facebook's Terms of Service.
> Ensure you have permission to access data and comply with all applicable terms and laws.

## Overview
This repository provides a starter Android UI and a Python backend for searching Facebook Marketplace and alerting users when new listings match their criteria.

### Features
- Android UI: keyword, location, radius, start button
- Background polling with WorkManager
- Android notifications for new listings
- Python backend with Playwright headless browser
- Basic anti-ban techniques (user-agent rotation, randomized delays)

## Project Structure
```
backend/                        # Flask + Playwright scraper
android/                        # Android Kotlin UI + worker
```

## Backend (Python)

### Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
playwright install
```

### Run
```bash
python backend/app.py
```

### API
`POST /search`
```json
{
  "keyword": "bicycle",
  "location": "san-francisco",
  "radiusKm": 25
}
```

## Android App

### Key Files
- `MainActivity.kt` — UI + starts background search
- `SearchWorker.kt` — periodic search + notification
- `BackendApi.kt` — stub network client (replace with Retrofit/OkHttp)

### Setup Notes
- Integrate Retrofit/OkHttp to call the backend `/search` endpoint.
- Register notification channels for Android 8.0+.

## Web/Email Alerts
You can reuse the backend search function and send email alerts using a provider like SendGrid or AWS SES.

## Scaling Suggestions
- Add a job queue (Redis + Celery or BullMQ)
- Batch queries per region
- Use proxy rotation for reliability
- Cache results to reduce duplicate scraping
