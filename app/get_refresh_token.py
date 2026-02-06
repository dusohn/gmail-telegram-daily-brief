import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail Readonly 권한
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    """
    사용법:
    1) Google Cloud에서 OAuth 클라이언트(Desktop app) 만들기
    2) credentials.json 다운로드 받아서 이 파일과 같은 폴더에 둠
    3) python tools/get_refresh_token.py 실행
    4) 출력되는 refresh_token을 GitHub Secrets에 저장
    """
    with open("credentials.json", "r", encoding="utf-8") as f:
        client_config = json.load(f)

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0)

    print("\n=== COPY THESE ===")
    print("client_id:", creds.client_id)
    print("client_secret:", creds.client_secret)
    print("refresh_token:", creds.refresh_token)

if __name__ == "__main__":
    main()
