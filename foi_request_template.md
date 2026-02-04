# FREEDOM OF INFORMATION (FOI) REQUEST TEMPLATE
## CDK4/6 Inhibitor Formulary Intelligence

---

## 📋 ABOUT FOI REQUESTS

**What is FOI?**
- Freedom of Information Act 2000 gives public right to access information from public authorities
- NHS trusts MUST respond within 20 working days
- They can only refuse if information is commercially sensitive or patient-identifiable

**Why Use FOI for Formulary Intelligence?**
- ✅ Legal right to this information
- ✅ Systematic approach (can batch-submit to 50 trusts)
- ✅ Written response (documented evidence)
- ✅ No reliance on MSL relationships

---

## ✉️ FOI REQUEST TEMPLATE

**Subject:** Freedom of Information Request - CDK4/6 Inhibitor Formulary Status

**To:** foi@[trustdomain].nhs.uk

**Body:**

```
Dear Freedom of Information Team,

I am writing to make a request under the Freedom of Information Act 2000.

REQUEST:

Please provide information regarding the formulary status of CDK4/6 inhibitors 
(palbociclib, ribociclib, and abemaciclib) at [Trust Name].

Specifically, I request:

1. Are the following drugs currently listed on your trust formulary?
   - Palbociclib (Ibrance)
   - Ribociclib (Kisqali)
   - Abemaciclib (Verzenio)

2. For each drug that is listed, please indicate:
   - First-line choice
   - Alternative/second-line choice
   - Restricted use (please specify restrictions)
   - Not listed on formulary

3. If any of these drugs are subject to special approval processes 
   (e.g., prior authorization, consultant-only prescribing, formulary 
   committee approval), please describe these requirements.

4. Approximate annual expenditure on each CDK4/6 inhibitor at your trust 
   (if this information is readily available).

5. Date of last formulary review for this drug class.

I understand that under the Act, I should receive a response within 20 working days.

If any part of this request is unclear, or if you require clarification, 
please contact me.

If you are unable to provide all the information requested, please provide 
as much as you are able to disclose.

Thank you for your assistance.

Yours faithfully,
[Your Name]
[Your Organization]
[Contact Email]
```

---

## 🎯 TARGET TRUSTS FOR FOI BATCH

### **Batch 1: Priority Cancer Centers (10 trusts)**

| Trust Name | FOI Email | Code |
|------------|-----------|------|
| Royal Marsden NHS FT | foi@rmh.nhs.uk | RPY |
| The Christie NHS FT | foi@christie.nhs.uk | RM2 |
| UCLH NHS FT | foi@uclh.nhs.uk | RRV |
| Guy's and St Thomas' NHS FT | foi@gstt.nhs.uk | RJ1 |
| Cambridge University Hospitals NHS FT | foi@addenbrookes.nhs.uk | RGT |
| Imperial College Healthcare NHS Trust | foi@imperial.nhs.uk | RYJ |
| Manchester University NHS FT | foi@mft.nhs.uk | R0A |
| Oxford University Hospitals NHS FT | foi.office@ouh.nhs.uk | RTH |
| King's College Hospital NHS FT | kch-tr.foi@nhs.net | RJZ |
| Royal Free London NHS FT | rf.foi@nhs.net | RAL |

### **Batch 2: Major Regional Centers (10 trusts)**

| Trust Name | Code |
|------------|------|
| Leeds Teaching Hospitals NHS Trust | RR8 |
| Newcastle upon Tyne Hospitals NHS FT | RTD |
| University Hospitals Birmingham NHS FT | RRK |
| Nottingham University Hospitals NHS Trust | RX1 |
| University Hospitals Bristol and Weston NHS FT | RA7 |
| Sheffield Teaching Hospitals NHS FT | RHQ |
| Liverpool University Hospitals NHS FT | REM |
| University Hospitals of Leicester NHS Trust | RWE |
| University Hospitals Southampton NHS FT | RHM |
| Cardiff and Vale University Health Board | 7A4 |

---

## 📊 TRACKING SPREADSHEET

**Create a tracking sheet with these columns:**

| Trust Name | FOI Sent Date | Response Due Date | Response Received | Ibrance Status | Kisqali Status | Verzenio Status | Notes |
|------------|---------------|-------------------|-------------------|----------------|----------------|-----------------|-------|
| Royal Marsden | 2026-02-04 | 2026-03-04 | | | | | |
| The Christie | 2026-02-04 | 2026-03-04 | | | | | |
| ... | | | | | | | |

---

## ⚖️ LEGAL NOTES

**Trust Obligations:**
- Must respond within 20 working days
- Can request clarification (extends timeline)
- Can refuse if: commercially sensitive, patient-identifiable, excessive cost (>£450)
- Must provide reason if refusing

**Your Rights:**
- Can appeal refusals to Information Commissioner's Office (ICO)
- Can request internal review if unsatisfied
- Information is typically disclosed (formulary status is standard request)

**Expected Disclosure Rate:**
- 70-80% of trusts will fully comply
- 10-20% will partially comply (some fields redacted)
- 5-10% will refuse (rare for formulary queries)

---

## 🤖 AUTOMATED FOI SUBMISSION (OpenClaw Implementation)

**For production, automate the process:**

```python
# Pseudo-code for automated FOI submission

def submit_foi_batch(trusts, template):
    for trust in trusts:
        email = generate_foi_email(trust, template)
        send_email(to=trust['foi_email'], subject=email['subject'], body=email['body'])
        
        # Track submission
        log_foi_submission(
            trust=trust['name'],
            sent_date=today(),
            due_date=today() + 20_working_days,
            status='Awaiting response'
        )
        
        # Set reminder
        schedule_reminder(
            date=today() + 15_working_days,
            message=f"FOI response due in 5 days: {trust['name']}"
        )
```

**Cron job setup:**
- Day 15: Reminder to check response
- Day 21: Alert if no response (follow-up required)
- Day 30: Escalation to ICO if still no response

---

## 📈 EXPECTED RESULTS

**After 8 weeks (20-day response + 2-3 weeks buffer):**

✅ **20-25 trusts with complete formulary data**
- Exact positioning: First-line vs alternative
- Restrictions/approval requirements
- Competitive comparison (Kisqali vs Ibrance vs Verzenio)

✅ **10-15 trusts with partial data**
- Some fields redacted
- General positioning indicated

❌ **5-10 trusts non-responsive or refusal**
- Follow up via MSL field intelligence
- Or escalate to ICO

**Net result:** 70-80% intelligence coverage across 50 major trusts

---

## 💡 COMBINING FOI + MSL INTELLIGENCE

**Best approach: Dual-track**

**Track 1: FOI Requests (Legal/Formal)**
- Batch submit to 50 trusts
- 8-week timeline
- Written documentation
- Good for: Official formulary status

**Track 2: MSL Field Intelligence (Relationship)**
- Concurrent with FOI
- 4-6 week timeline
- Qualitative insights
- Good for: KOL preferences, "why" behind formulary decisions

**Together:** Complete picture in 8 weeks
- FOI = "What is on formulary?"
- MSL = "Why? And what do prescribers actually use?"

---

## 🎯 NEXT STEP: EXECUTE

**This Week:**
1. Copy FOI template
2. Customize with your organization details
3. Find FOI email addresses for 10 priority trusts
4. Send batch submission
5. Set up tracking spreadsheet
6. Calendar reminder for Day 15 follow-ups

**Cost:** £0 (FOI requests are free)  
**Time:** 2-3 hours to prepare and submit batch  
**Expected Intelligence:** 70-80% formulary coverage in 8 weeks  

**Value:** Know exactly where Kisqali needs formulary positioning work vs where it's already competitive with Ibrance.

---

**Ready to submit?** This is how you get REAL formulary intelligence that web scraping can't provide.
