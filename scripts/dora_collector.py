import os
import json
from datetime import datetime, timedelta, timezone
import requests

API = "https://api.github.com"
REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]

DAYS_BACK = 90
INCIDENT_LABEL = "incident"
INCIDENT_WINDOW_HOURS = 48

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

def parse_dt(s: str):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def get_all(url, params=None, limit=2000):
    items, next_url = [], url
    while next_url and len(items) < limit:
        r = requests.get(next_url, headers=HEADERS, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list):
            items.extend(data)
        else:
            items.extend(data.get("items", []))
        next_url = r.links.get("next", {}).get("url")
        params = None
    return items

def main():
    since = datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)

    # 1) Deployments = GitHub Releases
    releases = get_all(f"{API}/repos/{REPO}/releases", params={"per_page": 100})
    deployments = [
        r for r in releases
        if (not r.get("draft")) and (not r.get("prerelease")) and r.get("published_at")
        and parse_dt(r["published_at"]) >= since
    ]
    deployments.sort(key=lambda r: r["published_at"])

    # 2) Changes = PRs merged to main
    prs = get_all(f"{API}/repos/{REPO}/pulls", params={"state": "closed", "base": "main", "per_page": 100})
    merged_prs = [
        p for p in prs
        if p.get("merged_at") and parse_dt(p["merged_at"]) >= since
    ]
    merged_prs.sort(key=lambda p: p["merged_at"])

    # 3) Incidents = Issues with label 'incident'
    issues = get_all(f"{API}/repos/{REPO}/issues", params={"state": "all", "labels": INCIDENT_LABEL, "per_page": 100})
    incidents = [
        i for i in issues
        if ("pull_request" not in i) and i.get("created_at") and parse_dt(i["created_at"]) >= since
    ]

    # DF: deployments per week (approx over window)
    weeks = max(1.0, DAYS_BACK / 7.0)
    df_per_week = len(deployments) / weeks

    # Lead Time: PR merged -> next deployment
    dep_times = [parse_dt(d["published_at"]) for d in deployments]
    lead_hours = []
    for pr in merged_prs:
        m = parse_dt(pr["merged_at"])
        nxt = next((dt for dt in dep_times if dt >= m), None)
        if nxt:
            lead_hours.append((nxt - m).total_seconds() / 3600.0)
    avg_lead = (sum(lead_hours) / len(lead_hours)) if lead_hours else None

    # CFR: deployment "failed" if incident created within 48h after release
    window = timedelta(hours=INCIDENT_WINDOW_HOURS)
    failed = 0
    for d in deployments:
        dep_t = parse_dt(d["published_at"])
        end = dep_t + window
        if any(dep_t <= parse_dt(i["created_at"]) <= end for i in incidents):
            failed += 1
    cfr = (failed / len(deployments)) if deployments else None

    # MTTR: avg incident close - open
    mttr_hours = []
    for i in incidents:
        if i.get("closed_at"):
            o = parse_dt(i["created_at"])
            c = parse_dt(i["closed_at"])
            mttr_hours.append((c - o).total_seconds() / 3600.0)
    avg_mttr = (sum(mttr_hours) / len(mttr_hours)) if mttr_hours else None

    metrics = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window_days": DAYS_BACK,
        "kpis": {
            "deployment_frequency_per_week": df_per_week,
            "lead_time_avg_hours": avg_lead,
            "change_failure_rate": cfr,
            "mttr_avg_hours": avg_mttr
        }
    }

    os.makedirs("docs", exist_ok=True)
    with open("docs/metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("Updated docs/metrics.json")

if __name__ == "__main__":
    main()
