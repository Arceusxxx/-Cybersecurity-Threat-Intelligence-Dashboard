import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# ---------- Reference lists ----------
attack_types = [
    "Phishing", "Ransomware", "DDoS", "Malware", "SQL Injection",
    "Insider Threat", "Man-in-the-Middle", "Zero-Day Exploit",
    "Credential Stuffing", "Social Engineering"
]

severities = ["Low", "Medium", "High", "Critical"]
severity_weights = [0.35, 0.30, 0.22, 0.13]

departments = ["Finance", "IT", "HR", "Sales", "Operations", "Legal", "R&D", "Customer Support"]

regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]

statuses = ["Resolved", "In Progress", "Escalated", "Closed - No Action"]
status_weights = [0.55, 0.20, 0.15, 0.10]

analysts = [
    "Pratik Chandra", "Neha Verma", "Arjun Mehta", "Sara Fernandez",
    "Liam O'Connor", "Priya Nair", "Tom Becker", "Wei Zhang"
]

vuln_categories = [
    "Outdated Software", "Weak Password Policy", "Unpatched OS",
    "Misconfigured Firewall", "Open Ports", "Missing Encryption",
    "Third-Party Library Flaw", "Insecure API Endpoint"
]

patch_status = ["Patched", "Pending", "Not Patched", "In Testing"]
patch_weights = [0.45, 0.25, 0.20, 0.10]

cvss_ranges = {"Low": (0.1, 3.9), "Medium": (4.0, 6.9), "High": (7.0, 8.9), "Critical": (9.0, 10.0)}

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)

def random_date():
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))

def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]

# ---------- 1. Incident data ----------
incident_rows = []
n_incidents = 500
for i in range(1, n_incidents + 1):
    date = random_date()
    severity = weighted_choice(severities, severity_weights)
    attack = random.choice(attack_types)
    dept = random.choice(departments)
    region = random.choice(regions)
    status = weighted_choice(statuses, status_weights)

    base_loss = {"Low": 500, "Medium": 5000, "High": 40000, "Critical": 200000}[severity]
    financial_loss = round(base_loss * random.uniform(0.4, 2.2), 2)

    affected_systems = random.randint(1, 45) if severity in ("High", "Critical") else random.randint(1, 10)

    incident_rows.append({
        "Incident_ID": f"INC-{i:04d}",
        "Date": date.strftime("%Y-%m-%d"),
        "Attack_Type": attack,
        "Severity": severity,
        "Department": dept,
        "Region": region,
        "Affected_Systems": affected_systems,
        "Financial_Loss_USD": financial_loss,
        "Status": status,
        "Reported_By": random.choice(analysts),
    })

with open("cyber_incident_data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=incident_rows[0].keys())
    writer.writeheader()
    writer.writerows(incident_rows)

# ---------- 2. Vulnerability data ----------
vuln_rows = []
n_vulns = 350
for i in range(1, n_vulns + 1):
    date = random_date()
    severity = weighted_choice(severities, severity_weights)
    low, high = cvss_ranges[severity]
    cvss = round(random.uniform(low, high), 1)
    category = random.choice(vuln_categories)
    patch = weighted_choice(patch_status, patch_weights)
    dept = random.choice(departments)

    days_to_patch = None
    if patch == "Patched":
        days_to_patch = random.randint(1, 60)

    vuln_rows.append({
        "Vulnerability_ID": f"VULN-{i:04d}",
        "Date_Identified": date.strftime("%Y-%m-%d"),
        "Category": category,
        "Severity": severity,
        "CVSS_Score": cvss,
        "Department": dept,
        "Patch_Status": patch,
        "Days_To_Patch": days_to_patch if days_to_patch is not None else "",
        "Asset_Type": random.choice(["Server", "Workstation", "Network Device", "Application", "Database", "Cloud Instance"]),
    })

with open("cyber_vulnerability_data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=vuln_rows[0].keys())
    writer.writeheader()
    writer.writerows(vuln_rows)

# ---------- 3. Response data ----------
response_rows = []
for i in range(1, n_incidents + 1):
    incident = incident_rows[i - 1]
    incident_date = datetime.strptime(incident["Date"], "%Y-%m-%d")

    detect_minutes = random.randint(2, 720)
    detection_time = incident_date + timedelta(minutes=detect_minutes)

    resolve_hours = {
        "Low": random.uniform(1, 24),
        "Medium": random.uniform(4, 72),
        "High": random.uniform(12, 168),
        "Critical": random.uniform(24, 336),
    }[incident["Severity"]]
    resolution_time = detection_time + timedelta(hours=resolve_hours)

    sla_target_hours = {"Low": 48, "Medium": 24, "High": 12, "Critical": 4}[incident["Severity"]]
    sla_met = "Yes" if resolve_hours <= sla_target_hours * 3 else "No"

    response_rows.append({
        "Incident_ID": incident["Incident_ID"],
        "Detection_Time_Minutes": detect_minutes,
        "Response_Team": random.choice(["SOC Tier 1", "SOC Tier 2", "Incident Response Team", "External Vendor"]),
        "Assigned_Analyst": random.choice(analysts),
        "Resolution_Time_Hours": round(resolve_hours, 2),
        "SLA_Target_Hours": sla_target_hours,
        "SLA_Met": sla_met,
        "Root_Cause_Identified": random.choice(["Yes", "No"]),
        "Post_Incident_Review": random.choice(["Completed", "Pending", "Not Required"]),
    })

with open("cyber_response_data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=response_rows[0].keys())
    writer.writeheader()
    writer.writerows(response_rows)

print(f"Generated {len(incident_rows)} incidents, {len(vuln_rows)} vulnerabilities, {len(response_rows)} response records.")
