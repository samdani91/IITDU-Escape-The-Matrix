# EML Email Forensic Analysis
### Linux / Kali Linux SOC Investigation Command Reference

**Prepared by:** Zaber Mahmud  
**Organization:** EWU Cybersecurity Club (EWUCSC)  
**Focus:** SOC • Email Forensics • Phishing Analysis • Threat Intelligence • IOC Extraction

---

> **Technical Reference**
>
> This document is prepared as a practical command-line reference for analyzing suspicious `.eml` email files using Linux/Kali Linux in a controlled security-analysis environment.

**Author:** Zaber Mahmud  
**EWU Cybersecurity Club (EWUCSC)**  
**Date:** 19 August 2026

---

## 1. Basic File Inspection

```bash
file suspicious.eml
ls -lh suspicious.eml
cat suspicious.eml
less suspicious.eml
```

---

## 2. Extract Email Headers

```bash
grep -Eai '^(From|To|Cc|Date|Subject|Reply-To|Return-Path|Message-ID|Received|Authentication-Results|DKIM-Signature|Received-SPF):' suspicious.eml
```

Show the complete header section:

```bash
sed '/^$/q' suspicious.eml
```

Important headers to review:

- `From`
- `To`
- `Cc`
- `Reply-To`
- `Return-Path`
- `Subject`
- `Date`
- `Message-ID`
- `Received`
- `Authentication-Results`
- `DKIM-Signature`
- `Received-SPF`

---

## 3. Analyze the Received Chain

```bash
grep -Eai '^Received:' suspicious.eml
```

Show `Received` headers with continuation lines:

```bash
awk 'BEGIN{IGNORECASE=1} /^Received:/{p=1} /^[^ \t].*:/{if($0 !~ /^Received:/) p=0} p' suspicious.eml
```

Look for:

- Sending server
- Relay servers
- Source IP
- Hostnames
- Timestamps
- Suspicious mail infrastructure

---

## 4. Extract IP Addresses

```bash
grep -Eo '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' suspicious.eml | sort -u
```

Show surrounding context:

```bash
grep -Ein -C 3 -E '([0-9]{1,3}\.){3}[0-9]{1,3}' suspicious.eml
```

---

## 5. Extract Domains

```bash
grep -Eo '([A-Za-z0-9-]+\.)+[A-Za-z]{2,}' suspicious.eml | sort -fu
```

---

## 6. Extract URLs

```bash
grep -Eo 'https?://[^[:space:]<>"()]+' suspicious.eml | sort -u
```

Search for URL-related HTML:

```bash
grep -Ein 'https?://|www\.|href=|url=' suspicious.eml
```

---

## 7. SPF Analysis

```bash
grep -Eai 'spf|received-spf' suspicious.eml
```

Check specifically for:

```bash
grep -Eai '^Received-SPF:' suspicious.eml
```

Look for:

- `pass`
- `fail`
- `softfail`
- `neutral`
- `none`
- `temperror`
- `permerror`

---

## 8. DKIM Analysis

```bash
grep -Eai 'dkim|dkim-signature' suspicious.eml
```

Specifically:

```bash
grep -Eai '^DKIM-Signature:' suspicious.eml
```

Look for:

- `d=`
- `s=`
- `bh=`
- `b=`

---

## 9. DMARC / Authentication Analysis

```bash
grep -Eai 'dmarc|authentication-results' suspicious.eml
```

Combined authentication check:

```bash
grep -Eai 'authentication-results|received-spf|dkim-signature|dmarc' suspicious.eml
```

Look for:

```text
spf=pass
spf=fail
dkim=pass
dkim=fail
dmarc=pass
dmarc=fail
```

---

## 10. Parse the EML Using Python

Python's standard `email` module can parse the message without executing attachments.

```bash
python3 - <<'PY'
from email import policy
from email.parser import BytesParser

with open("suspicious.eml", "rb") as f:
    msg = BytesParser(policy=policy.default).parse(f)

print("From:", msg.get("From"))
print("To:", msg.get("To"))
print("Cc:", msg.get("Cc"))
print("Reply-To:", msg.get("Reply-To"))
print("Return-Path:", msg.get("Return-Path"))
print("Subject:", msg.get("Subject"))
print("Date:", msg.get("Date"))
print("Message-ID:", msg.get("Message-ID"))

print("\nContent-Type:", msg.get_content_type())

print("\nParts:")
for i, part in enumerate(msg.walk()):
    print(
        i,
        "|",
        part.get_content_type(),
        "|",
        part.get_filename(),
        "|",
        part.get("Content-Transfer-Encoding")
    )
PY
```

---

## 11. List Attachments

```bash
python3 - <<'PY'
from email import policy
from email.parser import BytesParser

with open("suspicious.eml", "rb") as f:
    msg = BytesParser(policy=policy.default).parse(f)

for part in msg.iter_attachments():
    print(
        "Filename:",
        part.get_filename(),
        "| Type:",
        part.get_content_type(),
        "| Size:",
        len(part.get_payload(decode=True) or b""),
    )
PY
```

---

## 12. Extract Attachments

Create an isolated directory:

```bash
mkdir -p attachments
```

Extract attachments:

```bash
python3 - <<'PY'
from email import policy
from email.parser import BytesParser
from pathlib import Path

out = Path("attachments")
out.mkdir(exist_ok=True)

with open("suspicious.eml", "rb") as f:
    msg = BytesParser(policy=policy.default).parse(f)

for i, part in enumerate(msg.iter_attachments(), 1):
    filename = part.get_filename() or f"attachment_{i}"
    filename = Path(filename).name
    data = part.get_payload(decode=True)

    if data:
        path = out / filename
        path.write_bytes(data)
        print(f"[+] {path} ({len(data)} bytes)")
PY
```

**Important:** Do not execute extracted attachments during initial analysis.

---

## 13. Identify Attachment Types

```bash
file attachments/*
```

For detailed metadata:

```bash
exiftool attachments/*
```

---

## 14. Calculate Attachment Hashes

SHA-256:

```bash
sha256sum attachments/*
```

SHA-1:

```bash
sha1sum attachments/*
```

MD5:

```bash
md5sum attachments/*
```

For SOC/IR work, prefer SHA-256 as the primary hash.

---

## 15. Search for Suspicious Keywords

```bash
grep -Ein \
'password|passwd|credential|login|verify|urgent|invoice|payment|bank|account|crypto|bitcoin|click|download|macro|enable|attachment|powershell|cmd|base64|javascript|script' \
suspicious.eml
```

---

## 16. Analyze HTML and JavaScript

Search for HTML:

```bash
grep -Ein '<html|<body|<script|<iframe|<a ' suspicious.eml
```

Search for JavaScript:

```bash
grep -Ein '<script|javascript:|onerror=|onload=|onclick=' suspicious.eml
```

Search for suspicious redirects:

```bash
grep -Ein 'href=|location\.|window\.location|document\.location|redirect' suspicious.eml
```

Search for forms:

```bash
grep -Ein '<form|action=' suspicious.eml
```

---

## 17. Search for Executable and Dangerous File Extensions

```bash
grep -Eai \
'\.(exe|dll|scr|bat|cmd|ps1|vbs|js|hta|zip|rar|7z|iso|docm|xlsm|pptm|lnk|msi|apk)([^a-zA-Z]|$)' \
suspicious.eml
```

---

## 18. Search for PowerShell / Command Execution Indicators

```bash
grep -Ein \
'powershell|pwsh|cmd\.exe|wscript|cscript|mshta|rundll32|regsvr32|certutil|bitsadmin' \
suspicious.eml
```

---

## 19. Search for Base64

```bash
grep -Ein 'base64|content-transfer-encoding: base64' suspicious.eml
```

Decode a known Base64 value:

```bash
echo 'BASE64_DATA' | base64 -d
```

Inspect the raw EML:

```bash
xxd suspicious.eml | less
```

---

## 20. Search for MIME Information

```bash
grep -Eai \
'content-type:|content-disposition:|content-transfer-encoding:' \
suspicious.eml
```

Useful indicators:

- `multipart/mixed`
- `multipart/alternative`
- `text/plain`
- `text/html`
- `application/octet-stream`
- `Content-Disposition: attachment`
- `Content-Transfer-Encoding: base64`

---

## 21. Install Useful Kali/Linux Tools

```bash
sudo apt update
sudo apt install -y ripgrep file binutils exiftool yara
```

Then search efficiently:

```bash
rg -ni \
'powershell|cmd\.exe|javascript|base64|http://|https://|\.exe|\.dll|\.ps1' \
suspicious.eml
```

---

# 22. Complete Initial EML Triage

Create an analysis directory:

```bash
mkdir -p eml_analysis/{attachments,output}
```

Copy the email:

```bash
cp suspicious.eml eml_analysis/
cd eml_analysis
```

Calculate the EML hash:

```bash
sha256sum suspicious.eml | tee output/eml_sha256.txt
```

Identify the file:

```bash
file suspicious.eml | tee output/file_type.txt
```

Extract headers:

```bash
sed '/^$/q' suspicious.eml | tee output/headers.txt
```

Extract `Received` headers:

```bash
grep -Eai '^Received:' suspicious.eml | tee output/received.txt
```

Extract authentication information:

```bash
grep -Eai \
'authentication-results|received-spf|dkim-signature|dmarc' \
suspicious.eml | tee output/authentication.txt
```

Extract IP addresses:

```bash
grep -Eo \
'\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' \
suspicious.eml | sort -u | tee output/ips.txt
```

Extract URLs:

```bash
grep -Eo \
'https?://[^[:space:]<>"()]+' \
suspicious.eml | sort -u | tee output/urls.txt
```

Extract domains:

```bash
grep -Eo \
'([A-Za-z0-9-]+\.)+[A-Za-z]{2,}' \
suspicious.eml | sort -fu | tee output/domains.txt
```

Search suspicious keywords:

```bash
grep -Ein \
'password|credential|verify|urgent|invoice|payment|login|powershell|javascript|base64|download' \
suspicious.eml | tee output/suspicious_strings.txt
```

---

# 23. Recommended SOC Analysis Workflow

Use this sequence:

```text
EML File
   |
   v
File Hash
   |
   v
Headers
   |
   v
Received Chain
   |
   v
Sender / Reply-To / Return-Path
   |
   v
SPF / DKIM / DMARC
   |
   v
IP Extraction
   |
   v
Domain Extraction
   |
   v
URL Extraction
   |
   v
MIME Structure
   |
   v
Attachment Analysis
   |
   v
Attachment Hashing
   |
   v
HTML / JavaScript Analysis
   |
   v
IOC Extraction
   |
   v
Phishing / Maliciousness Assessment
```

---

# 24. Important IOCs to Record

During analysis, record:

| IOC Type | Examples |
|---|---|
| Sender | attacker@example.com |
| Reply-To | fake-reply@example.net |
| Return-Path | suspicious mailbox |
| Source IP | `203.0.113.10` |
| Domain | `example.net` |
| URL | `https://example.net/login` |
| Attachment | `invoice.exe` |
| SHA-256 | `...` |
| Message-ID | `<abc@example.com>` |
| DKIM domain | `example.com` |
| SPF result | `fail` |
| DKIM result | `fail` |
| DMARC result | `fail` |

---

# 25. Quick One-Liner IOC Extraction

```bash
{
echo "===== SHA256 ====="
sha256sum suspicious.eml

echo
echo "===== IPS ====="
grep -Eo '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' suspicious.eml | sort -u

echo
echo "===== URLS ====="
grep -Eo 'https?://[^[:space:]<>"()]+' suspicious.eml | sort -u

echo
echo "===== DOMAINS ====="
grep -Eo '([A-Za-z0-9-]+\.)+[A-Za-z]{2,}' suspicious.eml | sort -fu

echo
echo "===== AUTHENTICATION ====="
grep -Eai 'authentication-results|received-spf|dkim-signature|dmarc' suspicious.eml

echo
echo "===== RECEIVED ====="
grep -Eai '^Received:' suspicious.eml

echo
echo "===== SUSPICIOUS STRINGS ====="
grep -Ein 'powershell|cmd\.exe|javascript|base64|credential|password|verify|urgent|invoice|payment' suspicious.eml
} | tee eml_triage.txt
```

---

# 26. Safety Rules

When investigating suspicious EML files:

1. Do not open suspicious links in your normal browser.
2. Do not execute extracted attachments.
3. Do not enable macros in Office documents.
4. Do not run scripts from attachments.
5. Prefer an isolated VM for dynamic analysis.
6. Preserve the original EML file.
7. Calculate the original SHA-256 hash before analysis.
8. Work on copies where possible.
9. Treat extracted URLs, files, and scripts as potentially malicious.
10. Record all discovered IOCs.

---

# 27. Final SOC Investigation Checklist

- [ ] Calculate EML SHA-256
- [ ] Identify file type
- [ ] Extract complete headers
- [ ] Analyze `Received` chain
- [ ] Identify sender
- [ ] Check `Reply-To`
- [ ] Check `Return-Path`
- [ ] Check `Message-ID`
- [ ] Check SPF
- [ ] Check DKIM
- [ ] Check DMARC
- [ ] Extract IP addresses
- [ ] Extract domains
- [ ] Extract URLs
- [ ] Analyze MIME structure
- [ ] List attachments
- [ ] Extract attachments into an isolated directory
- [ ] Identify attachment file types
- [ ] Calculate attachment SHA-256 hashes
- [ ] Inspect attachment metadata
- [ ] Search for JavaScript
- [ ] Search for PowerShell
- [ ] Search for command execution indicators
- [ ] Search for Base64/encoded content
- [ ] Identify suspicious redirects
- [ ] Build an IOC list
- [ ] Determine phishing/malware indicators
- [ ] Write the final SOC finding

---

## Useful Command Summary

```bash
# File
file suspicious.eml
sha256sum suspicious.eml

# Headers
sed '/^$/q' suspicious.eml

# Mail path
grep -Eai '^Received:' suspicious.eml

# Authentication
grep -Eai 'authentication-results|received-spf|dkim-signature|dmarc' suspicious.eml

# IPs
grep -Eo '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' suspicious.eml | sort -u

# Domains
grep -Eo '([A-Za-z0-9-]+\.)+[A-Za-z]{2,}' suspicious.eml | sort -fu

# URLs
grep -Eo 'https?://[^[:space:]<>"()]+' suspicious.eml | sort -u

# Suspicious strings
grep -Ein 'powershell|cmd\.exe|javascript|base64|credential|password|verify|urgent' suspicious.eml

# MIME
grep -Eai 'content-type:|content-disposition:|content-transfer-encoding:' suspicious.eml

# Attachments
file attachments/*
sha256sum attachments/*
exiftool attachments/*
```

---

# Document Information

| Field | Information |
|---|---|
| Document | EML Email Forensic Analysis |
| Prepared by | Zaber Mahmud |
| Organization | EWU Cybersecurity Club (EWUCSC) |
| Platform | Linux / Kali Linux |
| Primary Use | SOC & Email Forensics |
| Topics | Phishing, Headers, SPF, DKIM, DMARC, URLs, IPs, Attachments, IOCs |
| Version | 1.0 |
| Date | 19 August 2026 |

---

## Disclaimer

This document is intended for **authorized cybersecurity investigation, defensive security operations, digital forensics, education, and incident response**.

Analyze suspicious email files in an isolated and controlled environment. Do not open malicious URLs or execute potentially harmful attachments on production systems.

**Prepared by Zaber Mahmud — EWU Cybersecurity Club (EWUCSC)**
