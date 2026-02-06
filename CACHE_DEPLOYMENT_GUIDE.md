# Cache Deployment Guide

## Overview

Country detail pages now use **real data** from live APIs, cached for performance. This guide explains how to set up and maintain the cache system in production.

## Initial Setup (Heroku)

After deploying the API, run the aggregation script to populate the cache:

```bash
# Connect to Heroku dyno
heroku run bash --app pharma-intelligence-api

# Inside the dyno, run aggregation
cd /app
python3 scripts/aggregate_country_data.py --all

# Exit
exit
```

**Expected time:**
- AU: ~5 seconds (local PBS JSON files)
- UK: ~30-60 seconds (NHS API queries)
- US: ~60-120 seconds (CMS API queries - when implemented)

## Cache Location

- **Local dev:** `api/cache/*.json`
- **Heroku:** Ephemeral filesystem (resets on dyno restart)

## Production Strategy

### Option 1: On-Demand Refresh (Current)

**Pros:** Simple, no infrastructure changes
**Cons:** Cache lost on dyno restart

Run aggregation manually when needed:
```bash
heroku run python3 scripts/aggregate_country_data.py --all --app pharma-intelligence-api
```

### Option 2: Scheduled Task (Recommended)

Use Heroku Scheduler addon (free tier):

1. Add scheduler addon:
   ```bash
   heroku addons:create scheduler:standard --app pharma-intelligence-api
   ```

2. Configure job:
   - Command: `python3 scripts/aggregate_country_data.py --all`
   - Frequency: Daily at 2:00 AM UTC
   - Dyno size: Standard-1X

3. Verify:
   ```bash
   heroku addons:open scheduler --app pharma-intelligence-api
   ```

### Option 3: Persistent Storage (Advanced)

For true persistence across restarts:

1. **AWS S3 Bucket:**
   - Upload cache files to S3
   - Modify routes.py to read from S3
   - Write aggregation output to S3

2. **Database Storage:**
   - Store aggregated data in PostgreSQL
   - Query from DB instead of JSON files

## Fallback Behavior

If cache is missing or outdated:
- API returns **generated framework data** (consistent but not real)
- No errors shown to users
- Warning logged: `"No cache found for {country}, generating fallback data"`

## Monitoring

Check cache freshness:

```bash
# View last update time
heroku run cat cache/uk_country_data.json --app pharma-intelligence-api | grep last_updated
```

Expected update times:
- AU: Monthly (PBS releases)
- UK: Daily (NHS updates daily)
- US: Quarterly (CMS releases)

## Troubleshooting

### Cache not loading

1. Check file exists:
   ```bash
   heroku run ls -lh cache/ --app pharma-intelligence-api
   ```

2. Validate JSON:
   ```bash
   heroku run python3 -m json.tool cache/uk_country_data.json --app pharma-intelligence-api
   ```

3. Check logs:
   ```bash
   heroku logs --tail --app pharma-intelligence-api | grep cache
   ```

### Aggregation fails

- **Rate limits:** NHS API may throttle. Add delays between requests.
- **Timeouts:** Increase timeout in aggregation script.
- **Missing data:** Some drugs may not return data (e.g., salbutamol in Oct 2025).

### Dyno restarts clear cache

Use Option 2 or 3 above for persistence.

## Data Sources

| Country | Source | Aggregation Time | Real Data? |
|---------|--------|------------------|------------|
| 🇦🇺 AU | PBS via AIHW | ~5s | ✅ Yes (metformin) |
| 🇬🇧 UK | NHS OpenPrescribing | ~60s | ✅ Yes (9 drugs) |
| 🇺🇸 US | CMS Part D | ~120s | 🚧 Planned |
| 🇫🇷 FR | Open Medic | ~30s | 🚧 Planned |
| 🇯🇵 JP | NDB Open Data | ~30s | 🚧 Planned |

## Next Steps

1. ✅ **Immediate:** Deploy with manual cache refresh
2. 🎯 **Week 1:** Add Heroku Scheduler for daily updates
3. 🚀 **Future:** Implement S3 storage for persistence

## Commands Reference

```bash
# Aggregate single country
heroku run python3 scripts/aggregate_country_data.py --country UK --app pharma-intelligence-api

# Aggregate all countries
heroku run python3 scripts/aggregate_country_data.py --all --app pharma-intelligence-api

# Check cache status
heroku run ls -lh cache/ --app pharma-intelligence-api

# View cache file
heroku run cat cache/au_country_data.json --app pharma-intelligence-api

# Monitor logs
heroku logs --tail --app pharma-intelligence-api | grep -E "cache|Aggregat"
```

---

**Note:** Cache files are **not** committed to Git (in `.gitignore`). Each environment generates its own cache from live APIs.
