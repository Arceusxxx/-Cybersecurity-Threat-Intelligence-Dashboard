# 🛡️ Cybersecurity Threat Intelligence & Incident Analysis Dashboard

**By Pratik Chandra**

## 📌 Project Overview

An interactive Cybersecurity Incident & Threat Intelligence Dashboard, built for Power BI, that analyzes security incidents, vulnerabilities, response performance, and financial impact to give decision-makers a single, actionable view of organizational security posture.

The dataset (500 incidents, 350 vulnerabilities, 500 response records, Jan 2024 – Dec 2025) is synthetic but structured the way a real SOC data model would be — three linked fact tables joined on `Incident_ID`.

## 🎯 Objectives

1. Monitor cybersecurity incidents over time
2. Analyze attack types and severity levels
3. Track financial losses caused by incidents
4. Evaluate patch management and vulnerability status
5. Measure incident response performance against SLA

## 🗂️ Data Model

| File | Grain | Key fields |
|---|---|---|
| `cyber_incident_data.csv` | one row per incident | Incident_ID, Date, Attack_Type, Severity, Department, Region, Financial_Loss_USD, Status |
| `cyber_vulnerability_data.csv` | one row per vulnerability | Vulnerability_ID, Category, Severity, CVSS_Score, Patch_Status, Days_To_Patch |
| `cyber_response_data.csv` | one row per incident (1:1 with incidents) | Incident_ID, Detection_Time_Minutes, Resolution_Time_Hours, SLA_Target_Hours, SLA_Met |

Relationship: `cyber_incident_data[Incident_ID]` (1) → `cyber_response_data[Incident_ID]` (1). Vulnerability data relates via shared `Department` and `Severity` dimensions.

## 📐 Key DAX Measures

```dax
Total Incidents = COUNTROWS(cyber_incident_data)

Total Financial Loss =
SUM(cyber_incident_data[Financial_Loss_USD])

Critical Incident % =
DIVIDE(
    CALCULATE(COUNTROWS(cyber_incident_data), cyber_incident_data[Severity] = "Critical"),
    [Total Incidents]
)

SLA Compliance % =
DIVIDE(
    CALCULATE(COUNTROWS(cyber_response_data), cyber_response_data[SLA_Met] = "Yes"),
    COUNTROWS(cyber_response_data)
)

Avg Resolution Time (hrs) =
AVERAGE(cyber_response_data[Resolution_Time_Hours])

Severity Risk Score =
SUMX(
    cyber_incident_data,
    SWITCH(
        cyber_incident_data[Severity],
        "Low", 1,
        "Medium", 3,
        "High", 7,
        "Critical", 10,
        0
    )
)

Patch Compliance % =
DIVIDE(
    CALCULATE(COUNTROWS(cyber_vulnerability_data), cyber_vulnerability_data[Patch_Status] = "Patched"),
    COUNTROWS(cyber_vulnerability_data)
)

Incidents MoM Change =
VAR CurrentMonth = [Total Incidents]
VAR PriorMonth = CALCULATE([Total Incidents], DATEADD('Date'[Date], -1, MONTH))
RETURN DIVIDE(CurrentMonth - PriorMonth, PriorMonth)
```

## 📊 Suggested Report Pages

- **Executive Summary** — KPI cards (Total Incidents, Financial Loss, Critical %, SLA Compliance), incident trend line, severity donut
- **Threat Analysis** — attack type breakdown, severity risk score by department/region, drill-through to incident detail
- **Vulnerability & Patch Management** — CVSS distribution, patch status funnel, days-to-patch by category
- **Response Performance** — detection vs. resolution time, SLA compliance by team, root-cause tracking

## 🖥️ Included Files

- `cyber_incident_data.csv`, `cyber_vulnerability_data.csv`, `cyber_response_data.csv` — source data, ready to import into Power BI (Get Data → Text/CSV)
- `dashboard.html` — a standalone interactive preview of the dashboard (open directly in a browser) since the source data hasn't been assembled into a `.pbix` yet
- `generate_data.py` — script used to generate the synthetic dataset (adjust and re-run for different volumes/date ranges)

## 🔧 Building the .pbix

1. Open Power BI Desktop → **Get Data** → **Text/CSV** → import all three files
2. In **Model view**, create the `Incident_ID` relationship between the incident and response tables
3. Add a **Date** dimension table (Power Query → New Source → Blank Query, or `CALENDAR()` in DAX) and mark it as the date table
4. Paste in the DAX measures above under a new **Measures** table
5. Build report pages per the suggested layout, using slicers for Date, Severity, Region, and Department

## ✅ Conclusion

The Cybersecurity Threat Intelligence Dashboard gives a comprehensive view of organizational security posture by integrating incident data, vulnerability metrics, and response performance analytics into a single interactive Power BI solution — surfacing where risk concentrates, how fast the team responds, and where patch management is falling behind.
