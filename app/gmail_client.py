import base64
from dataclasses import dataclass
from typing import List, Optional

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


@dataclass
class GmailMessage:
    id: str
    subject: str
    from_: str
    date: str
    snippet: str


def _get_header(headers, name: str) -> str:
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def _safe_snippet(msg: dict) -> str:
    # Gmail snippet is usually enough; avoid heavy MIME parsing
    return (msg.get("snippet") or "").strip()


def fetch_messages(
    creds: Credentials,
    query: str,
    max_results: int = 20,
) -> List[GmailMessage]:
    service = build("gmail", "v1", credentials=creds)

    resp = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    msg_ids = [m["id"] for m in resp.get("messages", [])]

    out: List[GmailMessage] = []
    for mid in msg_ids:
        m = service.users().messages().get(userId="me", id=mid, format="metadata", metadataHeaders=["Subject", "From", "Date"]).execute()
        payload = m.get("payload", {})
        headers = payload.get("headers", [])

        out.append(
            GmailMessage(
                id=mid,
                subject=_get_header(headers, "Subject"),
                from_=_get_header(headers, "From"),
                date=_get_header(headers, "Date"),
                snippet=_safe_snippet(m),
            )
        )
    return out
