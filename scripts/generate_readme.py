#!/usr/bin/env python3
"""Update the recent-public-repositories section in README.md using the GitHub API."""
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

USERNAME = "Haimanot25"
README = Path("README.md")
START = "<!-- RECENT_PROJECTS_START -->"
END = "<!-- RECENT_PROJECTS_END -->"


def github_repositories():
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=100&type=owner"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "haimanot-profile-automation",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"GitHub API returned HTTP {exc.code}. Check username, network, or token.") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not reach GitHub API: {exc.reason}") from exc


def main():
    if not README.exists():
        raise SystemExit("README.md not found. Run this script from the profile repository root.")
    repos = github_repositories()
    repos = [
        repo for repo in repos
        if not repo.get("fork")
        and not repo.get("archived")
        and repo.get("name", "").lower() != USERNAME.lower()
    ]
    repos.sort(key=lambda repo: repo.get("updated_at", ""), reverse=True)

    rows = [
        "| Repository | Description | Language | Stars |",
        "| --- | --- | --- | ---: |",
    ]
    for repo in repos[:6]:
        name = repo["name"].replace("|", r"\|")
        description = (repo.get("description") or "No description yet").replace("|", r"\|").replace("\n", " ")
        language = repo.get("language") or "—"
        rows.append(
            f'| [{name}]({repo["html_url"]}) | {description[:100]} | {language} | {repo["stargazers_count"]} |'
        )
    if not repos:
        rows.append("| No public repositories found | Publish a public project to populate this section | — | 0 |")

    section = f"{START}\n" + "\n".join(rows) + f"\n{END}"
    content = README.read_text(encoding="utf-8")
    if START not in content or END not in content:
        raise SystemExit("Could not find recent-project marker comments in README.md.")
    before, rest = content.split(START, 1)
    _, after = rest.split(END, 1)
    updated = before + section + after
    if updated != content:
        README.write_text(updated, encoding="utf-8")
        print(f"Updated recent repository section ({min(len(repos), 6)} repositories shown).")
    else:
        print("README is already up to date.")


if __name__ == "__main__":
    main()
