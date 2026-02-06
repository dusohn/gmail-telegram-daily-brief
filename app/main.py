import os
from datetime import datetime, timezone, timedelta

from google.oauth2.credentials import Credentials

from app.gmail_client import fetch_messages
from app.summarizer import summarize_with_openai
from app.telegram_client import send_telegram_message


def build_creds_from_env() -> Credentials:
    # OAuth2 (Installed App) 기반 refresh token 방식
    client_id = os.environ["GMAIL_CLIENT_ID"]
    client_secret = os.environ["GMAIL_CLIENT_SECRET"]
    refresh_token = os.environ["GMAIL_REFRESH_TOKEN"]

    return Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
    )


def main():
    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]
    openai_model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    # 최근 24시간: Gmail 검색은 서버 시간 기준이 섞일 수 있어 'newer_than:1d'가 가장 간단/안정적
    # 필요하면 라벨/프로모션 제외 등을 추가로 조정 가능
    query = os.environ.get("GMAIL_QUERY", 'newer_than:1d in:inbox -category:promotions -category:social')

    creds = build_creds_from_env()

    messages = fetch_messages(creds, query=query, max_results=int(os.environ.get("MAX_RESULTS", "25")))
    summary = summarize_with_openai(messages, model=openai_model)

    today_kst = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d")
    header = f"📬 Gmail 데일리 브리프 ({today_kst}, 최근 24시간)\n"
    text = header + "\n" + summary

    send_telegram_message(telegram_token, telegram_chat_id, text)


if __name__ == "__main__":
    main()
