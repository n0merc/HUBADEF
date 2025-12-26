# HUBADEF

**HUBADEF** is a stealth-style **Blue Team security audit framework** designed for defensive security testing, monitoring, and SOC-style analysis.

The tool focuses on **realistic, safe, and passive checks** without triggering aggressive alerts or unnecessary noise.

---

##  Features

- Full website security audit with risk scoring
- HTTP security headers analysis
- SSL/TLS handshake and HTTPS availability check
- DNS intelligence (A, MX, NS, TXT)
- Safe service / port exposure detection
- Robots.txt and surface exposure check
- SOC-style findings table with confidence levels
- Stealth hacker-style terminal UI (red theme)
- Ctrl+C safe navigation
- Integrated external tools

---

##  Blue Team Modules

- Web configuration analysis
- Network exposure detection (safe)
- Passive reconnaissance
- Misconfiguration detection
- Risk percentage & confidence scoring
- SOC-ready JSON report generation

---

##  Integrated Tools

- **Terminant OSINT**
  - https://github.com/anujin6969/terminant-osint

- **AllChanger (IP / Network isolation)**
  - https://github.com/anujin6969/allchanger

These tools are automatically cloned and launched from the menu.

---

##  Requirements

```bash
pip install requests rich dnspython
Python version:

nginx
Copy code
Python 3.9+
  Usage
bash
Copy code
python3 hubadef.py
Navigate using the menu:

Full Security Audit

More Tools (Blue Team Modules)

About

Exit

Press CTRL+C at any time to safely return to the menu.

Output
Terminal-based findings table

Risk level (LOW / MEDIUM / HIGH)

Confidence score

JSON SOC report (auto-saved)

Example report:

pgsql
Copy code
SOC_target_YYYYMMDD_HHMMSS.json

⚠️ Disclaimer
This framework is intended for defensive security testing and educational purposes only.

Use only on systems you own or have explicit permission to audit

The author is not responsible for misuse

👤 Author
Owner: husln

By: n0mercy

GitHub: https://github.com/anujin6969

install

git clone https://github.com/anujin6969/HUBADEF.git
cd HUBADEF
pip install -r requirements.txt
python3 hubadef.py


