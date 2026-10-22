#!/usr/bin/env python3
"""
README engine for github.com/iprsnmsra  -  stdlib only, zero dependencies.

Every animation in assets/*.svg is SIMULATED here (Kepler orbits, pendulum-wave
resonance, Verlet rope physics, damped harmonograph) and baked into SMIL
keyframes, because GitHub strips JS/CSS from READMEs but keeps SVG-in-<img>.
A GitHub Action re-runs this daily, so the page rebuilds itself from live data.
"""
import os, json, math, hashlib, html, datetime, textwrap, pathlib, urllib.request

# ───────────────────────── CONFIG (edit me) ─────────────────────────
USER     = "iprsnmsra"
NAME     = "Prasoon Mishra"
TAGLINE  = "I never give up."
ROLES    = ["System Designer  ·  Agentic AI  ·  Full-stack",
            "Game Dev  ·  Unity  ·  Unreal  ·  Blender  ·  AWS"]
PLANETS  = ["C++", "Java", "Python", "C#", "TypeScript", "JavaScript"]
FALLBACK = {"C++": 90, "Java": 70, "Python": 80, "C#": 45, "TypeScript": 50, "JavaScript": 60}
PENDULUMS = ["C++", "Java", "Python", "C#", "Node", "React", "Next.js", "AWS",
             "SQL", "DevOps", "Unity", "Unreal", "LLMs", "Blender"]
LINKS = [("PORTFOLIO", "iprsnmsra.vercel.app",       "https://iprsnmsra.vercel.app/"),
         ("LINKEDIN",  "in/iprsnmsra",               "https://www.linkedin.com/in/iprsnmsra"),
         ("EMAIL",     "prasoonmishra9c@gmail.com",  "mailto:prasoonmishra9c@gmail.com")]
# hook = fallback text; the repo's real GitHub description wins if it has one
PROJECTS = [
  dict(slug="vigil",   title="Vigil",   motif="eye",   url="https://github.com/iprsnmsra/vigil",
       repo="vigil",   hook="Always watching, so you never have to.",    tags="MONITORING · SYSTEMS"),
  dict(slug="kestrel", title="Kestrel", motif="radar", url="https://kestrel-ai-threat-analyzer.vercel.app/",
       repo=None,      hook="AI threat analyzer. Hovers, spots, strikes.", tags="LLM · SECURITY · NEXT.JS"),
  dict(slug="animebill", title="AnimeBill", motif="bars", url="https://github.com/iprsnmsra/AnimeBill",
       repo="AnimeBill", hook="Billing with an anime soul.",             tags="FULL-STACK · APP"),
]
# ────────────────────────────────────────────────────────────────────
OUT = pathlib.Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)
H = hashlib.sha256(USER.encode()).digest()          # your deterministic fingerprint
esc = html.escape

def gh(path):
    t = os.environ.get("GITHUB_TOKEN")
    req = urllib.request.Request("https://api.github.com" + path, headers={
        "User-Agent": "readme-engine", "Accept": "application/vnd.github+json",
        **({"Authorization": "Bearer " + t} if t else {})})
    try:
        return json.load(urllib.request.urlopen(req, timeout=20))
    except Exception:
        return None

STYLE = """<style>
:root{--bg:#0d1117;--card:#161b22;--fg:#e6edf3;--dim:#8b949e;--a:#58a6ff;--b:#f778ba;--star:#ffd33d;--ln:#30363d}
@media (prefers-color-scheme:light){:root{--bg:#fff;--card:#f6f8fa;--fg:#1f2328;--dim:#656d76;--a:#0969da;--b:#bf3989;--star:#d4a72c;--ln:#d0d7de}}
text{font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif}
.m{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.fg{fill:var(--fg)}.dim{fill:var(--dim)}.a{fill:var(--a)}.b{fill:var(--b)}
</style>"""

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>{STYLE}{body}</svg>')

def f(x): return f"{x:.1f}".rstrip("0").rstrip(".")

# ───────────── 1. HERO: Kepler orbits + harmonograph signature ─────────────
def harmonograph(x0, y0, w, h, N=2000, dt=0.1):
    fr = [2 + H[i] % 4 + H[i + 4] / 255 * 0.02 for i in range(4)]
    ph = [H[i + 8] / 255 * 2 * math.pi for i in range(4)]
    de = [0.002 + H[i + 12] / 255 * 0.004 for i in range(4)]
    pts = []
    for k in range(N):
        t = k * dt
        pts.append((math.sin(fr[0]*t+ph[0])*math.exp(-de[0]*t) + math.sin(fr[1]*t+ph[1])*math.exp(-de[1]*t),
                    math.sin(fr[2]*t+ph[2])*math.exp(-de[2]*t) + math.sin(fr[3]*t+ph[3])*math.exp(-de[3]*t)))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    s = min(w / (max(xs)-min(xs)), h / (max(ys)-min(ys)))
    mx, my = (max(xs)+min(xs))/2, (max(ys)+min(ys))/2
    return "M" + " L".join(f"{f(x0+w/2+(x-mx)*s)} {f(y0+h/2+(y-my)*s)}" for x, y in pts)

def hero(weights):
    cx, cy, a0 = 215, 215, 62
    wmax = max(w for _, w in weights)
    o = [f'<rect width="900" height="430" rx="14" fill="var(--bg)" stroke="var(--ln)"/>',
         '<defs><radialGradient id="g"><stop offset="0" stop-color="var(--star)"/><stop offset="1" stop-color="var(--star)" stop-opacity="0"/></radialGradient></defs>',
         f'<circle cx="{cx}" cy="{cy}" r="34" fill="url(#g)" opacity=".55"><animate attributeName="r" values="30;40;30" dur="4s" repeatCount="indefinite"/></circle>',
         f'<circle cx="{cx}" cy="{cy}" r="13" fill="var(--star)"/>']
    cols = ["#f2cc60", "#ff7b72", "#58a6ff", "#bc8cff", "#3fb950", "#ffa657"]
    for i, (name, wt) in enumerate(weights):
        a = a0 + i * 28
        T = round(5 * (a / a0) ** 1.5, 2)                 # Kepler: T^2 ∝ a^3
        th = H[i] * 360 / 255
        r = 4.5 + 8 * math.sqrt(wt / wmax)
        px = cx + a
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{a}" fill="none" stroke="var(--ln)" stroke-dasharray="2 5"/>')
        o.append(f'<g><animateTransform attributeName="transform" type="rotate" from="{f(th)} {cx} {cy}" to="{f(th+360)} {cx} {cy}" dur="{T}s" repeatCount="indefinite"/>'
                 f'<circle cx="{px}" cy="{cy}" r="{f(r)}" fill="{cols[i % 6]}"/>'
                 f'<g><animateTransform attributeName="transform" type="rotate" from="{f(-th)} {px} {cy}" to="{f(-th-360)} {px} {cy}" dur="{T}s" repeatCount="indefinite"/>'
                 f'<text class="fg m" x="{px}" y="{f(cy-r-5)}" font-size="10" text-anchor="middle">{esc(name)}</text></g></g>')
    sig = harmonograph(450, 292, 420, 112)
    o += [f'<circle cx="452" cy="86" r="4" fill="#3fb950"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>',
          '<text class="dim m" x="464" y="90" font-size="11" letter-spacing="2">SYSTEM ONLINE</text>',
          f'<text class="fg" x="450" y="150" font-size="46" font-weight="800">{esc(NAME)}</text>',
          f'<text class="b" x="450" y="190" font-size="24" font-style="italic" font-weight="600">{esc(TAGLINE)}</text>',
          f'<text class="dim" x="450" y="224" font-size="14">{esc(ROLES[0])}</text>',
          f'<text class="dim" x="450" y="246" font-size="14">{esc(ROLES[1])}</text>',
          '<text class="a m" x="450" y="276" font-size="10">T² ∝ a³ · orbit = Kepler · radius ∝ √(bytes of code written)</text>',
          f'<path d="{sig}" pathLength="1" fill="none" stroke="var(--b)" stroke-width=".7" stroke-linejoin="round" stroke-dasharray="1 1" stroke-dashoffset="1">'
          '<animate attributeName="stroke-dashoffset" values="1;0;0;-1" keyTimes="0;.6;.85;1" dur="16s" repeatCount="indefinite"/></path>',
          f'<text class="dim m" x="450" y="420" font-size="9">signature = damped harmonograph(sha256("{USER}")) — unique to this account</text>']
    return svg(900, 430, "".join(o), f"{NAME} — orbital system of languages")

# ───────────── 2. PENDULUM WAVE: resonance realigns every 60 s ─────────────
def pendulum():
    n, N0, A, cy, S = len(PENDULUMS), 30, 78, 150, 40
    o = ['<rect width="900" height="300" rx="14" fill="var(--bg)" stroke="var(--ln)"/>',
         '<text class="fg" x="30" y="36" font-size="15" font-weight="700">PENDULUM WAVE</text>',
         '<text class="dim m" x="30" y="54" font-size="10">T_i = 60 / (30 + i)  →  all skills re-align in perfect phase every 60 s</text>',
         f'<line x1="30" x2="870" y1="{cy}" y2="{cy}" stroke="var(--ln)" stroke-dasharray="3 5"/>']
    for i, name in enumerate(PENDULUMS):
        x = 60 + i * (780 / (n - 1))
        T = 60 / (N0 + i)
        vals = ";".join(f(cy + A * math.sin(2 * math.pi * k / S)) for k in range(S + 1))
        hue = 205 + i * (130 / n)
        o.append(f'<line x1="{f(x)}" x2="{f(x)}" y1="{cy-A}" y2="{cy+A}" stroke="var(--ln)" opacity=".6"/>')
        o.append(f'<circle cx="{f(x)}" cy="{cy}" r="9" fill="hsl({hue:.0f},80%,62%)"><animate attributeName="cy" values="{vals}" dur="{T:.4f}s" repeatCount="indefinite"/></circle>')
        o.append(f'<text class="dim m" x="{f(x)}" y="262" font-size="10" text-anchor="middle">{esc(name)}</text>')
    o += ['<rect x="30" y="278" width="840" height="3" rx="1.5" fill="var(--ln)"/>',
          '<rect x="30" y="278" width="0" height="3" rx="1.5" fill="var(--a)"><animate attributeName="width" values="0;840" dur="60s" repeatCount="indefinite"/></rect>']
    return svg(900, 300, "".join(o), "Pendulum wave of skills")

# ───────────── 3. VERLET ROPES: real constraint physics, baked ─────────────
def rope(label, sub, idx):
    W, Hh, n, L, dt = 300, 175, 14, 5.6, 1 / 30
    ax, ay, steps = W / 2, 10, 150                           # 5 s loop
    P = [[ax, ay + i * L] for i in range(n)]
    Q = [p[:] for p in P]
    inv = [0] + [1] * (n - 2) + [0.35]                       # heavy tag at the end
    frames, ph = [], idx * 0.9
    for s in range(steps * 30 + steps):
        t = s * dt
        wind = 330 * math.sin(2 * math.pi * t / 5 + ph) + 110 * math.sin(4 * math.pi * t / 5 + 2 * ph)
        for i in range(1, n):
            x, y = P[i]; px, py = Q[i]
            Q[i] = [x, y]
            P[i] = [x + (x - px) * 0.992 + wind * dt * dt, y + (y - py) * 0.992 + 900 * dt * dt]
        for _ in range(24):
            P[0] = [ax, ay]
            for i in range(n - 1):
                dx, dy = P[i+1][0]-P[i][0], P[i+1][1]-P[i][1]
                d = math.hypot(dx, dy) or 1e-9
                k = (d - L) / d; wi, wj = inv[i], inv[i+1]
                if wi + wj == 0: continue
                P[i][0] += dx*k*wi/(wi+wj); P[i][1] += dy*k*wi/(wi+wj)
                P[i+1][0] -= dx*k*wj/(wi+wj); P[i+1][1] -= dy*k*wj/(wi+wj)
        if s >= steps * 30: frames.append([p[:] for p in P])   # last period only (steady state)
    frames.append(frames[0])
    d = ";".join("M" + " L".join(f"{f(p[0])} {f(p[1])}" for p in fr) for fr in frames)
    tr = ";".join(f"{f(fr[-1][0])} {f(fr[-1][1])}" for fr in frames)
    rot = ";".join(f(-math.degrees(math.atan2(fr[-1][0]-fr[-2][0], fr[-1][1]-fr[-2][1]))) for fr in frames)
    o = [f'<circle cx="{ax}" cy="{ay}" r="4" fill="var(--dim)"/>',
         f'<path fill="none" stroke="var(--dim)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="{d.split(";")[0]}">'
         f'<animate attributeName="d" values="{d}" dur="5s" repeatCount="indefinite"/></path>',
         '<g><animateTransform attributeName="transform" type="translate" values="%s" dur="5s" repeatCount="indefinite"/>' % tr,
         '<g><animateTransform attributeName="transform" type="rotate" values="%s" dur="5s" repeatCount="indefinite"/>' % rot,
         '<rect x="-88" y="0" width="176" height="52" rx="9" fill="var(--card)" stroke="var(--a)" stroke-width="1.5"/>',
         '<circle cx="0" cy="7" r="3" fill="var(--bg)" stroke="var(--dim)"/>',
         f'<text class="fg" x="0" y="29" font-size="14" font-weight="700" text-anchor="middle" letter-spacing="1.5">{esc(label)}</text>',
         f'<text class="a m" x="0" y="44" font-size="9" text-anchor="middle">{esc(sub)}</text></g></g>']
    return svg(W, Hh, "".join(o), f"{label} link hanging on a physics rope")

# ───────────── 4. PROJECT CARDS ─────────────
def motif(kind):
    if kind == "radar":
        return ('<circle r="20" fill="none" stroke="var(--a)" opacity=".5"/><circle r="10" fill="none" stroke="var(--a)" opacity=".35"/>'
                '<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="3s" repeatCount="indefinite"/>'
                '<path d="M0 0 L20 0 A20 20 0 0 0 14 -14 Z" fill="var(--a)" opacity=".45"/><line x2="20" stroke="var(--a)" stroke-width="2"/></g>')
    if kind == "eye":
        return ('<path d="M-22 0 Q0 -20 22 0 Q0 20 -22 0Z" fill="none" stroke="var(--a)" stroke-width="2"/>'
                '<circle r="7" fill="var(--b)"><animate attributeName="cx" values="-8;8;-8" dur="3.2s" repeatCount="indefinite"/></circle>'
                '<path d="M-22 0 Q0 -20 22 0 Q0 -20 -22 0Z" fill="var(--card)"><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;.9;.95;1;1" dur="4s" repeatCount="indefinite"/></path>')
    out = ""
    for i in range(4):
        hs = [10, 22, 15, 28]
        out += (f'<rect x="{-20+i*11}" width="7" rx="2" fill="var(--a)"><animate attributeName="height" values="4;{hs[i]};4" dur="{1.6+i*.3}s" repeatCount="indefinite"/>'
                f'<animate attributeName="y" values="14;{14-hs[i]};14" dur="{1.6+i*.3}s" repeatCount="indefinite"/></rect>')
    return out

def card(p, desc):
    hook = textwrap.wrap(desc or p["hook"], 32)[:2]
    o = ['<rect x=".5" y=".5" width="299" height="159" rx="12" fill="var(--card)" stroke="var(--ln)"/>',
         '<rect x=".5" y=".5" width="299" height="159" rx="12" fill="none" stroke="var(--b)" stroke-width="2" pathLength="100" stroke-dasharray="14 86">'
         '<animate attributeName="stroke-dashoffset" from="0" to="-100" dur="7s" repeatCount="indefinite"/></rect>',
         f'<g transform="translate(252 46)">{motif(p["motif"])}</g>',
         f'<text class="fg" x="22" y="44" font-size="20" font-weight="800">{esc(p["title"])}</text>']
    for i, ln in enumerate(hook):
        o.append(f'<text class="dim" x="22" y="{74+i*18}" font-size="13">{esc(ln)}</text>')
    o += [f'<text class="a m" x="22" y="124" font-size="10" letter-spacing="1">{esc(p["tags"])}</text>',
          f'<text class="dim m" x="22" y="145" font-size="9">↗ {esc(p["url"].replace("https://", "").rstrip("/")[:44])}</text>']
    return svg(300, 160, "".join(o), f'{p["title"]} project')

# ───────────── 5. SELF-AWARE TERMINAL FOOTER ─────────────
def footer(build):
    C, cw = 18.0, 8.8
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = ["$ while true; do build && learn && ship || retry; done",
             "> exit code: never.  status: still building.",
             f"> compiled by itself · build {build} · {now}"]
    o = ['<rect width="900" height="190" rx="14" fill="var(--card)" stroke="var(--ln)"/>',
         '<circle cx="28" cy="26" r="6" fill="#ff5f56"/><circle cx="50" cy="26" r="6" fill="#ffbd2e"/><circle cx="72" cy="26" r="6" fill="#27c93f"/>',
         f'<text class="dim m" x="450" y="30" font-size="11" text-anchor="middle">{USER}@never-give-up: ~</text><defs>']
    starts, dur = [1.0, 4.5, 7.5], [3.0, 2.2, 3.5]
    for k, ln in enumerate(lines):
        n = len(ln)
        kt, vals = [0, starts[k] / C], [0, 0]
        for i in range(1, n + 1):
            kt.append((starts[k] + dur[k] * i / n) / C); vals.append(f(i * cw))
        kt.append(1); vals.append(f(n * cw))
        o.append(f'<clipPath id="c{k}"><rect x="30" y="{58+k*34}" height="26" width="0"><animate attributeName="width" calcMode="discrete" '
                 f'keyTimes="{";".join(f"{t:.4f}" for t in kt)}" values="{";".join(map(str, vals))}" dur="{C}s" repeatCount="indefinite"/></rect></clipPath>')
    o.append('</defs>')
    for k, ln in enumerate(lines):
        cls = "b" if k == 1 else ("a" if k == 0 else "dim")
        o.append(f'<text class="{cls} m" x="30" y="{76+k*34}" font-size="15" xml:space="preserve" clip-path="url(#c{k})">{esc(ln)}</text>')
    end = starts[2] + dur[2]
    kt, vals, t = [0, end / C], [0, 1], end
    while t + 0.5 < C:
        t += 0.5; kt.append(t / C); vals.append(1 - vals[-1])
    kt.append(1); vals.append(vals[-1])
    o.append(f'<rect x="{f(30+len(lines[2])*cw+3)}" y="{58+2*34+2}" width="9" height="18" class="a" opacity="0">'
             f'<animate attributeName="opacity" calcMode="discrete" keyTimes="{";".join(f"{x:.4f}" for x in kt)}" values="{";".join(map(str, vals))}" dur="{C}s" repeatCount="indefinite"/></rect>')
    return svg(900, 190, "".join(o), "Self-compiling terminal footer")

# ───────────── BUILD ─────────────
def main():
    api = {}
    for r in (gh(f"/users/{USER}/repos?per_page=100") or []):
        if r.get("fork"): continue
        for lang, b in (gh(f"/repos/{USER}/{r['name']}/languages") or {}).items():
            api[lang] = api.get(lang, 0) + b
    floor = 0.12 * max(api.values()) if api else 0
    weights = sorted(((l, max(api.get(l, 0), floor) if api else FALLBACK[l]) for l in PLANETS), key=lambda x: -x[1])
    print("planets:", weights)
    files = {"hero.svg": hero(weights), "pendulum.svg": pendulum()}
    for i, (lab, sub, _) in enumerate(LINKS): files[f"rope_{lab.lower()}.svg"] = rope(lab, sub, i)
    for p in PROJECTS:
        d = (gh(f"/repos/{USER}/{p['repo']}") or {}).get("description") if p["repo"] else None
        files[f"card_{p['slug']}.svg"] = card(p, d)
    build = hashlib.sha256("".join(files.values()).encode()).hexdigest()[:7]
    files["footer.svg"] = footer(build)
    for name, data in files.items():
        (OUT / name).write_text(data, encoding="utf-8")
        print(f"wrote assets/{name}  {len(data)/1024:.1f} KB")

if __name__ == "__main__":
    main()
