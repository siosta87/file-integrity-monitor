# Automated Security Log Analyzer with Geo-IP

A lightweight Python-based security information and event parsing tool developed to showcase threat detection engineering, regular expression pattern matching, threshold alerting, and Geo-IP enrichment capabilities for cybersecurity portfolios.

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [System Architecture & Workflow](#system-architecture--workflow)
4. [Project Structure](#project-structure)
5. [Prerequisites & Setup](#prerequisites-setup)
6. [How to Run](#how-to-run)
7. [Sample Output & SIEM Reporting](#sample-output--siem-reporting)
8. [Corporate Safety & Compliance](#corporate-safety--compliance)

---

## 🔎 Overview

In modern Security Operations Centers (SOC), analysts rely on Security Information and Event Management (SIEM) platforms to parse authentication logs, track brute-force attacks, and identify unauthorized privilege escalation. 

This project simulates that exact triage pipeline entirely in user-space using pure Python. It reads simulated authentication telemetry, applies regular expressions to extract Indicators of Compromise (IoCs), enriches source IP addresses with threat intelligence geolocation context, and exports a structured JSON report suitable for upstream SIEM integration.

---

## ⚡ Key Features

* **Regex Pattern Matching:** Employs precise regular expressions to parse timestamps, usernames, event states, source IP addresses, and executed shell commands from raw log streams.
* **Brute-Force Attack Detection:** Tracks failed authentication frequency using frequency counting algorithms, flagging source IPs that breach configurable failure thresholds.
* **Privilege Escalation Tracking:** Monitors command execution strings for high-privilege activities (such as `sudo` or `su -`) performed by standard users.
* **Geo-IP Threat Intelligence Context:** Integrates live secure HTTPS queries (`ipapi.co`) with an intelligent offline local fallback dictionary to provide country, city, and organization attribution without failing behind corporate proxies.
* **Structured SIEM Reporting:** Generates automated, machine-readable JSON security reports (`security_report.json`) for downstream incident response playbooks.

---

## 🛠️ System Architecture & Workflow

1. **Ingestion Layer:** Reads raw text log files (`auth_mock.log`) line-by-line.
2. **Parsing Engine:** Evaluates each line against compiled regex patterns to categorize events into `LOGIN_FAILED`, `LOGIN_SUCCESS`, or `COMMAND_EXEC`.
3. **Analysis & Enrichment:** Aggregates failed login attempts per source IP and cross-references them against a sliding threshold. Enriches flagged IPs with geographical and organizational metadata.
4. **Reporting Layer:** Prints formatted, color-coded console alerts for real-time analyst visibility and writes out a structured JSON threat report.

---

## 📁 Project Structure

```text
auth_mock/
│
├── log_analyzer.py        # Main Python threat detection and enrichment engine
├── auth_mock.log          # Simulated authentication log telemetry
└── security_report.json   # Exported machine-readable SIEM alert payload
```

---

## ⚙️ Prerequisites & Setup

* **Python 3.x** installed on your workstation.
* No external pip packages required (runs entirely on Python standard libraries: `re`, `collections`, `json`, `urllib.request`).

---

## 🚀 How to Run

1. Clone or download this repository into your local directory.
2. Ensure both `log_analyzer.py` and `auth_mock.log` are located in the same folder.
3. Open your terminal and execute the script:
   ```bash
   python3 log_analyzer.py
   ```

---

## 📊 Sample Output & SIEM Reporting

When executed against the mock log file, the analyzer outputs structured diagnostic telemetry:

```text
======================================================================
🛡️  ENHANCED SECURITY LOG ANALYSIS REPORT (WITH GEO-IP CONTEXT)
======================================================================

[!] Scanning for Brute-Force Activity...
⚠️  ALERT: Potential Brute-Force detected from IP: 185.72.33.10 
    └─ Source Count: 5 failed attempts
    └─ Geolocation: Moscow, Russia (Malicious Host Inc.)

[!] Scanning for Suspicious Privileged Activity...
⚠️  ALERT: High-privilege command run by 'admin_user'!
    └─ Command: sudo su -
    └─ Source Host: 192.168.1.12 [Google Corp LAN]

[+] Structured SIEM context report saved to 'security_report.json'
```

---

## 🛡️ Corporate Safety & Compliance

This tool was intentionally designed with secure sandbox constraints:
* **In-Memory & Simulated Data:** Operates strictly on local synthetic text files (`auth_mock.log`). It never parses actual host system logs (`/var/log/system.log` or Windows Event Logs).
* **Standard Libraries Only:** Avoids third-party networking libraries (`scapy`, `paramiko`) to prevent triggering corporate Endpoint Detection and Response (EDR) compliance alerts.
* **No Active Sockets:** Uses safe, passive parsing and standard HTTPS REST GET queries with built-in timeouts, avoiding raw socket port probing.
