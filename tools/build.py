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

# ---------- HERO ----------
W,H=1000,450
b=head(W,H,"Prasoon Mishra — signal","Animated boot sequence revealing the name Prasoon Mishra beside orbital rings labelled core, systems and worlds.")+frame(W,H,"00 / signal","26.8467°N 80.9462°E")
lines=[("$ boot --identity prasoon",AMB),("mount /dsa /os /architecture /worlds ............ ok",DIM),("load pattern_library[150+] ........... verified",DIM),("signal: building",INK)]
d=0;ends=[]
for i,(s,col) in enumerate(lines):
    t,n=typed(40,72+i*21,s,d,12,col);b+=t;ends.append((s,d+n));d+=n+6
tl=d*0.022
cx,cy=815,225
b+=f'<rect x="{40+len(lines[3][0])*7.2+4}" y="{72+63-11}" width="7" height="13" fill="{AMB}" opacity="0"><animate attributeName="opacity" values="1;0" dur="1s" begin="{tl:.2f}s" repeatCount="indefinite"/></rect>'
# name wipes
tot=tl+1.8;k=round(tl/tot*0.9,3)
def wipe(i,x,y,w,txt,style,delay):
    return (f'<clipPath id="n{i}"><rect x="{x}" y="{y-120}" width="{w+60}" height="140"><animate attributeName="width" values="0;0;{w+60}" keyTimes="0;{round((tl*0.85+delay)/(tot+delay),3)};1" dur="{round(tot+delay,2)}s" fill="freeze"/></rect></clipPath>'
            f'<text x="{x}" y="{y}" font-family="{SANS}" font-weight="800" font-size="106" textLength="{w}" lengthAdjust="spacingAndGlyphs" {style} clip-path="url(#n{i})">{txt}</text>')
b+=wipe(1,40,240,570,"PRASOON",f'fill="{INK}"',0)
b+=wipe(2,40,352,490,"MISHRA",f'fill="none" stroke="{INK}" stroke-width="1.6"',0.4)
b+=f'<text x="40" y="396" class="f" font-size="22">I build the rules that worlds run on.</text>'
b+=T(40,422,"status: building   domain: algorithms → systems → worlds   since: 2024.09","m","start",'xml:space="preserve"')
# device
b+=f'<path d="M{cx-175} {cy}H{cx+175}M{cx} {cy-175}V{cy+175}" stroke="{LINE}"/>'
tk=""
for i in range(72):
    a=i*math.pi/36;l=10 if i%6==0 else 5;r=140
    tk+=f"M{cx+r*math.cos(a):.1f} {cy+r*math.sin(a):.1f}L{cx+(r-l)*math.cos(a):.1f} {cy+(r-l)*math.sin(a):.1f}"
b+=f'<g><path d="{tk}" stroke="{DIM}" fill="none"/><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="90s" repeatCount="indefinite"/></g>'
b+=f'<circle cx="{cx}" cy="{cy}" r="100" fill="none" stroke="{MID}" stroke-dasharray="2 6"><animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="60s" repeatCount="indefinite"/></circle>'
b+=f'<circle cx="{cx}" cy="{cy}" r="60" fill="none" stroke="{SIG}" stroke-opacity=".6"/>'
b+=f'<rect x="{cx-14}" y="{cy-14}" width="28" height="28" fill="none" stroke="{AMB}"><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="90 {cx} {cy}" dur="6s" repeatCount="indefinite"/></rect><circle cx="{cx}" cy="{cy}" r="3" fill="{AMB}"/>'
for r,dur,col in [(60,9,SIG),(100,16,INK),(140,26,AMB)]:
    p=f"M{cx+r} {cy}a{r} {r} 0 1 1 {-2*r} 0a{r} {r} 0 1 1 {2*r} 0"
    b+=pulse(p,dur,0,3.5,col)
b+=T(cx,cy-64,"core · dsa os arch","m","middle")+T(cx,cy-104,"systems · ci/cd api cloud","m","middle")+T(cx,cy-144,"worlds · unity unreal blender","m","middle")
b+=f'<rect x="0" y="0" width="{W}" height="2" fill="{SIG}" opacity=".22"><animateTransform attributeName="transform" type="translate" values="0 0;0 {H}" dur="7s" repeatCount="indefinite"/></rect>'
b+=f'<text x="{W-30}" y="{H-14}" class="m" text-anchor="end">signal received<tspan fill="{AMB}"> ▮</tspan><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></text>'
write("hero",b)

# ---------- IDENTITY / PIPELINE ----------
W,H=1000,360
b=head(W,H,"How the work moves","Six-stage pipeline: problem, abstraction, pattern, implementation, verification, world, with an iteration loop back to the start.")+frame(W,H,"01 / identity","pipeline: problem → world")
xs=[90,255,420,585,750,915];y=150
st=[("problem","requirements","impact analysis",None),("abstraction","dsa · 500+ solved","leetcode",None),("pattern","150+ design patterns","awesome-Modern-SE-Algorithms",None),
    ("implementation","c++ · java · python","javascript · sql",None),("verification","github actions","5 languages at once",None),("world","vercel deploys","unity · unreal",None)]
for x in xs: b+=f'<path d="M{x} 70V300" stroke="{LINE}" stroke-dasharray="2 5"/>'
b+=f'<path d="M{xs[0]} {y}H{xs[-1]}" stroke="{MID}" stroke-width="2"/>'
for i,x in enumerate(xs):
    n,l1,l2,_=st[i]
    b+=f'<circle cx="{x}" cy="{y}" r="9" fill="{BG}" stroke="{SIG}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="3" fill="{AMB if i==5 else SIG}"/>'
    b+=T(x,y-34,n,"s","middle",'font-size="16"')+T(x,y+38,l1,"mi","middle")+T(x,y+56,l2,"m","middle")
    if i<5: b+=f'<path d="M{x+16} {y}H{xs[i+1]-18}" stroke="{SIG}" marker-end="url(#ar)"/>'
b+=pulse(f"M{xs[0]} {y}H{xs[-1]}",8,0,4,AMB)
b+=f'<path d="M{xs[-1]} {y+78}V318H{xs[0]}V{y+78}" fill="none" stroke="{DIM}" stroke-dasharray="4 4" marker-end="url(#ard)"/>'
b+=T(500,336,"iterate — every world raises the next problem","f","middle",'font-size="15"')
write("identity",b)

# ---------- ARCHITECTURE ----------
W,H=1000,630
b=head(W,H,"Capability architecture","Human intent branches into four capability columns — compute, systems, data and cloud, worlds — converging on architecture, implementation and measured impact.")+frame(W,H,"02 / capability","intent → architecture → impact")
b+=box(380,48,240,44,SIG)+T(500,68,"human intent","s","middle",'font-size="14"')+T(500,83,"a problem worth a system","m","middle")
cols=[("compute",["c++ · java · python","dsa · 500+ solved","operating systems","computer architecture"],"↳ leetcode.com/u/iprsnmsra"),
      ("systems",["design patterns · 150+","rest apis","ci/cd · github actions","testing · debugging"],"↳ awesome-Modern-SE-Algorithms"),
      ("data + cloud",["sql schema design","query optimisation","vercel · aws","node.js · next.js"],"↳ AnimeBill · Kestrel AI"),
      ("worlds",["unity · unreal","blender · c#","storytelling","game production"],"↳ matrix-decrypter.vercel.app")]
for i,(nm,ls,ev) in enumerate(cols):
    x=20+i*250;c=x+105
    p=f"M500 92V121H{c}V150"
    b+=f'<path d="{p}" fill="none" stroke="{SIG}" marker-end="url(#ar)"/>'+pulse(p,4,i*0.6,3)
    b+=box(x,150,210,172,MID,"#0C1218")+T(x+16,178,nm,"s","start",'font-size="15"')+f'<path d="M{x+16} 190H{x+194}" stroke="{LINE}"/>'
    for j,l in enumerate(ls): b+=T(x+16,214+j*24,l,"mi")
    b+=T(x+16,308,ev,"ma")
    b+=f'<path d="M{c} 322V396" stroke="{DIM}" marker-end="url(#ard)"/>'
b+=box(20,398,960,44,SIG,"#0C1218")+T(40,425,"architecture","s","start",'font-size="16"')+T(960,425,"a model of decisions","m","end")
b+=f'<path d="M500 442V476" stroke="{SIG}" marker-end="url(#ar)"/>'+box(280,478,440,44,MID,"#0C1218")+T(500,498,"implementation","s","middle",'font-size="14"')+T(500,513,"code · tests · deploys","m","middle")
b+=f'<path d="M500 522V558" stroke="{SIG}" marker-end="url(#ar)"/>'
for i,s in enumerate(["500+ students · hackathons · webinars","hack secure · 3rd place · kestrel ai","ey hackathon · finalist · tata capital"]):
    x=35+i*320;b+=box(x,560,290,34,AMB,"none",None,17)+T(x+145,581,s,"ma","middle")
b+=T(30,H-12,"impact = evidence, not adjectives","m")
write("architecture",b)

# ---------- SKILL NETWORK ----------
W,H=1000,520
b=head(W,H,"Skill network","Technologies as a graph. Solid outlines are used in a shipped project; dashed outlines are declared skills. Edges name the relationship.")+frame(W,H,"03 / network","technology → role → relationship")
N={"Unity":(110,150,0),"Unreal":(110,270,0),"Blender":(200,350,0),"C#":(250,210,0),"C++":(370,270,1),"Java":(370,120,1),"Python":(290,425,0),
 "Git":(540,270,1),"GitHub Actions":(540,130,1),"SQL":(540,400,1),"JavaScript":(700,300,1),"Node.js":(700,170,1),"Next.js":(820,110,1),"React":(935,190,0),"OpenAI API":(925,300,1),"Vercel":(820,400,1),"AWS":(680,455,0)}
E=[("Unity","C#","scripting"),("Unreal","C++","engine code"),("Blender","Unity","assets"),("Blender","Unreal",None),("GitHub Actions","Java","ci"),("GitHub Actions","C++","ci"),("Git","GitHub Actions",None),
   ("JavaScript","Node.js",None),("Node.js","Next.js",None),("Next.js","React",None),("Next.js","Vercel","deploy"),("Node.js","OpenAI API","rest"),("SQL","JavaScript","billing"),("AWS","Vercel","cloud")]
for a,c,l in E:
    (x1,y1,_),(x2,y2,_)=N[a],N[c]
    b+=f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{MID}"/>'
    if l: b+=T((x1+x2)/2,(y1+y2)/2-6,l,"ma","middle")
for a in ["Python"]:
    for c in ["C++","Java"]:
        (x1,y1,_),(x2,y2,_)=N[a],N[c];b+=f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{MID}" stroke-dasharray="3 5"/>'
for pa,du in [("M820 110L700 170",5),("M700 170L925 300",6),("M540 130L370 120",5)]: b+=pulse(pa,du,0,3,AMB)
for k,(x,y,s) in N.items():
    w=len(k)*7+24
    b+=(f'<rect x="{x-w/2}" y="{y-14}" width="{w}" height="28" rx="14" fill="{"#10213F" if s else BG}" stroke="{SIG if s else DIM}"'+('' if s else ' stroke-dasharray="3 3"')+'/>')
    b+=T(x,y+4,k,"mi","middle",'font-size="12"' if s else f'font-size="12" style="fill:{DIM}"')
b+=T(110,490,"worlds","f","middle",'font-size="16" style="fill:#6B7A8C"')+T(450,490,"core","f","middle",'font-size="16" style="fill:#6B7A8C"')+T(790,490,"web + cloud","f","middle",'font-size="16" style="fill:#6B7A8C"')
b+=f'<rect x="640" y="52" width="26" height="14" rx="7" fill="#10213F" stroke="{SIG}"/>'+T(674,63,"used in a shipped project","m")
b+=f'<rect x="640" y="72" width="26" height="14" rx="7" fill="none" stroke="{DIM}" stroke-dasharray="3 3"/>'+T(674,83,"declared skill / in progress","m")
write("skill-network",b)

# ---------- BUILDS ----------
W,H=1000,610
b=head(W,H,"Projects as systems","Four builds drawn as boundaries and data flow: Kestrel AI, awesome-Modern-SE-Algorithms, AnimeBill, and the Tata Capital agent.")+frame(W,H,"04 / builds","system boundary → evidence")
rows=[("Kestrel AI",["next.js · node.js · openai api","rest · vercel"],["next.js ui","rest · node","openai api"],"vercel · serverless",
       ["hack secure · 3rd place","real-time detection logic","↳ KESTERAL-AI-Threat-Analyzer"]),
      ("awesome-Modern-SE-Algorithms",["c++ · java · git","github actions · unit tests"],["patterns","git","ci matrix","tests ×5"],"github",
       ["150+ patterns · 5-language ci","regressions caught on push","↳ awesome-Modern-SE-Algorithms"]),
      ("AnimeBill",["html5 · css3 · vanilla js","sql"],["html/css/js","app layer","sql schema"],None,
       ["schema → queries → working app","anime-themed billing ui",""]),
      ("Tata Capital agent",["nlp · chatbot","agentic assistant"],["query","nlp agent","answer"],None,
       ["ey hackathon · finalist","built for tata capital",""])]
for r,(nm,stk,ch,bd,ev) in enumerate(rows):
    y0=58+r*136
    if r: b+=f'<path d="M30 {y0-8}H{W-30}" stroke="{LINE}"/>'
    b+=T(40,y0+36,f"b{r+1}","m")+T(70,y0+38,nm,"s","start",'font-size="'+("13.5" if len(nm)>20 else "20")+'"')
    for j,s in enumerate(stk): b+=T(70,y0+64+j*17,s,"m")
    n=len(ch);gap=24;bw=(340-(n-1)*gap)/n;cy=y0+68
    if bd: b+=box(335,y0+34,360,74,MID,"none","4 4")+T(343,y0+122,bd,"m")
    for i,l in enumerate(ch):
        x=345+i*(bw+gap)
        b+=box(x,cy-18,bw,36,SIG,"#0C1218")+T(x+bw/2,cy+4,l,"mi","middle",'font-size="10"')
        if i<n-1: b+=f'<path d="M{x+bw+3} {cy}H{x+bw+gap-3}" stroke="{SIG}" marker-end="url(#ar)"/>'
    b+=pulse(f"M345 {cy}H{345+340}",3.5+r*.4,r*.5,3,AMB)
    for j,s in enumerate(ev): b+=T(720,y0+52+j*18,s,["mi","m","ma"][j])
write("builds",b)

# ---------- GENOME ----------
W,H=1000,310
b=head(W,H,"Engineering genome","Two strands — rigor and imagination — crossing at four named projects.")+frame(W,H,"05 / genome","rigor × imagination")
def strand(ph):
    return [(x,160+62*math.sin(2*math.pi*(x-100)/240+ph)) for x in range(40,961,4)]
A=strand(math.pi/2*0);B=strand(math.pi)
for i in range(0,len(A),5): b+=f'<path d="M{A[i][0]} {A[i][1]:.1f}V{B[i][1]:.1f}" stroke="{MID}" stroke-opacity=".6"/>'
pa="M"+"L".join(f"{x} {y:.1f}" for x,y in A);pb="M"+"L".join(f"{x} {y:.1f}" for x,y in B)
b+=f'<path d="{pa}" fill="none" stroke="{SIG}" stroke-width="2"/><path d="{pb}" fill="none" stroke="{AMB}" stroke-width="2"/>'
b+=pulse(pa,12,0,3.5,INK)+pulse(pb,12,3,3.5,INK)
for x,nm,sub in [(100,"matrix-decrypter","game × terminal"),(340,"KESTERAL-AI-Threat-Analyzer","security × generative ai"),(580,"awesome-Modern-SE-Algorithms","design × verification"),(820,"AnimeBill","sql × anime sketches")]:
    w=len(nm)*6.6+20
    b+=f'<path d="M{x} 98V222" stroke="{INK}"/><rect x="{x-w/2}" y="143" width="{w}" height="34" fill="{BG}" stroke="{INK}" stroke-opacity=".4"/>'
    b+=T(x,158,nm,"mi","middle",'font-size="10.5"')+T(x,171,sub,"m","middle",'font-size="9.5"')
b+=T(40,60,"rigor strand · dsa · os · ci/cd · tests","m","start",f'style="fill:{SIG}"')+T(960,60,"imagination strand · story · worlds · aesthetics","m","end",f'style="fill:{AMB}"')
b+=T(500,292,"the interesting part is where they cross.","f","middle",'font-size="16"')
write("genome",b)

# ---------- EVOLUTION ----------
W,H=1000,720
b=head(W,H,"Evolution of tools","Six pairs of human ability and the artifact it was externalized into: hands to tool, memory to writing, calculation to computer, distance to network, reasoning to intelligence, imagination to worlds. A question mark follows: whoever holds all of these builds what comes next.")+frame(W,H,"06 / evolution","ability → artifact → ability")
rowsE=[("hands","force and reach","tool","stone → lever",None),("memory","what we know","writing","memory outside the skull",None),
 ("calculation","logic by hand","computer","logic that runs unattended","↳ dsa · os · computer architecture"),
 ("distance","reach by travel","network","reach without travel",None),
 ("reasoning","thought at human speed","intelligence","reasoning at scale","↳ openai api · aws ai practitioner"),
 ("imagination","worlds in the head","worlds","imagination you can enter","↳ unity · unreal · blender")]
ys=[620,530,440,350,260,170]
b+=f'<path d="M500 {ys[0]}V104" stroke="{MID}" stroke-width="2"/><path d="M500 {ys[-1]}V102" stroke="{SIG}" marker-end="url(#ar)"/>'
b+=pulse(f"M500 {ys[0]}V104",9,0,4,AMB)
for (ab,s1,ar,s2,ev),y in zip(rowsE,ys):
    b+=T(380,y+2,ab,"s","end",'font-size="19"')+T(380,y+19,s1,"m","end")
    b+=f'<path d="M396 {y}H606" stroke="{DIM}" stroke-dasharray="3 4" marker-end="url(#ard)"/>'
    b+=f'<circle cx="500" cy="{y}" r="10" fill="{BG}" stroke="{SIG}" stroke-width="2"/><circle cx="500" cy="{y}" r="3" fill="{SIG}"/>'
    b+=T(620,y+2,ar,"s","start",'font-size="19"')+T(620,y+19,s2,"m")
    if ev: b+=T(620,y+36,ev,"ma")
b+=T(500,ys[0]+42,"t = 0 · stone","m","middle")
b+=f'<circle cx="500" cy="70" r="26" fill="none" stroke="{AMB}" stroke-dasharray="4 4"><animateTransform attributeName="transform" type="rotate" from="0 500 70" to="360 500 70" dur="40s" repeatCount="indefinite"/></circle>'
b+=T(500,80,"?","f","middle",f'font-size="30" style="fill:{AMB}"')
b+=T(458,66,"collaboration,","m","end")+T(458,80,"not replacement","m","end")+T(542,70,"next: built by whoever holds all of it","f","start",'font-size="15"')
b+=f'<path d="M60 {ys[-1]}V{ys[0]}" stroke="{DIM}" marker-end="url(#ard)"/><path d="M940 {ys[0]}V{ys[-1]}" stroke="{DIM}" marker-end="url(#ard)"/>'
b+=T(44,395,"tools change the people who hold them","m","middle",'transform="rotate(-90 44 395)"')+T(956,395,"people build better tools","m","middle",'transform="rotate(90 956 395)"')
write("evolution",b)

# ---------- FOOTER ----------
W,H=1000,320
b=head(W,H,"System complete","Closing signature: build boldly, question everything, leave better systems behind. I am Iron Man.")+frame(W,H,"07 / closure","system complete")
cx,cy=140,165
b+=f'<circle cx="{cx}" cy="{cy}" r="78" fill="none" stroke="{MID}"/><circle cx="{cx}" cy="{cy}" r="56" fill="none" stroke="{SIG}" stroke-opacity=".7"/>'
for i in range(10):
    a=i*math.pi/5;b+=f'<path d="M{cx+30*math.cos(a):.1f} {cy+30*math.sin(a):.1f}L{cx+54*math.cos(a):.1f} {cy+54*math.sin(a):.1f}" stroke="{SIG}" stroke-width="5" stroke-opacity=".8"/>'
b+=f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="{AMB}" stroke-width="2"><animate attributeName="r" values="22;26;22" dur="3s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="1;.4;1" dur="3s" repeatCount="indefinite"/></circle><circle cx="{cx}" cy="{cy}" r="8" fill="{AMB}"/>'
for i,s in enumerate(["Build boldly.","Question everything.","Leave better systems behind."]): b+=T(290,120+i*38,s,"f","start",'font-size="28"')
b+=f'<path d="M290 252H960" stroke="{LINE}"/>'+T(960,290,"“I am Iron Man.”","s","end",'font-size="26" font-style="italic"')+f'<path d="M800 298H960" stroke="{SIG}" stroke-width="2"/>'
b+=T(290,276,"Boku'wa-rekishi ,o tsukuru tame'ni iru, ichibu de-wa nai ≈ ∞","m")+T(290,293,"i exist to make history, not to be a part of it.","m","start",f'style="fill:{AMB}"')
write("footer",b)
