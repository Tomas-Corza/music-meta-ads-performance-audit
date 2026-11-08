# Music Meta Ads Performance Audit

**Prepared by Tomas Corza** · Portfolio implementation for Case Study #2

A reproducible Python audit tool for identifying how Meta advertising budgets performed across campaigns, countries, and creative assets. The tool summarizes spend, clicks, reported landing-page views, cost per landing-page view, and campaigns with clicks but no reported visits.

This repository is distinct from the [music marketing analytics dashboard](https://github.com/Tomas-Corza/music-marketing-analytics), which combines Meta Ads and Spotify engagement.

## Quick start

```bash
python3 audit.py sample_data/demo_meta_ads.csv --out outputs
python3 -m unittest discover -s tests -v
```

Requires Python 3.10+ and only the standard library. CSV columns: `campaign, country, creative, spend, link_clicks, landing_page_views`. Values should represent matching time windows and attribution definitions. The sample data is entirely fictional.

## Outputs

- `campaign_summary.csv`: spend, clicks, visits and cost per reported visit by campaign
- `country_summary.csv`: same metrics grouped by geography
- `creative_summary.csv`: same metrics grouped by creative
- `tracking_flags.csv`: rows with link clicks but zero reported landing-page views
- `summary.md`: plain-language audit snapshot

## Interpretation and privacy

Meta-reported landing-page visits are not equivalent to confirmed Spotify listeners, saves, or new fans. A zero-visit record flags a measurement or destination issue for investigation; it does not prove that tracking is broken. Avoid comparing datasets with incompatible objectives, attribution windows, or export definitions. Do not publish private artist exports, API tokens, or personally identifying data.

The 2026 results described in Case Study #2 are historical findings, **not** generated from the fictional sample CSV. To reproduce those exact findings, run the tool against authorized, appropriately anonymized exports.

Portfolio: https://tomascorza.me/music-marketing-case-studies-tomas-corza
