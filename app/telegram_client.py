import requests


def send_telegram_message(bot_token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # 텔레그램 메시지 길이 제한 대비(4096자) - 길면 잘라서 여러 번 보냄
    chunks = []
    max_len = 3800
    s = text
    while len(s) > max_len:
        cut = s.rfind("\n", 0, max_len)
        if cut == -1:
            cut = max_len
        chunks.append(s[:cut])
        s = s[cut:].lstrip("\n")
    chunks.append(s)

    for c in chunks:
        r = requests.post(url, json={"chat_id": chat_id, "text": c, "disable_web_page_preview": True}, timeout=30)
        r.raise_for_status()
