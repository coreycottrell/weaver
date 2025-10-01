#!/usr/bin/env python3
"""
AI-CIV GitHub Auto-Backup System
Automatically backs up collective to GitHub repository
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import git
from dotenv import load_dotenv
import requests

sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

# GitHub credentials
GITHUB_TOKEN = os.getenv('PAT')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'ai-CIV-2025')
REPO_NAME = 'ai-civ-collective'

# Repository path
REPO_PATH = Path(__file__).parent.parent


def create_github_repo():
    """Create new GitHub repository"""
    print(f"📦 Creating GitHub repository: {GITHUB_USERNAME}/{REPO_NAME}")

    url = "https://api.github.com/user/repos"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    data = {
        'name': REPO_NAME,
        'description': '🎭 AI-CIV Collective - Multi-Agent Intelligence System with The Conductor',
        'private': False,
        'auto_init': False,
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            repo_data = response.json()
            print(f"✅ Repository created: {repo_data['html_url']}")
            return repo_data['clone_url']

        elif response.status_code == 422:
            # Repository already exists
            print(f"ℹ️  Repository already exists, using existing repo")
            return f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

        else:
            print(f"❌ Failed to create repository: {response.status_code}")
            print(f"   {response.json()}")
            return None

    except Exception as e:
        print(f"❌ Error creating repository: {e}")
        return None


def init_git_repo():
    """Initialize git repository if needed"""
    try:
        repo = git.Repo(REPO_PATH)
        print(f"✅ Git repository already initialized")
        return repo
    except git.exc.InvalidGitRepositoryError:
        print(f"📝 Initializing git repository at {REPO_PATH}")
        repo = git.Repo.init(REPO_PATH)
        print(f"✅ Git repository initialized")
        return repo


def add_remote(repo, remote_url):
    """Add GitHub remote"""
    try:
        # Check if remote exists
        if 'origin' in [remote.name for remote in repo.remotes]:
            origin = repo.remote('origin')
            # Update URL
            origin.set_url(remote_url)
            print(f"✅ Updated remote 'origin' to {remote_url}")
        else:
            # Add new remote
            repo.create_remote('origin', remote_url)
            print(f"✅ Added remote 'origin': {remote_url}")

        return True

    except Exception as e:
        print(f"❌ Error adding remote: {e}")
        return False


def create_gitignore():
    """Create .gitignore if it doesn't exist or update it"""
    gitignore_path = REPO_PATH / '.gitignore'

    ignore_patterns = [
        "# Session-specific runtime data",
        ".claude/memory/session-context.json",
        "",
        "# User-specific preferences",
        ".claude/memory/user-preferences.md",
        "",
        "# Observatory state (runtime data)",
        ".claude/observatory/dashboard-state.json",
        ".claude/observatory/config.json",
        "",
        "# Environment variables",
        ".env",
        "",
        "# Python",
        "__pycache__/",
        "*.py[cod]",
        "*$py.class",
        "*.so",
        ".Python",
        "env/",
        "venv/",
        ".venv/",
        "*.egg-info/",
        "",
        "# IDEs",
        ".vscode/",
        ".idea/",
        "*.swp",
        "*.swo",
        "",
        "# OS",
        ".DS_Store",
        "Thumbs.db",
        "",
        "# Logs",
        "*.log",
    ]

    with open(gitignore_path, 'w') as f:
        f.write('\n'.join(ignore_patterns))

    print(f"✅ Created/updated .gitignore")


def commit_and_push(repo, message=None):
    """Commit all changes and push to GitHub"""
    try:
        # Check if there are changes
        if not repo.is_dirty(untracked_files=True):
            print("ℹ️  No changes to commit")
            return True

        # Add all files (respecting .gitignore)
        repo.git.add(A=True)

        # Create commit message
        if not message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"🎭 Auto-backup: {timestamp}"

        # Commit
        repo.index.commit(message)
        print(f"✅ Committed: {message}")

        # Push to GitHub
        print(f"📤 Pushing to GitHub...")

        # Configure authentication
        remote_url = repo.remotes.origin.url
        if not remote_url.startswith('https://'):
            # Update URL to use token authentication
            remote_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
            repo.remotes.origin.set_url(remote_url)

        # Push
        origin = repo.remotes.origin
        origin.push(refspec='master:main', force=True)

        print(f"✅ Pushed to GitHub successfully!")
        print(f"🌐 View at: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")

        return True

    except Exception as e:
        print(f"❌ Error during commit/push: {e}")
        return False


def setup_github_backup():
    """Complete setup of GitHub backup system"""
    print("🎭 AI-CIV GitHub Auto-Backup Setup")
    print("=" * 60)

    # Step 1: Create GitHub repository
    remote_url = create_github_repo()
    if not remote_url:
        print("❌ Failed to create/access GitHub repository")
        return False

    # Step 2: Initialize local git repo
    repo = init_git_repo()

    # Step 3: Create .gitignore
    create_gitignore()

    # Step 4: Add remote
    if not add_remote(repo, remote_url):
        return False

    # Step 5: Initial commit and push
    print("\n📝 Creating initial commit...")
    if commit_and_push(repo, "🎭 Initial commit - AI-CIV Collective Observatory\n\nComplete multi-agent intelligence system with real-time visualization, email reporting, and automated GitHub backups."):
        print("\n✅ GitHub backup system setup complete!")
        print(f"🌐 Repository: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
        return True
    else:
        return False


def auto_backup(message=None):
    """Perform automatic backup (to be called after missions)"""
    try:
        repo = git.Repo(REPO_PATH)

        if not message:
            # Generate message based on latest deployment
            from tools.github_backup import load_latest_deployment
            deployment = load_latest_deployment()

            if deployment:
                task = deployment.get('task', 'mission')
                message = f"🎭 Backup after mission: {task}"
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                message = f"🎭 Auto-backup: {timestamp}"

        return commit_and_push(repo, message)

    except Exception as e:
        print(f"❌ Auto-backup failed: {e}")
        return False


def load_latest_deployment():
    """Load latest deployment from Observatory state"""
    try:
        state_file = REPO_PATH / ".claude/observatory/dashboard-state.json"
        if not state_file.exists():
            return None

        import json
        with open(state_file, 'r') as f:
            state = json.load(f)

        # Get most recent from history
        history = state.get('history', [])
        if history:
            return history[0]

        return None

    except Exception:
        return None


if __name__ == '__main__':
    # Run setup
    if len(sys.argv) > 1 and sys.argv[1] == 'setup':
        setup_github_backup()
    else:
        # Perform backup
        auto_backup()
