"""Update the star counts in the README tables. Uses only the Python standard library."""
import json, os, re, urllib.request

ROW = re.compile(r'^(\| \[([\w.-]+/[\w.-]+)\]\(https://github\.com/[^)]+\) \| )⭐(?:&nbsp;| )[^|]*( \|.*)$', re.M)

def stars(repo):
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}")
    req.add_header("Accept", "application/vnd.github+json")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["stargazers_count"]

def short(n):
    if n >= 1000:
        return f"{n/1000:.1f}".rstrip("0").rstrip(".") + "k"
    return str(n)

def fix(m):
    try:
        return f"{m.group(1)}⭐&nbsp;{short(stars(m.group(2)))}{m.group(3)}"
    except Exception as e:  # keep the old number if one repo fails
        print(f"Skipped {m.group(2)}: {e}")
        return m.group(0)

text = open("README.md", encoding="utf-8").read()
new = ROW.sub(fix, text)
if new != text:
    open("README.md", "w", encoding="utf-8").write(new)
    print("README updated.")
else:
    print("No change.")
