"""Generates the animated SVG assets for the GitHub profile README (light + dark)."""
import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", fg="#e6edf3", muted="#8b949e",
                 a1="#f5a524", a2="#22d3ee", a3="#a78bfa", grid="#21262d", glow=0.55),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", fg="#1f2328", muted="#59636e",
                  a1="#d97706", a2="#0891b2", a3="#7c3aed", grid="#e6e9ec", glow=0.28),
}
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
CH = 0.602  # monospace advance per em


def write(name, svg):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)


def header(t):
    W, H = 1200, 340
    phrases = ["building cross-chain payment rails", "shipping native dev tools in Rust",
               "turning ideas into production systems"]
    cyc, n = 12, len(phrases)
    typed = []
    for i, p in enumerate(phrases):
        w = len(p) * 20 * CH + 4
        s, e = i / n, (i + 1) / n
        kt = [0, s, s + 0.10, e - 0.05, e - 0.01, 1]
        kt = ";".join(f"{min(max(k, 0), 1):.4f}" for k in kt)
        vals = f"0;0;{w:.0f};{w:.0f};0;0"
        cx = ";".join(f"{v}" for v in [92, 92, 92 + w, 92 + w, 92, 92])
        op = "0;1;1;1;0;0" if i else "1;1;1;1;0;0"
        typed.append(f'''
    <clipPath id="c{i}"><rect x="92" y="238" height="34" width="{w if i == 0 else 0:.0f}">
      <animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{cyc}s" repeatCount="indefinite"/></rect></clipPath>
    <text x="92" y="262" font-family="{MONO}" font-size="20" fill="{t['a1']}" clip-path="url(#c{i})">{escape(p)}</text>
    <rect x="{92 + w:.0f}" y="243" width="11" height="24" fill="{t['a1']}" opacity="{1 if i == 0 else 0}">
      <animate attributeName="x" values="{cx}" keyTimes="{kt}" dur="{cyc}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="{op}" keyTimes="{kt}" dur="{cyc}s" repeatCount="indefinite" calcMode="discrete"/>
    </rect>''')

    # cross-chain graph on the right: chains around a treasury hub, value packets flowing
    hub = (965, 170)
    nodes = [("ETH", 820, 78), ("BASE", 1110, 78), ("ARB", 820, 262), ("SOL", 1110, 262)]
    paths, packets, boxes = [], [], []
    for k, (label, x, y) in enumerate(nodes):
        d = f"M{x},{y} C{(x + hub[0]) / 2},{y} {(x + hub[0]) / 2},{hub[1]} {hub[0]},{hub[1]}"
        paths.append(f'<path id="p{k}" d="{d}" fill="none" stroke="{t["border"]}" stroke-width="1.5" stroke-dasharray="4 5"/>')
        col = [t["a1"], t["a2"], t["a3"], t["a2"]][k]
        rev = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if k % 2 else ""
        packets.append(f'''<circle r="4.5" fill="{col}" filter="url(#soft)" opacity="0">
      <set attributeName="opacity" to="1" begin="{k * 0.7:.1f}s"/>
      <animateMotion dur="{2.6 + k * 0.45:.2f}s" repeatCount="indefinite" begin="{k * 0.7:.1f}s"{rev}><mpath href="#p{k}"/></animateMotion></circle>''')
        boxes.append(f'''<g><rect x="{x - 36}" y="{y - 18}" width="72" height="36" rx="10" fill="{t['panel']}" stroke="{col}" stroke-opacity="0.7"/>
      <text x="{x}" y="{y + 5}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="600" fill="{t['fg']}">{label}</text></g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Arpit Patidar, Full-Stack and Web3 Engineer">
  <defs>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t['grid']}"/></pattern>
    <radialGradient id="g1"><stop offset="0" stop-color="{t['a1']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['a1']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="g2"><stop offset="0" stop-color="{t['a2']}" stop-opacity="{t['glow'] * 0.8}"/><stop offset="1" stop-color="{t['a2']}" stop-opacity="0"/></radialGradient>
    <linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="{t['fg']}"/><stop offset="0.55" stop-color="{t['fg']}"/><stop offset="1" stop-color="{t['a1']}"/></linearGradient>
    <filter id="soft" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="frame"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{t['bg']}"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
    <circle cx="980" cy="60" r="260" fill="url(#g1)"><animate attributeName="cx" values="980;900;980" dur="14s" repeatCount="indefinite"/></circle>
    <circle cx="160" cy="330" r="240" fill="url(#g2)"><animate attributeName="cy" values="330;280;330" dur="11s" repeatCount="indefinite"/></circle>
  </g>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="none" stroke="{t['border']}"/>

  <g font-family="{SANS}">
    <circle cx="70" cy="76" r="5" fill="#3fb950"><animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/></circle>
    <text x="84" y="81" font-family="{MONO}" font-size="14" letter-spacing="2" fill="{t['muted']}">OPEN TO INTERESTING PROBLEMS · INDORE, INDIA</text>
    <text x="62" y="160" font-size="68" font-weight="800" letter-spacing="-2" fill="url(#name)">Arpit Patidar</text>
    <text x="64" y="208" font-size="27" font-weight="500" fill="{t['fg']}" opacity="0.85">Full-Stack &amp; Web3 Engineer</text>
    <text x="64" y="262" font-family="{MONO}" font-size="20" fill="{t['muted']}">&gt;</text>
    {''.join(typed)}
    <text x="64" y="306" font-family="{MONO}" font-size="13" fill="{t['muted']}">TypeScript · Next.js · Node / NestJS · Rust · Web3</text>
  </g>

  {''.join(paths)}
  {''.join(packets)}
  <circle cx="{hub[0]}" cy="{hub[1]}" r="46" fill="none" stroke="{t['a1']}" stroke-opacity="0.35">
    <animate attributeName="r" values="40;58;40" dur="3s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values="0.45;0;0.45" dur="3s" repeatCount="indefinite"/></circle>
  <rect x="{hub[0] - 52}" y="{hub[1] - 26}" width="104" height="52" rx="14" fill="{t['panel']}" stroke="{t['a1']}"/>
  <text x="{hub[0]}" y="{hub[1] - 2}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{t['a1']}">TREASURY</text>
  <text x="{hub[0]}" y="{hub[1] + 15}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{t['muted']}">quote · settle</text>
  {''.join(boxes)}
</svg>'''


def reveal(at):
    """Hidden until `at` seconds when animated; fully visible where SVG animation is unsupported."""
    if at <= 0:
        return ""
    return f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;0.999;1" dur="{at:.2f}s" fill="freeze"/>'


def terminal(t):
    W = 1000
    lines = [
        ("cmd", "whoami"),
        ("out", [("Arpit Patidar", "fg"), (" — Full-Stack & Web3 Engineer · 3+ yrs · 15+ live products", "muted")]),
        ("cmd", "cat ./now.md"),
        ("out", [("▸ ", "a1"), ("Software Engineer @ Metaverse Ventures", "fg"), (" (remote)", "muted")]),
        ("out", [("▸ ", "a1"), ("cross-chain treasury: swap · bridge · yield · pay-in/out · stablecoins", "muted")]),
        ("out", [("▸ ", "a1"), ("Privy embedded wallets · multi-chain virtual accounts · auto fund routing", "muted")]),
        ("cmd", "ls ~/shipped"),
        ("out", [("stablecoinpay.io  stables.link  intentswap.io  metasub.xyz  adventuredao.com", "a2")]),
        ("cmd", "stackroost --version"),
        ("out", [("✓ ", "ok"), ("v0.2.0", "fg"), (" · macOS dev console · Rust + Tauri 2 + React 19", "muted")]),
        ("cmd", ""),
    ]
    colors = dict(t, ok="#3fb950")
    y0, lh, t0 = 92, 30, 0.4
    body, t_at = [], t0
    for i, (kind, val) in enumerate(lines):
        y = y0 + i * lh
        if kind == "cmd":
            w = len(val) * 15 * CH + 2
            dur = max(0.05 * len(val), 0.01)
            prompt = (f'<text x="40" y="{y}" font-size="15"><tspan fill="{t["a1"]}">arpit</tspan>'
                      f'<tspan fill="{t["muted"]}">@</tspan><tspan fill="{t["a2"]}">mac</tspan>'
                      f'<tspan fill="{t["muted"]}"> ~ $</tspan></text>')
            px = 40 + len("arpit@mac ~ $ ") * 15 * CH
            body.append(f'<g>{reveal(t_at)}{prompt}')
            if val:
                body.append(f'''<clipPath id="t{i}"><rect x="{px:.0f}" y="{y - 16}" height="22" width="{w:.0f}">
        <animate attributeName="width" values="0;0;{w:.0f}" keyTimes="0;{(t_at + 0.25) / (t_at + 0.25 + dur):.4f};1" dur="{t_at + 0.25 + dur:.2f}s" fill="freeze"/></rect></clipPath>
      <text x="{px:.0f}" y="{y}" font-size="15" fill="{t['fg']}" clip-path="url(#t{i})">{escape(val)}</text>''')
            else:
                body.append(f'''<rect x="{px:.0f}" y="{y - 14}" width="9" height="18" fill="{t['a1']}">
        <animate attributeName="opacity" values="1;0;1" dur="1.1s" begin="{t_at:.2f}s" repeatCount="indefinite" calcMode="discrete"/></rect>''')
            body.append("</g>")
            t_at += 0.25 + dur + 0.25
        else:
            spans = "".join(f'<tspan fill="{colors[c]}">{escape(s)}</tspan>' for s, c in val)
            body.append(f'''<text x="40" y="{y}" font-size="15">{reveal(t_at)}{spans}</text>''')
            t_at += 0.18
    H = y0 + len(lines) * lh + 10
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="whoami: Arpit Patidar, Full-Stack and Web3 Engineer">
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{t['panel']}" stroke="{t['border']}"/>
  <path d="M1,17 a16,16 0 0 1 16,-16 H{W - 17} a16,16 0 0 1 16,16 V46 H1 Z" fill="{t['bg']}"/>
  <line x1="1" y1="46" x2="{W - 1}" y2="46" stroke="{t['border']}"/>
  <circle cx="28" cy="24" r="6.5" fill="#ff5f57"/><circle cx="50" cy="24" r="6.5" fill="#febc2e"/><circle cx="72" cy="24" r="6.5" fill="#28c840"/>
  <text x="{W / 2}" y="29" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t['muted']}">arpit@mac — zsh — 100×12</text>
  <g font-family="{MONO}">{''.join(body)}</g>
</svg>'''


CARDS = [
    ("Stackroost", "Your Mac's developer console in one window: Homebrew services, ports, SSH server fleet, system doctor and disk cleanup.", "Rust", "#dea584", ["Tauri 2", "React 19", "macOS"]),
    ("job-hunter-bot", "Self-expanding, event-driven job intelligence engine with BM25 / TF-IDF scoring and AI validation on the edge.", "JavaScript", "#f1e05a", ["Cloudflare", "BM25", "AI"]),
    ("Git-Agent", "Event-driven GitHub automation bot: webhooks in, user-defined rules, Slack notifications and automated write-backs.", "TypeScript", "#3178c6", ["Webhooks", "Slack", "Rules"]),
    ("WarehousePulse-server", "Real-time IoT telemetry for warehouse operations: ingestion API, Redis pub/sub and Server-Sent Events.", "TypeScript", "#3178c6", ["Express", "Redis", "SSE"]),
    ("E-Commerce-Microservices", "Horizontally scalable commerce backend: API gateway with rate limiting in front of independent services.", "TypeScript", "#3178c6", ["Fastify", "MongoDB", "Gateway"]),
    ("taskboard-race-lab", "A lab for race conditions in client state: optimistic updates, stale responses and conflict handling.", "TypeScript", "#3178c6", ["React", "TanStack", "Express"]),
]


def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return out + [cur]


def card(t, name, desc, lang, lcol, tags):
    W, H = 480, 196
    lines = wrap(desc, 54)[:3]
    desc_svg = "".join(f'<text x="28" y="{86 + i * 22}" font-size="14" fill="{t["muted"]}">{escape(l)}</text>' for i, l in enumerate(lines))
    x, pills = 28, []
    for tag in tags:
        w = len(tag) * 7.2 + 20
        pills.append(f'<rect x="{x:.0f}" y="156" width="{w:.0f}" height="24" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>'
                     f'<text x="{x + w / 2:.0f}" y="172" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{t["fg"]}">{escape(tag)}</text>')
        x += w + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(name)}: {escape(desc)}">
  <defs><linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/></linearGradient></defs>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{t['panel']}" stroke="{t['border']}"/>
  <rect x="28" y="1" width="64" height="3" rx="1.5" fill="url(#bar)"/>
  <g font-family="{SANS}">
    <path transform="translate(28,30)" fill="{t['muted']}" d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"/>
    <text x="52" y="43" font-size="19" font-weight="700" fill="{t['fg']}">{escape(name)}</text>
    {desc_svg}
    <circle cx="{W - 120}" cy="38" r="6" fill="{lcol}"/>
    <text x="{W - 108}" y="43" font-size="13" fill="{t['muted']}">{lang}</text>
    {''.join(pills)}
  </g>
</svg>'''


def section(t, label, sub):
    W, H = 1000, 64
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">
  <defs><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{t['a1']}"/><stop offset="0.4" stop-color="{t['a2']}" stop-opacity="0.5"/><stop offset="1" stop-color="{t['border']}" stop-opacity="0"/></linearGradient></defs>
  <text x="0" y="22" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{t['a1']}">{escape(sub)}</text>
  <text x="0" y="50" font-family="{SANS}" font-size="24" font-weight="700" fill="{t['fg']}">{escape(label)}</text>
  <rect x="0" y="61" width="{W}" height="2" fill="url(#l)"/>
</svg>'''


def footer(t):
    W, H = 1200, 150
    a = "M0,70 C200,30 400,110 600,70 C800,30 1000,110 1200,70 V150 H0 Z"
    b = "M0,80 C200,120 400,40 600,80 C800,120 1000,40 1200,80 V150 H0 Z"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Thanks for visiting">
  <defs><linearGradient id="w" x1="0" x2="1"><stop offset="0" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/></linearGradient></defs>
  <path d="{a}" fill="url(#w)" opacity="0.22"><animate attributeName="d" values="{a};{b};{a}" dur="9s" repeatCount="indefinite"/></path>
  <path d="{b}" fill="url(#w)" opacity="0.35"><animate attributeName="d" values="{b};{a};{b}" dur="7s" repeatCount="indefinite"/></path>
  <text x="{W / 2}" y="122" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{t['fg']}">THANKS FOR STOPPING BY — LET'S BUILD SOMETHING</text>
</svg>'''


SECTIONS = {"about": ("whoami", "01 — ABOUT"), "work": ("Featured work", "02 — BUILDING"),
            "path": ("Career path", "03 — EXPERIENCE"), "stack": ("Toolbox", "04 — STACK"),
            "shipped": ("Shipped in production", "05 — LIVE"), "activity": ("Activity", "06 — GITHUB")}

for mode, t in THEMES.items():
    write(f"header-{mode}.svg", header(t))
    write(f"terminal-{mode}.svg", terminal(t))
    write(f"footer-{mode}.svg", footer(t))
    for key, (label, sub) in SECTIONS.items():
        write(f"section-{key}-{mode}.svg", section(t, label, sub))
    for c in CARDS:
        write(f"cards/{c[0]}-{mode}.svg", card(t, *c))
print("ok")
