"""Audits aggregated Meta Ads CSV data; standard library only."""
import argparse
import csv
from collections import defaultdict
from pathlib import Path

REQUIRED = {"campaign", "country", "creative", "spend", "link_clicks", "landing_page_views"}

def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
        rows = []
        for n, row in enumerate(reader, 2):
            try:
                parsed = {key: (row[key] or "").strip() for key in ("campaign", "country", "creative")}
                for col in ("spend", "link_clicks", "landing_page_views"):
                    parsed[col] = float(row[col])
                    if parsed[col] < 0:
                        raise ValueError("negative value")
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid numeric value on row {n}: {exc}") from exc
            rows.append(parsed)
    return rows

def aggregate(rows, dimension):
    grouped = defaultdict(lambda: {"spend": 0.0, "link_clicks": 0.0, "landing_page_views": 0.0})
    for row in rows:
        values = grouped[row[dimension]]
        for field in values:
            values[field] += row[field]
    output = []
    for name, values in sorted(grouped.items()):
        spend, visits = values["spend"], values["landing_page_views"]
        output.append({dimension: name, **{k: round(v, 2) for k, v in values.items()},
                       "cost_per_landing_page_view": round(spend / visits, 4) if visits else ""})
    return output

def write_csv(path, rows, cols):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=cols)
        writer.writeheader()
        writer.writerows(rows)

def audit(input_file, outdir):
    rows = read_rows(input_file)
    if not rows:
        raise ValueError("CSV contains no data rows")
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    metrics = ["spend", "link_clicks", "landing_page_views", "cost_per_landing_page_view"]
    for dimension in ("campaign", "country", "creative"):
        write_csv(outdir / f"{dimension}_summary.csv", aggregate(rows, dimension), [dimension, *metrics])
    flags = [r for r in rows if r["link_clicks"] > 0 and r["landing_page_views"] == 0]
    write_csv(outdir / "tracking_flags.csv", flags, ["campaign", "country", "creative", "spend", "link_clicks", "landing_page_views"])
    spend = sum(r["spend"] for r in rows)
    clicks = sum(r["link_clicks"] for r in rows)
    visits = sum(r["landing_page_views"] for r in rows)
    report = ("# Advertising audit snapshot\n\n"
              f"- Recorded advertising spend: ${spend:,.2f}\n"
              f"- Meta-reported link clicks: {clicks:,.0f}\n"
              f"- Meta-reported landing-page views: {visits:,.0f}\n"
              f"- Cost per reported landing-page view: ${spend/visits:.3f}\n" if visits else
              "# Advertising audit snapshot\n\nNo reported landing-page visits; cost per visit is undefined.\n")
    report += f"- Rows with clicks but zero reported landing-page views: {len(flags)}\n\n"
    report += "**Caution:** These are Meta-reported traffic metrics, not confirmed streams, saves, or customers.\n"
    (outdir / "summary.md").write_text(report, encoding="utf-8")
    return len(rows), len(flags)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit aggregated Meta Ads performance exports")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--out", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    count, flagged = audit(args.csv_file, args.out)
    print(f"Analyzed {count} rows. Flagged {flagged} rows for review. Reports: {args.out}")
