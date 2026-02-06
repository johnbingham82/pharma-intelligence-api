# Country Data Cache

This directory contains pre-aggregated country-level data sourced from live APIs.

## Purpose

Country detail pages (`/country/{code}`) serve data from these cache files for fast response times and reduced API load.

## Cache Files

- `au_country_data.json` - Australia (PBS real data)
- `uk_country_data.json` - United Kingdom (NHS OpenPrescribing)
- `us_country_data.json` - United States (CMS Medicare Part D)
- `fr_country_data.json` - France (Open Medic)
- `jp_country_data.json` - Japan (NDB Open Data)

## Updating Cache

### Manual Update

```bash
# Single country
python3 scripts/aggregate_country_data.py --country AU

# All countries
python3 scripts/aggregate_country_data.py --all
```

### Automated Updates

Set up a cron job to refresh data:

```bash
# Daily at 2 AM
0 2 * * * cd /path/to/api && python3 scripts/aggregate_country_data.py --all
```

## Cache Structure

Each file contains:

```json
{
  "country": "AU",
  "last_updated": "2026-02-06T11:00:00Z",
  "period": "2025-06",
  "regions": [
    {
      "region": "New South Wales",
      "prescriptions": 250000,
      "cost": 8000000,
      "prescribers": 1500
    }
  ],
  "top_drugs": [
    {
      "name": "Metformin",
      "prescriptions": 776721,
      "cost": 24994613
    }
  ],
  "monthly_data": [...],
  "metadata": {
    "source": "PBS - AIHW",
    "update_frequency": "Monthly"
  }
}
```

## Data Sources

| Country | Source | Update Freq | Level |
|---------|--------|-------------|-------|
| AU | PBS via AIHW | Monthly | State |
| UK | NHS OpenPrescribing | Daily | Practice |
| US | CMS Part D | Quarterly | Prescriber |
| FR | Open Medic / SNDS | Annual | Regional |
| JP | NDB Open Data | Annual | Prefecture |

## Notes

- Cache files are **not** committed to Git (in `.gitignore`)
- Each deployment environment should generate its own cache
- If cache is missing, API falls back to generated/framework data
- Cache update time depends on country:
  - AU: ~5 seconds (local JSON files)
  - UK: ~30-60 seconds (NHS API queries)
  - US: ~60-120 seconds (CMS API queries)
