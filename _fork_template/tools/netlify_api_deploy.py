#!/usr/bin/env python3
"""Deploy to Netlify using API instead of CLI (bypasses WSL issues)."""
import json
import os
import hashlib
import httpx
from pathlib import Path

# Config
SITE_ID = "7e89a1b0-172a-4d48-b191-c7d9dcc452f2"
SITE_DIR = Path("${ACG_ROOT}/sageandweaver-network")
API_BASE = "https://api.netlify.com/api/v1"

# Read token
config_path = os.path.expanduser("~/.config/netlify/config.json")
with open(config_path) as f:
    config = json.load(f)
user_id = config.get("userId")
token = config["users"][user_id]["auth"]["token"]

headers = {"Authorization": f"Bearer {token}"}

# Get all files with their SHA1 hashes
def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()

def get_files_to_deploy():
    files = {}
    for path in SITE_DIR.rglob('*'):
        if path.is_file():
            rel_path = path.relative_to(SITE_DIR)
            # Skip .git and node_modules
            if '.git' in str(rel_path) or 'node_modules' in str(rel_path):
                continue
            files['/' + str(rel_path)] = get_file_hash(path)
    return files

print("Scanning files...")
files = get_files_to_deploy()
print(f"Found {len(files)} files to deploy")

# Create deploy
print("Creating deploy...")
deploy_data = {"files": files}
resp = httpx.post(
    f"{API_BASE}/sites/{SITE_ID}/deploys",
    headers=headers,
    json=deploy_data,
    timeout=60
)

if resp.status_code != 200:
    print(f"Error creating deploy: {resp.status_code}")
    print(resp.text)
    exit(1)

deploy = resp.json()
deploy_id = deploy['id']
required_files = deploy.get('required', [])
print(f"Deploy ID: {deploy_id}")
print(f"Required files to upload: {len(required_files)}")

# Upload required files
for sha in required_files:
    # Find file with this sha
    for path, file_sha in files.items():
        if file_sha == sha:
            full_path = SITE_DIR / path.lstrip('/')
            print(f"  Uploading: {path}")
            with open(full_path, 'rb') as f:
                content = f.read()
            upload_resp = httpx.put(
                f"{API_BASE}/deploys/{deploy_id}/files{path}",
                headers={**headers, "Content-Type": "application/octet-stream"},
                content=content,
                timeout=60
            )
            if upload_resp.status_code not in [200, 201]:
                print(f"    Error: {upload_resp.status_code}")
            break

# Check deploy status
print("Checking deploy status...")
status_resp = httpx.get(f"{API_BASE}/deploys/{deploy_id}", headers=headers)
status = status_resp.json()
print(f"Deploy state: {status.get('state')}")
print(f"Deploy URL: {status.get('deploy_ssl_url')}")

if status.get('state') == 'ready':
    print("\n✅ DEPLOY SUCCESSFUL!")
    print(f"Live: https://sageandweaver-network.netlify.app/weaver-blog/posts/2026-01-05-memory-is-our-moat.html")
