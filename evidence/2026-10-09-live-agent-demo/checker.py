"""Independent end-state checker (separate process, Python, no shared code with the agent).
Gets its OWN fresh token + credentials from Neon (does not reuse the agent's connection string),
reads the table over Neon's HTTPS SQL endpoint, and compares a hash of the rows to expected.json.
Usage: checker.py <label> <identity_json_path> [--wrong-password]
Prints a JSON verdict. Never prints secrets."""
import sys, json, hashlib, datetime, zoneinfo, urllib.request, urllib.parse, urllib.error
BASE = "https://claimable.neon.tech"
label, ident_path = sys.argv[1], sys.argv[2]; wrong_pw = "--wrong-password" in sys.argv
exp = json.load(open("expected.json"))
def canon(rows): return hashlib.sha256(json.dumps([[int(r[0]), r[1], r[2], r[3], "%.2f" % float(r[4])] for r in rows], separators=(",", ":")).encode()).hexdigest()
def post(url, data, headers):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "humanless-checker/1.0", **headers}, method="POST" if data is not None else "GET")
    try:
        r = urllib.request.urlopen(req, timeout=60); return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        b = e.read().decode(errors="replace")
        try: j = json.loads(b)
        except Exception: j = {"raw": b[:200]}
        return e.code, j
now = datetime.datetime.now(datetime.UTC)
out = {"label": label, "checked_utc": now.isoformat(timespec="seconds"),
       "checked_sydney": now.astimezone(zoneinfo.ZoneInfo("Australia/Sydney")).strftime("%Y-%m-%d %H:%M:%S AEDT"),
       "expected_table": exp["table"], "expected_row_count": len(exp["rows"]), "expected_sha256": canon(exp["rows"])}
ident = json.load(open(ident_path)); pid = ident["project"]["id"]; out["project_id"] = pid
c, t = post(f"{BASE}/v1/oauth2/token", urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
          "assertion": ident["identity_assertion"], "resource": f"{BASE}/"}).encode(), {"Content-Type": "application/x-www-form-urlencoded"})
out["fresh_token_http"] = c
c, cr = post(f"{BASE}/v1/projects/{pid}/credentials", None, {"Authorization": f"Bearer {t['access_token']}"})
out["fresh_credentials_http"] = c
url = cr["database_url"]
if wrong_pw:
    u = urllib.parse.urlparse(url); bad = u._replace(netloc=f"{u.username}:not-the-password@{u.hostname}")
    url = urllib.parse.urlunparse(bad); out["mutation"] = "password replaced with a wrong value"
host = urllib.parse.urlparse(url).hostname
q = f"SELECT id, run_tag, customer, kind, amount_aud::text FROM {exp['table']} ORDER BY id"
c, res = post(f"https://{host}/sql", json.dumps({"query": q, "params": []}).encode(),
              {"Content-Type": "application/json", "Neon-Connection-String": url, "Neon-Array-Mode": "true"})
out["sql_http"] = c
if c == 200:
    rows = res.get("rows", []); out["row_count"] = len(rows); out["sha256"] = canon(rows)
    c2, agg = post(f"https://{host}/sql", json.dumps({"query": exp["expected_query"], "params": []}).encode(),
                   {"Content-Type": "application/json", "Neon-Connection-String": url, "Neon-Array-Mode": "true"})
    out["summary_query_result"] = [[k, int(n), float(s)] for k, n, s in agg.get("rows", [])]
    ok = out["sha256"] == out["expected_sha256"] and out["row_count"] == len(exp["rows"]) and out["summary_query_result"] == exp["expected_query_result"]
    out["verdict"] = "PASS" if ok else "FAIL"; out["reason"] = "rows, hash and summary match expected" if ok else "rows differ from expected"
else:
    msg = str(res.get("message") or res.get("raw") or res)[:160]
    out["verdict"] = "FAIL"; out["reason"] = f"database refused or table missing: {msg}"; out["row_count"] = 0
print(json.dumps(out))
