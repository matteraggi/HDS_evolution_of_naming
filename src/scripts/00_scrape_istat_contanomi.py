"""
Scrape Italian baby-name rankings (1999-2024) from ISTAT's "contanomi" tool web
service. This is the JSONP endpoint that backs
https://www.istat.it/dati/calcolatori/contanomi/ - discovered by reading the
tool's birthName.js.

The UI only shows top 10-50, but the API's `limit` param isn't hard-capped there.
Requesting very high limits (e.g. 99999) sometimes returns the full distribution
(confirmed for 2023: 25,197 male / 24,126 female names, ~100% of births covered,
no privacy-suppression floor) but returns an empty response for other years -
most likely an unhandled edge case server-side when the requested range exceeds
that year's real record count. Empirically this breaking point is NOT constant
across years (1999 breaks above limit=375, but 2018 already breaks at 375), so
there's no single safe constant to hardcode.

Instead, for each year this script probes a descending ladder of limits and
keeps the first (largest) one that returns data. Most years likely still get
the full distribution; years that don't get the largest slice ISTAT's service
will actually hand back for that year. The ladder is coarse (not a precise
binary search) since exact-max precision doesn't matter for this use case -
getting *a* large, working slice per year does.

Output:
  data/raw/istat/contanomi_raw/list_<year>.json    - raw JSONP response per year
  data/raw/istat/contanomi_raw/manifest.csv        - year, limit_used, male_count,
                                                      female_count, coverage info
  data/raw/istat/istat_contanomi_full.csv          - combined long table:
      year,name,gender,count,percent
"""
import json
import re
import time
import urllib.request
from pathlib import Path

BASE_URL = "https://www.istat.it/wp-content/themes/EGPbs5-child/contanomi/nati/index2022.php"
HEADERS = {"User-Agent": "Mozilla/5.0 (research script; Human Data Science course project)"}
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "istat" / "contanomi_raw"
OUT_CSV = Path(__file__).resolve().parents[2] / "data" / "raw" / "istat" / "istat_contanomi_full.csv"
MANIFEST_CSV = RAW_DIR / "manifest.csv"
REQUEST_DELAY_SECONDS = 1.2
# Descending probe ladder - first value that returns data wins for that year.
LIMIT_LADDER = [99999, 20000, 10000, 5000, 2000, 1000, 500, 375, 300, 250, 200, 150, 100, 50, 25, 10]


def fetch_raw(params: dict) -> str:
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{BASE_URL}?{qs}&callback=callback"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
    time.sleep(REQUEST_DELAY_SECONDS)
    return raw


def parse_jsonp(raw: str):
    # JSONP wrapper name varies by query type (e.g. "callback" vs "callbackY"),
    # so match any leading identifier followed by "(...)" rather than a fixed name.
    match = re.search(r"^\s*\w+\((.*)\);?\s*$", raw, re.S)
    body = match.group(1) if match else ""
    return json.loads(body) if body else None


def fetch_years() -> list:
    return parse_jsonp(fetch_raw({"type": "years"}))


def fetch_list_for_year(year: int):
    """
    Find the largest working `limit` for this year in two passes:
    1. Coarse ladder to quickly bracket [last success, first failure].
    2. Binary search inside that bracket for the exact max (the ladder's round
       numbers can under-shoot the real per-year ceiling by 20-30%, confirmed
       for 2018/2021 during exploration).
    """
    good_limit, good_data = None, None
    bad_limit = None
    for limit in LIMIT_LADDER:
        data = parse_jsonp(fetch_raw({"type": "list", "limit": limit, "year": year}))
        if data is not None:
            good_limit, good_data = limit, data
            break
        bad_limit = limit
        print(f"  {year}: limit={limit} empty, trying smaller")
    if good_limit is None:
        raise RuntimeError(f"No working limit found for year {year}, even at the floor of {LIMIT_LADDER[-1]}")
    if bad_limit is None:
        # first (largest) rung already worked - that's the true max, nothing above it to search
        return good_data, good_limit

    lo, hi = good_limit + 1, bad_limit - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        data = parse_jsonp(fetch_raw({"type": "list", "limit": mid, "year": year}))
        if data is not None:
            good_limit, good_data = mid, data
            lo = mid + 1
        else:
            hi = mid - 1
    return good_data, good_limit


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    years = fetch_years()
    print(f"Available years: {years[0]}-{years[-1]} ({len(years)} years)")

    manifest_rows = []
    rows = []
    for year in years:
        cache_path = RAW_DIR / f"list_{year}.json"
        limit_used = None
        if cache_path.exists():
            data = json.loads(cache_path.read_text(encoding="utf-8"))
            print(f"{year}: using cached response (male={len(data.get('0', []))}, female={len(data.get('1', []))})")
        else:
            data, limit_used = fetch_list_for_year(year)
            cache_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            print(
                f"{year}: fetched at limit={limit_used}, male={len(data.get('0', []))}, "
                f"female={len(data.get('1', []))}"
            )

        male = data.get("0", [])
        female = data.get("1", [])
        manifest_rows.append(
            {
                "year": year,
                "limit_used": limit_used if limit_used is not None else "cached",
                "male_count": len(male),
                "female_count": len(female),
                "male_percent_sum": round(sum(x["percent"] for x in male), 4) if male else 0,
                "female_percent_sum": round(sum(x["percent"] for x in female), 4) if female else 0,
            }
        )
        rows.extend(male)
        rows.extend(female)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        f.write("year,name,gender,count,percent\n")
        for r in rows:
            name = r["name"].replace('"', "'")
            f.write(f'{r["year"]},"{name}",{r["gender"]},{r["count"]},{r["percent"]}\n')
    print(f"\nWrote {len(rows)} rows to {OUT_CSV}")

    with MANIFEST_CSV.open("w", encoding="utf-8", newline="") as f:
        f.write("year,limit_used,male_count,female_count,male_percent_sum,female_percent_sum\n")
        for m in manifest_rows:
            f.write(
                f"{m['year']},{m['limit_used']},{m['male_count']},{m['female_count']},"
                f"{m['male_percent_sum']},{m['female_percent_sum']}\n"
            )
    print(f"Wrote manifest to {MANIFEST_CSV}")
    print(
        "\nNote: 'male_percent_sum'/'female_percent_sum' close to 100 means that year's "
        "slice is (near) the complete distribution; well below 100 means only the top "
        "names by rank were captured for that year - check manifest.csv before treating "
        "coverage as uniform across years."
    )


if __name__ == "__main__":
    main()
