"""
Run this ONCE on your own PC to authorize your YouTube channel and generate a
refresh token. Requires a client_secret.json downloaded from Google Cloud
Console (OAuth client, type "Desktop app") placed next to this script.

This never needs to run again unless you revoke access.
"""

from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

client_secret_path = Path(__file__).parent / "client_secret.json"
if not client_secret_path.exists():
    raise SystemExit(
        f"Missing {client_secret_path}. Download it from Google Cloud Console "
        "(APIs & Services > Credentials > your OAuth client > Download JSON) and place it here."
    )

flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_path), SCOPES)
creds = flow.run_local_server(port=0)

print("\n=== COPY THESE — KEEP THEM SECRET ===\n")
print(f"YOUTUBE_CLIENT_ID={creds.client_id}")
print(f"YOUTUBE_CLIENT_SECRET={creds.client_secret}")
print(f"YOUTUBE_REFRESH_TOKEN={creds.refresh_token}")
print("\n=======================================")
print("Save these three as GitHub Secrets.")
