import math
BG="#090D12";INK="#E8ECF1";DIM="#6B7A8C";LINE="#1B2430";MID="#2A3849";SIG="#5B8CFF";AMB="#FFB347"
MONO="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS="'Helvetica Neue',Helvetica,Arial,'Segoe UI',sans-serif"
SERIF="Georgia,'Times New Roman',serif"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def head(W,H,title,desc):
    mk=lambda i,c:f'<marker id="{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">'
      f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc><defs>'
      f'<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#18212C"/></pattern>'
      +mk("ar",SIG)+mk("ard",DIM)+mk("ara",AMB)+'</defs>'
      f'<style>.m{{font-family:{MONO};font-size:11px;fill:{DIM}}}.mi{{font-family:{MONO};font-size:12px;fill:{INK}}}'
      f'.ma{{font-family:{MONO};font-size:10.5px;fill:{AMB}}}.s{{font-family:{SANS};font-weight:700;fill:{INK}}}'
      f'.f{{font-family:{SERIF};font-style:italic;fill:{INK}}}</style>')
def frame(W,H,code,label):
    c=""
    for (x,y,dx,dy) in [(0,0,1,1),(W,0,-1,1),(0,H,1,-1),(W,H,-1,-1)]:
        c+=f'<path d="M{x+dx*10} {y+dy*2}H{x+dx*22}M{x+dx*2} {y+dy*10}V{y+dy*22}" stroke="{DIM}" fill="none"/>'
    return (f'<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#dots)"/>'
      f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" fill="none" stroke="{LINE}"/>{c}'
      f'<text x="30" y="34" class="m" fill="{SIG}" style="fill:{SIG}">{esc(code)}</text>'
      f'<text x="{W-30}" y="34" class="m" text-anchor="end">{esc(label)}</text>')
def T(x,y,s,cls="m",anc=None,extra=""):
    a=f' text-anchor="{anc}"' if anc else ""
    return f'<text x="{x}" y="{y}" class="{cls}"{a} {extra}>{esc(s)}</text>'
def box(x,y,w,h,stroke=SIG,fill="none",dash=None,rx=2):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"{d}/>'
def pulse(path,dur,begin=0,r=3,col=SIG):
    return (f'<circle r="{r}" fill="{col}"><animateMotion path="{path}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>')
def write(n,body):
    open(f"assets/{n}.svg","w",encoding="utf-8").write(body+"</svg>\n")
cid=[0]
def typed(x,y,s,delay,fs=12,fill=INK,step=0.022):
    cid[0]+=1;n=len(s);cw=fs*0.6;W=round(n*cw,1)
    vals=[0]*delay+[round(i*cw,1) for i in range(1,n+1)]
    dur=round(len(vals)*step,2)
    return (f'<clipPath id="c{cid[0]}"><rect x="{x}" y="{y-fs-2}" width="{W}" height="{fs+8}"><animate attributeName="width" values="{";".join(map(str,vals))}" dur="{dur}s" calcMode="discrete" fill="freeze"/></rect></clipPath>'
      f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{fill}" textLength="{W}" lengthAdjust="spacing" clip-path="url(#c{cid[0]})">{esc(s)}</text>'),len(vals)

