import os,sys,math
sys.path.insert(0,os.path.dirname(__file__))
from helpers import *
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
PANEL="#0C1218"
def anim(attr,pts,tag="animate",extra="",dur=15,disc=False):
    kt=";".join(f"{t:.4f}" for t,_ in pts);vs=";".join(str(v) for _,v in pts)
    c=' calcMode="discrete"' if disc else ""
    return f'<{tag} attributeName="{attr}" {extra} values="{vs}" keyTimes="{kt}" dur="{dur}s"{c} repeatCount="indefinite"/>'

# ================= HERO =================
W,H=1000,440
b=head(W,H,"Prasoon Mishra — signal","Animated boot sequence. J.A.R.V.I.S. online, friday standing by, workshop cave, materials box of scraps. The name PRASOON MISHRA is revealed beside an arc-reactor style ring.")+frame(W,H,"00 / signal","clearance: level ∞")
b=b.replace("</defs>",f'<radialGradient id="gl"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".35" stop-color="{SIG}" stop-opacity=".9"/><stop offset="1" stop-color="{SIG}" stop-opacity="0"/></radialGradient></defs>',1)
lines=[("jarvis > online",AMB),("friday > standing by",DIM),("workshop: cave · materials: box_of_scraps",DIM),("suit.version = mark_∞ · power: 400%",INK)]
d=0
for i,(s,col) in enumerate(lines):
    t,n=typed(40,72+i*21,s,d,12,col);b+=t;d+=n+6
tl=d*0.022;last=lines[3][0]
b+=f'<rect x="{40+len(last)*7.2+4}" y="{72+63-11}" width="7" height="13" fill="{AMB}" opacity="0"><animate attributeName="opacity" values="1;0" dur="1s" begin="{tl:.2f}s" repeatCount="indefinite"/></rect>'
tot=tl+1.8
def wipe(i,x,y,w,txt,style,delay):
    return (f'<clipPath id="n{i}"><rect x="{x}" y="{y-120}" width="{w+60}" height="140"><animate attributeName="width" values="0;0;{w+60}" keyTimes="0;{round((tl*0.85+delay)/(tot+delay),3)};1" dur="{round(tot+delay,2)}s" fill="freeze"/></rect></clipPath>'
            f'<text x="{x}" y="{y}" font-family="{SANS}" font-weight="800" font-size="106" textLength="{w}" lengthAdjust="spacingAndGlyphs" {style} clip-path="url(#n{i})">{txt}</text>')
b+=wipe(1,40,240,570,"PRASOON",f'fill="{INK}"',0)+wipe(2,40,352,490,"MISHRA",f'fill="none" stroke="{INK}" stroke-width="1.6"',0.4)
b+=f'<text x="40" y="396" class="f" font-size="21">Sometimes you gotta run before you can walk.</text>'
b+=T(40,422,"// some files stay classified","m")
cx,cy=815,225
b+=f'<path d="M{cx-185} {cy}H{cx+185}M{cx} {cy-185}V{cy+185}" stroke="{LINE}"/>'
b+=f'<circle cx="{cx}" cy="{cy}" r="40" fill="url(#gl)"><animate attributeName="r" values="34;48;34" dur="3.2s" repeatCount="indefinite"/></circle>'
b+=f'<path id="ring" d="M{cx-124} {cy}a124 124 0 1 1 248 0a124 124 0 1 1 -248 0" fill="none"/>'
b+=f'<g><text class="m" font-size="9.5" letter-spacing="1" style="fill:{DIM}"><textPath href="#ring" textLength="770" lengthAdjust="spacing">'+("love you 3000 · "*8)+f'</textPath></text><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="120s" repeatCount="indefinite"/></g>'
tk=""
for i in range(72):
    a=i*math.pi/36;l=9 if i%6==0 else 4;r=104
    tk+=f"M{cx+r*math.cos(a):.1f} {cy+r*math.sin(a):.1f}L{cx+(r-l)*math.cos(a):.1f} {cy+(r-l)*math.sin(a):.1f}"
b+=f'<g><path d="{tk}" stroke="{DIM}" fill="none"/><animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="80s" repeatCount="indefinite"/></g>'
b+=f'<circle cx="{cx}" cy="{cy}" r="88" fill="none" stroke="{SIG}" stroke-opacity=".7"/><circle cx="{cx}" cy="{cy}" r="58" fill="none" stroke="{MID}"/>'
for i in range(10):
    a=i*36
    b+=f'<rect x="{cx-11}" y="{cy-82}" width="22" height="16" rx="2" fill="#10213F" stroke="{SIG}" transform="rotate({a} {cx} {cy})"><animate attributeName="fill-opacity" values="1;.3;1" dur="3s" begin="{i*0.3}s" repeatCount="indefinite"/></rect>'
tri=" ".join(f"{cx+34*math.cos(math.radians(-90+k*120)):.1f},{cy+34*math.sin(math.radians(-90+k*120)):.1f}" for k in range(3))
b+=f'<polygon points="{tri}" fill="none" stroke="{INK}" stroke-width="1.6"><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="30s" repeatCount="indefinite"/></polygon><circle cx="{cx}" cy="{cy}" r="7" fill="#fff"/>'
b+=pulse(f"M{cx+88} {cy}a88 88 0 1 1 -176 0a88 88 0 1 1 176 0",11,0,3.5,AMB)
for sx,sy,dx,dy in [(cx-150,cy-150,1,1),(cx+150,cy-150,-1,1),(cx-150,cy+150,1,-1),(cx+150,cy+150,-1,-1)]:
    b+=f'<path d="M{sx+dx*18} {sy}H{sx}V{sy+dy*18}" stroke="{SIG}" fill="none" stroke-opacity=".6"/>'
b+=T(cx,cy+150+16,"arc: stable","m","middle")
b+=f'<rect x="0" y="0" width="{W}" height="2" fill="{SIG}" opacity=".2"><animateTransform attributeName="transform" type="translate" values="0 0;0 {H}" dur="7s" repeatCount="indefinite"/></rect>'
write("hero",b)

# ================= SKILLS =================
W,H=1000,540
b=head(W,H,"Core approach and stack","Five core strengths: problem solving, algorithm design, database management, CI/CD workflows and automation, each with an animated glyph, followed by foundations, languages, tools and engines.")+frame(W,H,"01 / core","approach → stack")
def gl_problem(x,y):
    P=[(8,62),(40,20),(72,52),(104,16),(136,46)]
    g="".join(f'<path d="M{P[i][0]} {P[i][1]}L{P[i+1][0]} {P[i+1][1]}" stroke="{MID}" stroke-width="2"/>' for i in range(4))
    g+=f'<path d="M8 62L72 52M40 20L104 16M72 52L136 46" stroke="{LINE}" stroke-dasharray="2 3"/>'
    for i,(px,py) in enumerate(P): g+=f'<circle cx="{px}" cy="{py}" r="5" fill="{PANEL}" stroke="{SIG}" stroke-width="1.6"><animate attributeName="stroke" values="{SIG};{AMB};{SIG}" dur="4s" begin="{i*0.6}s" repeatCount="indefinite"/></circle>'
    return g+pulse("M8 62L40 20L72 52L104 16L136 46",4,0,3.5,AMB)
def gl_algo(x,y):
    N=[(72,8),(36,34),(108,34),(18,64),(54,64),(90,64),(126,64)]
    E=[(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]
    g="".join(f'<path d="M{N[a][0]} {N[a][1]}L{N[c][0]} {N[c][1]}" stroke="{MID}" stroke-width="1.6"/>' for a,c in E)
    for px,py in N: g+=f'<circle cx="{px}" cy="{py}" r="5.5" fill="{PANEL}" stroke="{SIG}" stroke-width="1.6"/>'
    return g+pulse("M72 8L36 34L18 64L36 34L54 64L36 34L72 8L108 34L90 64L108 34L126 64",7,0,4,AMB)
def gl_db(x,y):
    g=f'<path d="M32 14V58A40 9 0 0 0 112 58V14M32 36A40 9 0 0 0 112 36" fill="none" stroke="{SIG}" stroke-width="1.6"/><ellipse cx="72" cy="14" rx="40" ry="9" fill="{PANEL}" stroke="{SIG}" stroke-width="1.6"/>'
    g+=f'<rect x="33" y="14" width="78" height="8" fill="{AMB}" opacity=".3"><animateTransform attributeName="transform" type="translate" values="0 0;0 44;0 0" dur="3.6s" repeatCount="indefinite"/></rect>'
    return g+f'<path d="M12 74H132" stroke="{LINE}"/>'
def gl_ci(x,y):
    g=""
    for i,l in enumerate("btld"):
        px=i*40
        g+=f'<rect x="{px}" y="22" width="30" height="30" rx="3" fill="{PANEL}" stroke="{SIG if i<3 else AMB}" stroke-width="1.6"/>'+T(px+15,42,l,"mi","middle",'font-size="12"')
        if i<3: g+=f'<path d="M{px+32} 37H{px+38}" stroke="{SIG}" marker-end="url(#ar)"/>'
    g+=f'<rect x="120" y="22" width="30" height="30" rx="3" fill="{AMB}" opacity="0"><animate attributeName="opacity" values="0;0;.35;0" keyTimes="0;.6;.7;1" dur="4s" repeatCount="indefinite"/></rect>'
    return g+pulse("M-2 37H150",4,0,3.5,AMB)+T(0,72,"build · test · lint · deploy","m")
def gl_auto(x,y):
    pts=[]
    for i in range(8):
        a=i*45
        for da,rr in [(-9,36),(9,36),(15,27),(30,27)]: pts.append((72+rr*math.cos(math.radians(a+da)),40+rr*math.sin(math.radians(a+da))))
    po=" ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    return (f'<g><polygon points="{po}" fill="none" stroke="{SIG}" stroke-width="1.6"/><circle cx="72" cy="40" r="10" fill="none" stroke="{AMB}" stroke-width="1.6"/>'
            f'<animateTransform attributeName="transform" type="rotate" from="0 72 40" to="360 72 40" dur="14s" repeatCount="indefinite"/></g>')
cards=[("problem solving","frame it. break it. prove it.",["requirement analysis","debugging","performance tuning","500+ problems solved"],gl_problem),
 ("algorithm design","pick the right shape.",["data structures","complexity analysis","design patterns · 150+","c++ · java · python"],gl_algo),
 ("database management","model first. query second.",["sql","schema design + modelling","query optimisation","transactional data"],gl_db),
 ("ci/cd workflows","untested is unfinished.",["github actions","matrix test pipelines","regression gates","vercel deploys"],gl_ci),
 ("automation","do it once. never again.",["scripted pipelines","rest api integration","agentic workflows","serverless runtimes"],gl_auto)]
for i,(nm,tag,kw,gf) in enumerate(cards):
    x=20+i*196;y=58
    b+=box(x,y,176,262,MID,PANEL)+T(x+16,y+30,nm,"s","start",'font-size="12.5"')+f'<path d="M{x+16} {y+42}H{x+160}" stroke="{LINE}"/>'
    b+=f'<g transform="translate({x+16},{y+58})">{gf(x,y)}</g>'
    for j,k in enumerate(kw): b+=T(x+16,y+168+j*20,k,"mi","start",'font-size="11"')
    b+=T(x+16,y+250,tag,"f","start",f'font-size="12.5" style="fill:{AMB}"')
b+=f'<path d="M30 340H{W-30}" stroke="{LINE}"/>'
rowsS=[("foundations",["data structures","operating systems","computer architecture","oop (c++)","unit testing","agile"]),
 ("languages",["c++","java","python","javascript es6+","sql","html5 / css3","c#"]),
 ("platforms",["git","github actions","node.js","react","next.js","rest apis","openai api","aws","vercel"]),
 ("engines",["unity","unreal engine","blender"])]
ci=0
for r,(lab,chips) in enumerate(rowsS):
    y=358+r*40;b+=T(40,y+17,lab,"m");x=150
    for c in chips:
        w=len(c)*7+22
        b+=box(x,y,w,26,MID,"none",None,13)+f'<circle cx="{x+11}" cy="{y+13}" r="2.5" fill="{SIG}"><animate attributeName="opacity" values="1;.2;1" dur="3s" begin="{(ci%9)*0.35}s" repeatCount="indefinite"/></circle>'+T(x+19,y+17,c,"mi","start",'font-size="11.5"')
        x+=w+10;ci+=1
write("skills",b)

# ================= MANIFESTO =================
W,H=1000,430
b=head(W,H,"Drive","A short brief on a builder driven by tools, solutions, agentic AI and game development, beside an orbit diagram of those four domains.")+frame(W,H,"02 / drive","classified")
para=["Some people see a problem and walk away.","I see an unfinished machine.","",
 "Give me a cave, a box of scraps, and a deadline.","I'll hand back a tool, a system, an agent that","works while you sleep — or a world you can walk into.","",
 "Sleep is a deprecated feature.","Every prototype is waiting for its Mark II."]
y=92;k=0
for s in para:
    if s:
        a=0.3+k*0.55;en=a+0.7;tot=en+0.01
        b+=f'<text x="50" y="{y}" class="f" font-size="20"><animate attributeName="opacity" values="0;0;1" keyTimes="0;{a/tot:.3f};1" dur="{tot:.2f}s" fill="freeze"/>{esc(s)}</text>'
        k+=1
    y+=32 if s else 18
b+=T(50,H-30,"and part of the journey is the end.","m")
cx,cy=775,225
b+=f'<circle cx="{cx}" cy="{cy}" r="125" fill="none" stroke="{MID}" stroke-dasharray="2 6"><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="90s" repeatCount="indefinite"/></circle><circle cx="{cx}" cy="{cy}" r="62" fill="none" stroke="{SIG}" stroke-opacity=".5"/>'
b+=f'<circle cx="{cx}" cy="{cy}" r="28" fill="url(#gl)" opacity=".7"/>'+T(cx,cy+11,"∞","f","middle",f'font-size="34" style="fill:{AMB}"')
doms=[(0,-125,"software tools","things that remove work"),(125,0,"solutions","problem → working system"),(0,125,"agentic ai","models that take action"),(-125,0,"game dev","worlds with rules")]
for dx,dy,nm,sub in doms:
    px,py=cx+dx,cy+dy;w=len(nm)*7.6+26
    b+=f'<path d="M{cx} {cy}L{px} {py}" stroke="{MID}"/>'+box(px-w/2,py-14,w,28,SIG,"#10213F",None,14)+T(px,py+4,nm,"mi","middle",'font-size="12.5"')
    b+=T(px,py+(30 if dy>=0 else -22),sub,"m","middle",'font-size="10"')
b+=pulse(f"M{cx+125} {cy}a125 125 0 1 1 -250 0a125 125 0 1 1 250 0",14,0,4,AMB)+pulse(f"M{cx+62} {cy}a62 62 0 1 0 -124 0a62 62 0 1 0 124 0",8,0,3,SIG)
write("manifesto",b)

# ================= PANDA =================
W,H=300,230
b=head(W,H,"Gaming panda","A headset-wearing panda takes bites of a burger. After each bite a role card appears in front of its mouth: Game Programmer, Blender, Unreal Engine, Game Designer, Unity.")+frame(W,H,"","")
N=5
t=lambda c,f:(c+f)/N
def uniq(p):
    o=[]
    for a in p:
        if o and abs(o[-1][0]-a[0])<1e-6: o[-1]=a
        else: o.append(a)
    return o
# burger
bx,by=170,100
cx0=anim("x",[(0,0)]+[(t(c,.14),14*(c+1)) for c in range(N)],"animate","",15,True)
burger=(f'<clipPath id="bc"><rect x="0" y="-5" width="100" height="70">{cx0}</rect></clipPath><g transform="translate({bx},{by})"><g clip-path="url(#bc)">'
 '<path d="M0 22Q0 0 45 0Q90 0 90 22Z" fill="#E0A050"/><ellipse cx="25" cy="9" rx="3" ry="1.6" fill="#F6E3B4"/><ellipse cx="46" cy="6" rx="3" ry="1.6" fill="#F6E3B4"/><ellipse cx="66" cy="10" rx="3" ry="1.6" fill="#F6E3B4"/>'
 '<path d="M0 22H90V27Q80 33 70 27T50 27T30 27T10 27T0 29Z" fill="#6BBF59"/><path d="M2 29H88L80 36H10Z" fill="#FFB347"/>'
 '<rect x="0" y="34" width="90" height="12" rx="6" fill="#6B3A24"/><path d="M0 46H90V50Q90 56 80 56H10Q0 56 0 50Z" fill="#E0A050"/></g>')
for c in range(N):
    for yy in (10,28,46):
        burger+=f'<circle cx="{14*(c+1)+2}" cy="{yy}" r="9" fill="{BG}" opacity="0">'+anim("opacity",[(0,0),(t(c,.14),1)],"animate","",15,True)+'</circle>'
b+=burger+'</g>'
DARK="#14181E";WH="#F4F6F8"
b+=f'<ellipse cx="100" cy="182" rx="50" ry="40" fill="{WH}"/><ellipse cx="60" cy="176" rx="11" ry="22" fill="{DARK}" transform="rotate(15 60 176)"/>'
b+=f'<path d="M142 170L180 150" stroke="{DARK}" stroke-width="20" stroke-linecap="round"/><circle cx="182" cy="150" r="11" fill="{DARK}"/>'
hd=anim("transform",uniq([(0,"0 0")]+[p for c in range(N) for p in [(t(c,.12),"40 3"),(t(c,.22),"40 3"),(t(c,.34),"0 0")]]+[(1,"0 0")]),"animateTransform",'type="translate"',15)
mo=anim("ry",uniq([(0,1.5)]+[p for c in range(N) for p in [(t(c,.07),1.5),(t(c,.1),9),(t(c,.2),9),(t(c,.24),1.5)]]+[(1,1.5)]),"animate","",15)
b+=(f'<g>{hd}<circle cx="62" cy="50" r="16" fill="{DARK}"/><circle cx="138" cy="50" r="16" fill="{DARK}"/><circle cx="100" cy="88" r="46" fill="{WH}"/>'
 f'<path d="M55 86A45 45 0 0 1 145 86" fill="none" stroke="{SIG}" stroke-width="5"/><rect x="47" y="76" width="11" height="26" rx="4" fill="{SIG}"/><rect x="142" y="76" width="11" height="26" rx="4" fill="{SIG}"/>'
 f'<ellipse cx="82" cy="86" rx="11" ry="15" fill="{DARK}" transform="rotate(20 82 86)"/><ellipse cx="118" cy="86" rx="11" ry="15" fill="{DARK}" transform="rotate(-20 118 86)"/>'
 f'<circle cx="83" cy="84" r="4.5" fill="#fff"/><circle cx="117" cy="84" r="4.5" fill="#fff"/><circle cx="84" cy="85" r="2" fill="{DARK}"/><circle cx="118" cy="85" r="2" fill="{DARK}"/>'
 f'<ellipse cx="100" cy="101" rx="7" ry="5" fill="{DARK}"/><ellipse cx="100" cy="112" rx="9" ry="1.5" fill="#7A2230">{mo}</ellipse>'
 f'<path d="M52 100Q50 128 86 124" fill="none" stroke="{SIG}" stroke-width="2.5"/><circle cx="88" cy="124" r="4" fill="{AMB}"/></g>')
roles=["Game Programmer","Blender","Unreal Engine","Game Designer","Unity"]
for c,rn in enumerate(roles):
    op=uniq([(0,0),(t(c,.36),0),(t(c,.42),1),(t(c,.88),1),(t(c,.95),0),(1,0)])
    ty=uniq([(0,"0 6"),(t(c,.36),"0 6"),(t(c,.42),"0 0"),(t(c,.88),"0 0"),(t(c,.95),"0 -4"),(1,"0 6")])
    b+=(f'<g transform="translate(35,134)"><g opacity="0">{anim("opacity",op)}{anim("transform",ty,"animateTransform",chr(116)+"ype=\"translate\"",15)}'
        f'<rect width="130" height="36" rx="5" fill="{PANEL}" stroke="{SIG}"/><text x="65" y="14" class="ma" text-anchor="middle" font-size="8.5">role unlocked</text>'
        f'<text x="65" y="29" class="s" text-anchor="middle" font-size="11">{rn}</text></g></g>')
write("panda",b)
