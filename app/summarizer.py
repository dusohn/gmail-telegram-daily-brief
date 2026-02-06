from typing import List
from openai import OpenAI

from .gmail_client import GmailMessage


def build_prompt(messages: List[GmailMessage]) -> str:
    if not messages:
        return "최근 24시간 새 메일이 없습니다."

    lines = []
    for i, m in enumerate(messages, start=1):
        lines.append(
            f"[{i}] From: {m.from_}\n"
            f"Subject: {m.subject}\n"
            f"Date: {m.date}\n"
            f"Snippet: {m.snippet}\n"
        )
    joined = "\n---\n".join(lines)

    return (
        "아래는 최근 24시간 동안의 Gmail 메시지 목록이다.\n"
        "요구사항:\n"
        "1) 한국어로 요약\n"
        "2) '중요/긴급 가능성' 높은 것 먼저\n"
        "3) 각 항목은 한 줄: [번호] 핵심요약 (발신자/주제)\n"
        "4) 마지막에 전체 한 줄 총평(오늘의 핵심)\n\n"
        f"{joined}"
    )


def summarize_with_openai(messages: List[GmailMessage], model: str = "gpt-4o-mini") -> str:
    prompt = build_prompt(messages)
    client = OpenAI()

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "너는 업무 비서처럼 간결하게 메일을 요약한다."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
