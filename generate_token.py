"""
Run this script locally to generate the GARMINTOKENS_BASE64 env var for Railway.
Usage: python generate_token.py
"""
import os
import sys
import tarfile
import base64
import io
import getpass
import tempfile

try:
    from garminconnect import Garmin
except ImportError:
    print("Installing garminconnect...")
    os.system(f"{sys.executable} -m pip install garminconnect")
    from garminconnect import Garmin

email = input("Garmin email: ").strip()
password = getpass.getpass("Garmin password: ")

print("\nAuthenticating with Garmin Connect...")

tokenstore = os.path.join(tempfile.gettempdir(), "garmin_tokens_export")
os.makedirs(tokenstore, exist_ok=True)

try:
    garmin = Garmin(email=email, password=password)
    garmin.login()
    garmin.client.dump(tokenstore)
    print("Authentication successful.")
except Exception as e:
    print(f"Authentication failed: {e}")
    sys.exit(1)

buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w:gz") as tar:
    tar.add(tokenstore, arcname=".")
buf.seek(0)
result = base64.b64encode(buf.read()).decode()

print("\n" + "="*60)
print("Copy this value and set it as GARMINTOKENS_BASE64 on Railway:")
print("="*60)
print(result)
print("="*60)
