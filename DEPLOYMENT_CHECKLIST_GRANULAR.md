# Deployment Checklist - Granular Geographic Boundaries

## ✅ Pre-Deployment (Local Testing)

- [x] Postcode geocoding module working (100% accuracy)
- [x] LA aggregation script created
- [ ] **Aggregation complete** (~51% done, waiting...)
- [ ] Verify cache files exist:
  - [ ] `api/cache/uk_local_authority_data.json`
  - [ ] `api/cache/uk_practice_locations.json`
  - [ ] `api/cache/postcode_cache.json` (755KB+)
- [ ] Test LA API endpoint locally:
  ```bash
  curl http://localhost:8000/api/country/UK/local-authorities
  ```
- [ ] Test frontend granularity toggle locally

## 📦 Files to Deploy

### Backend (Heroku):
```
api/postcode_geocoding.py              # NEW
api/ccg_to_la_mapping.py               # NEW (unused but included)
api/scripts/aggregate_country_data.py  # MODIFIED
api/routes.py                           # MODIFIED (+1 endpoint)
api/cache/uk_local_authority_data.json  # NEW (wait for aggregation)
api/cache/uk_practice_locations.json    # NEW (wait for aggregation)
api/cache/postcode_cache.json           # NEW (optional - can rebuild)
```

### Frontend (AWS Amplify):
```
frontend/src/components/GeographicHeatMap.tsx  # MODIFIED
frontend/src/pages/CountryDetail.tsx            # MODIFIED
frontend/public/geojson/uk-local-authorities.json  # NEW
```

## 🚀 Deployment Steps

### 1. Wait for Aggregation to Complete
```bash
# Check progress
python3 -c "
import json
with open('api/cache/postcode_cache.json') as f:
    cache = json.load(f)
full_count = sum(1 for k in cache if k.startswith('full_'))
print(f'{full_count} / ~6700 ({full_count/6700*100:.1f}%)')
"

# Check if LA data file exists
ls -lh api/cache/uk_local_authority_data.json
```

### 2. Test Locally

**Backend:**
```bash
cd /Users/administrator/.openclaw/workspace/api
uvicorn main:app --reload --port 8000

# Test LA endpoint
curl http://localhost:8000/api/country/UK/local-authorities | jq '.local_authorities | length'
```

**Frontend:**
```bash
cd /Users/administrator/.openclaw/workspace/frontend
npm run dev

# Visit: http://localhost:3000/country/UK
# Toggle: Regions → Local Auth. (150+)
# Verify: Map reloads with more granular boundaries
```

### 3. Git Commit & Push

```bash
cd /Users/administrator/.openclaw/workspace

# Add new files
git add api/postcode_geocoding.py
git add api/ccg_to_la_mapping.py
git add api/cache/uk_local_authority_data.json
git add api/cache/uk_practice_locations.json
git add frontend/public/geojson/uk-local-authorities.json

# Add modified files
git add api/scripts/aggregate_country_data.py
git add api/routes.py
git add frontend/src/components/GeographicHeatMap.tsx
git add frontend/src/pages/CountryDetail.tsx

# Add documentation
git add GRANULAR_GEOCODING_SUMMARY.md
git add GRANULAR_BOUNDARIES_PLAN.md
git add DEPLOYMENT_CHECKLIST_GRANULAR.md

# Commit
git commit -m "feat: Add granular LA boundaries + postcode geocoding for UK

- 100% accurate postcode-based geocoding (NHS ODS + postcodes.io)
- 150+ Local Authority boundaries (vs 7 regions)
- 6,700+ GP practice locations with lat/lng
- New API endpoint: /country/{code}/local-authorities
- Frontend granularity toggle UI
- Persistent geocoding cache

Phase 1 complete. Practice point markers ready for Phase 2."

# Push to trigger deployments
git push origin main        # → AWS Amplify (frontend)
git push heroku main        # → Heroku (backend)
```

### 4. Monitor Deployments

**Frontend (AWS Amplify):**
- Auto-deploys on push to main
- Check: https://intelligence.clarion.co.uk
- Time: ~3 minutes

**Backend (Heroku):**
- Auto-deploys on push to heroku main
- Check: https://pharma-intelligence-api-ee752ce1773a.herokuapp.com/api/docs
- Time: ~5 minutes

### 5. Verify Production

**API Endpoint:**
```bash
curl https://pharma-intelligence-api-ee752ce1773a.herokuapp.com/api/country/UK/local-authorities | jq '.local_authorities | length'

# Expected: ~150
```

**Frontend:**
1. Visit: https://intelligence.clarion.co.uk/country/UK
2. Toggle: "Regions (7)" → "Local Auth. (150+)"
3. Verify: Map shows more granular boundaries
4. Verify: Table shows top 20 LAs

### 6. Cache Management (Heroku)

**Note:** Heroku dynos have ephemeral filesystem!

**Option A: Keep cache in Git (Recommended for now)**
- ✅ Cache persists across deploys
- ✅ No need to re-aggregate
- ❌ Git repo grows (755KB postcode cache)

**Option B: Rebuild cache on deploy**
- Add build step to `Procfile`:
  ```
  release: python api/scripts/aggregate_country_data.py --country UK --granular
  ```
- ❌ Adds 11-12 minutes to each deploy
- ✅ Keeps Git repo small

**Option C: Use S3/persistent storage (Future)**
- Store cache in S3
- Load from S3 on startup
- ✅ Best of both worlds
- ❌ Requires AWS setup

**Decision:** Use Option A for now (cache in Git). If repo size becomes an issue, move to Option C.

## ✅ Post-Deployment Checks

- [ ] Frontend loads without errors
- [ ] UK country page shows granularity toggle
- [ ] Switching to "Local Auth" loads new boundaries
- [ ] Map displays correctly at LA granularity
- [ ] Table shows top 20 LAs
- [ ] API endpoint returns LA data
- [ ] No console errors in browser

## 🐛 Rollback Plan

If issues arise:
```bash
git revert HEAD
git push origin main
git push heroku main
```

Or redeploy previous working commit:
```bash
git push heroku <previous-commit-sha>:main --force
```

## 📈 Success Metrics

After deployment, verify:
- Users can toggle between Regions and Local Authorities
- LA-level data loads quickly (<2s)
- Map renders correctly with granular boundaries
- No performance degradation

## 🎯 Phase 2 Tasks (Future)

Once deployed and stable:
1. Add practice point markers overlay
2. Add Australia LGA boundaries
3. Add US county-level boundaries
4. Implement marker clustering for practices
5. Add filtering by prescription volume

---

**Current Status:** Waiting for aggregation to complete (~51% done)

**Next:** Test locally → Git commit → Push → Monitor deployments
