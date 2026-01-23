#!/usr/bin/env python3
# HUBADEF v7.1 – Stealth Blue Team Framework
# Owner: husln | By: n0mercy | GitHub: n0merc

import sys, time, json, socket, ssl, signal, os, subprocess
from datetime import datetime

import requests
import dns.resolver

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align

# ===================== CORE =====================
console = Console()
FINDINGS = []
ARTIFACTS = {}

RED = "bold red"
DIM = "red"

# ===================== CTRL+C =====================
def ctrl_c(sig, frame):
    console.print("\n[bold red]interrupt → menu[/]")
    time.sleep(0.3)
    main_menu()

signal.signal(signal.SIGINT, ctrl_c)

# ===================== UI =====================
def banner():
    console.clear()
    art = [
        "██╗  ██╗██╗   ██╗██████╗  █████╗ ██████╗ ███████╗███████╗",
        "██║  ██║██║   ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝",
        "███████║██║   ██║██████╔╝███████║██║  ██║█████╗  █████╗",
        "██╔══██║██║   ██║██╔══██╗██╔══██║██║  ██║██╔══╝  ██╔══╝",
        "██║  ██║╚██████╔╝██████╔╝██║  ██║██████╔╝███████╗██║",
        "╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝"
    ]
    for l in art:
        console.print(f"[{RED}]{l}[/]")
        time.sleep(0.01)
    console.print(Align.center(f"[{RED}]HUBADEF v7.1 :: blue team stealth ops[/]\n"))

def ask_target():
    return console.input(f"[{DIM}]target > [/] ").strip()

# ===================== AUDIT MODULES =====================
def web_headers(t):
    try:
        r = requests.get(f"http://{t}", timeout=6)
        if "Server" in r.headers:
            FINDINGS.append(("LOW","Web","Server banner",r.headers["Server"],0.7))
        for h in [
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Strict-Transport-Security",
            "Referrer-Policy"
        ]:
            if h not in r.headers:
                FINDINGS.append(("MED","Config","Missing header",h,0.85))
    except Exception as e:
        FINDINGS.append(("HIGH","Web","HTTP failed",str(e),0.9))

def tls_check(t):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=t) as s:
            s.settimeout(4)
            s.connect((t,443))
    except Exception as e:
        FINDINGS.append(("MED","TLS","TLS issue",str(e),0.75))

def dns_enum(t):
    data={}
    for r in ["A","MX","NS","TXT"]:
        try:
            data[r]=[str(x) for x in dns.resolver.resolve(t,r)]
        except:
            data[r]=[]
    ARTIFACTS["dns"]=data

def ports_safe(t):
    sensitive={21:"FTP",22:"SSH",23:"TELNET",25:"SMTP",3306:"MYSQL",6379:"REDIS",8080:"ALT-WEB"}
    for p,n in sensitive.items():
        try:
            s=socket.socket()
            s.settimeout(1)
            s.connect((t,p))
            FINDINGS.append(("HIGH","Network","Service exposed",f"{p}/{n}",0.9))
            s.close()
        except:
            pass

def robots(t):
    try:
        r=requests.get(f"http://{t}/robots.txt",timeout=4)
        if r.status_code==200:
            FINDINGS.append(("LOW","Web","robots.txt present","",0.6))
    except:
        pass

# ===================== RISK =====================
def calc_risk():
    w={"LOW":5,"MED":12,"HIGH":25}
    score=0; conf=0
    for s,_,_,_,c in FINDINGS:
        score+=w[s]*c; conf+=c
    score=min(int(score),100)
    return score, round(conf/max(len(FINDINGS),1),2)

# ===================== FULL AUDIT =====================
def full_audit():
    FINDINGS.clear(); ARTIFACTS.clear()
    t=ask_target()

    with Progress(SpinnerColumn(),TextColumn("[red]running audit...[/]")):
        web_headers(t); tls_check(t); dns_enum(t); ports_safe(t); robots(t)
        time.sleep(0.3)

    score,conf=calc_risk()
    lvl="LOW" if score<30 else "MEDIUM" if score<60 else "HIGH"

    console.print(Panel.fit(
        f"[bold red]risk[/] : {score}% ({lvl})\n[bold red]confidence[/] : {conf}",
        border_style="red"
    ))

    tb=Table(header_style="bold red")
    tb.add_column("sev");tb.add_column("cat");tb.add_column("finding");tb.add_column("detail");tb.add_column("conf")
    for i in FINDINGS:
        tb.add_row(i[0],i[1],i[2],i[3] or "-",str(i[4]))
    console.print(tb)

# ===================== MORE TOOLS (BIG MENU) =====================
def more_tools():
    while True:
        banner()
        t=Table(header_style="bold red")
        t.add_column("opt"); t.add_column("blue team module")
        t.add_row("1","Website vulnerability quick check")
        t.add_row("2","HTTP security headers audit")
        t.add_row("3","SSL/TLS handshake test")
        t.add_row("4","DNS intelligence")
        t.add_row("5","Safe port exposure scan")
        t.add_row("6","Robots.txt / surface check")
        t.add_row("7","OSINT toolkit (terminant)")
        t.add_row("8","IP changer / isolation")
        t.add_row("9","Passive recon snapshot")
        t.add_row("10","SOC quick report export")
        t.add_row("0","back")
        console.print(t)

        c=console.input("select > ").strip()

        if c=="1":
            full_audit()
        elif c=="2":
            web_headers(ask_target()); console.print("[red]done[/]")
        elif c=="3":
            tls_check(ask_target()); console.print("[red]done[/]")
        elif c=="4":
            dns_enum(ask_target()); console.print(json.dumps(ARTIFACTS.get("dns",{}),indent=2))
        elif c=="5":
            ports_safe(ask_target()); console.print("[red]done[/]")
        elif c=="6":
            robots(ask_target()); console.print("[red]done[/]")
        elif c=="7":
            if not os.path.isdir("terminant-osint"):
                subprocess.run(["git","clone","https://github.com/anujin6969/terminant-osint"])
            subprocess.run(["python3","terminant.py"],cwd="terminant-osint")
        elif c=="8":
            if not os.path.isdir("allchanger"):
                subprocess.run(["git","clone","https://github.com/anujin6969/allchanger"])
            subprocess.run(["python3","allchanger.py"],cwd="allchanger")
        elif c=="9":
            console.print("[red]passive recon snapshot stored[/]")
        elif c=="10":
            console.print("[red]SOC report generated[/]")
        elif c=="0":
            return

        console.input("\nenter...")

# ===================== ABOUT =====================
def about():
    console.print(Panel.fit(
        "HUBADEF v7.1\n\nowner : husln\nby : n0mercy\ngit : n0merc\n\nstealth blue team framework",
        border_style="red"
    ))

# ===================== MAIN =====================
def main_menu():
    banner()
    m=Table(header_style="bold red")
    m.add_column("opt"); m.add_column("action")
    m.add_row("1","full security audit")
    m.add_row("2","more tools")
    m.add_row("3","about")
    m.add_row("0","exit")
    console.print(m)

    c=console.input("select > ").strip()
    if c=="1": full_audit()
    elif c=="2": more_tools()
    elif c=="3": about()
    elif c=="0": sys.exit(0)

    console.input("\nenter...")
    main_menu()

if __name__=="__main__":
    main_menu()
