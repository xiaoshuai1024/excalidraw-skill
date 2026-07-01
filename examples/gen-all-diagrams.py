#!/usr/bin/env python3
"""Generate all 64 diagram types as .excalidraw scenes. Professional notation."""
import json, sys

PID=[0]
def nid(): PID[0]+=1; return f"e{PID[0]}"

def base(**kw):
    d={"angle":0,"strokeColor":"#1e1e1e","backgroundColor":"transparent","fillStyle":"solid",
       "strokeWidth":2,"strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],
       "roundness":None,"seed":None,"version":1,"versionNonce":None,"isDeleted":False,
       "boundElements":[],"updated":1,"link":None,"locked":False}
    d.update(kw); return d

def box(x,y,w,h,label,fill="#a5d8ff",fs=14,dashed=False,stroke="#1e1e1e",roundness={"type":3}):
    b=base(type="rectangle",id=nid(),x=x,y=y,width=w,height=h,backgroundColor=fill,strokeColor=stroke,
           roundness=roundness,strokeStyle="dashed" if dashed else "solid")
    t=base(type="text",id=nid(),x=x+w/2,y=y+h/2,width=80,height=24,fontSize=fs,fontFamily=1,
           textAlign="center",verticalAlign="middle",containerId=b["id"],text=label,
           originalText=label,lineHeight=1.25)
    b["boundElements"]=[{"id":t["id"],"type":"text"}]
    return [b,t]

def ellipse(x,y,w,h,label,fill="#b2f2bb",fs=14):
    e=base(type="ellipse",id=nid(),x=x,y=y,width=w,height=h,backgroundColor=fill)
    t=base(type="text",id=nid(),x=x+w/2,y=y+h/2,width=50,height=20,fontSize=fs,fontFamily=1,
           textAlign="center",verticalAlign="middle",containerId=e["id"],text=label,
           originalText=label,lineHeight=1.25)
    e["boundElements"]=[{"id":t["id"],"type":"text"}]
    return [e,t]

def diamond(x,y,w,h,label,fill="#ffec99",fs=12):
    d=base(type="diamond",id=nid(),x=x,y=y,width=w,height=h,backgroundColor=fill)
    t=base(type="text",id=nid(),x=x+w/2,y=y+h/2,width=50,height=24,fontSize=fs,fontFamily=1,
           textAlign="center",verticalAlign="middle",containerId=d["id"],text=label,
           originalText=label,lineHeight=1.25)
    d["boundElements"]=[{"id":t["id"],"type":"text"}]
    return [d,t]

def arrow(x1,y1,x2,y2,dashed=False,color="#1e1e1e"):
    # Returns a single-element list so `e += arrow(...)` appends the element
    # (list += dict would silently iterate the dict's KEYS — a Python gotcha).
    return [base(type="arrow",id=nid(),x=x1,y=y1,width=x2-x1,height=y2-y1,strokeColor=color,
                roundness={"type":2},strokeStyle="dashed" if dashed else "solid",
                startBinding=None,endBinding=None,lastCommittedPoint=None,
                startArrowhead=None,endArrowhead="arrow",points=[[0,0],[x2-x1,y2-y1]])]

def line(x1,y1,x2,y2,dashed=False,color="#1e1e1e"):
    return [base(type="line",id=nid(),x=x1,y=y1,width=x2-x1,height=y2-y1,roundness={"type":2},
                strokeStyle="dashed" if dashed else "solid",strokeColor=color,
                lastCommittedPoint=None,points=[[0,0],[x2-x1,y2-y1]])]

def polyline(pts,dashed=False,color="#1e1e1e"):
    # Continuous multi-segment line through absolute points [[x,y],...].
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    x0,y0=xs[0],ys[0]
    rel=[[x-x0,y-y0] for x,y in pts]
    return [base(type="line",id=nid(),x=x0,y=y0,
                width=max(xs)-min(xs),height=max(ys)-min(ys),roundness={"type":2},
                strokeStyle="dashed" if dashed else "solid",strokeColor=color,
                lastCommittedPoint=None,points=rel)]

def dot(cx,cy,r=6,color="#1e1e1e",fill="#ffffff"):
    # A small commit-node circle, r = radius. Excalidraw ellipse x/y is top-left.
    d=ellipse(cx-r,cy-r,r*2,r*2,"",fill,1)
    d[0]["strokeColor"]=color
    return d

def text(x,y,s,size=14,color="#1e1e1e"):
    return [base(type="text",id=nid(),x=x,y=y,width=len(s)*(size*0.55),height=size+4,fontSize=size,
                fontFamily=1,textAlign="left",verticalAlign="top",containerId=None,
                text=s,originalText=s,lineHeight=1.25,strokeColor=color)]

def region(x,y,w,h,title,color="#1971c2"):
    r=base(type="rectangle",id=nid(),x=x,y=y,width=w,height=h,strokeColor=color,
           backgroundColor="transparent",strokeStyle="dashed",roundness={"type":3})
    # text() returns a list; flatten so the result is a flat list of elements.
    return [r]+text(x+14,y+8,title,14,color)

def scene(elements):
    # Z-order: Excalidraw renders elements in array order, later = on top.
    # Put connectors (arrow/line) FIRST so boxes/text are drawn over them —
    # this prevents arrow endpoints that fall inside a box from covering text.
    order = {"arrow":0,"line":0,"rectangle":1,"ellipse":1,"diamond":1,"text":2}
    els = sorted(elements, key=lambda e: order.get(e.get("type"),1))
    return {"type":"excalidraw","version":2,"source":"https://excalidraw.com",
            "elements":els,"appState":{"viewBackgroundColor":"#ffffff"},"files":{}}

C_BLUE="#a5d8ff"; C_GREEN="#b2f2bb"; C_YELLOW="#ffec99"; C_RED="#ffc9c9"
C_PURPLE="#eebefa"; C_GRAY="#e9ecef"; C_ORANGE="#ffd8a8"; C_PINK="#ffe3e3"

DIAGRAMS=[]

def add(name,fn): DIAGRAMS.append((name,fn))

# ═══ 37. RACI Matrix (RACI矩阵) ═══
def raci():
    e=[]
    e += text(300,15,"用户注册功能 — RACI 矩阵",22)
    tasks=["需求评审","UI设计","前端开发","后端开发","测试","部署上线"]
    roles=["产品经理","设计师","前端","后端","QA","运维"]
    data=[["A","I","I","I","I","I"],
          ["C","R","I","I","I","I"],
          ["I","C","R","I","I","I"],
          ["I","I","C","R","I","I"],
          ["I","I","I","C","R","I"],
          ["I","I","I","I","C","R"]]
    cx=[150,290,430,570,710,850]
    cy=[80]
    for j,n in enumerate(roles):
        e+=box(30,cy[0]+j*48,100,40,n,C_BLUE,12)
    for i,t_name in enumerate(tasks):
        e+=box(cx[i],40,120,32,t_name,C_GRAY,11)
        for j,n in enumerate(roles):
            val=data[j][i]
            e+=text(cx[i]+48,cy[0]+j*48+14,val,18,C_YELLOW if val=="R" else(C_RED if val=="A" else "#868e96"))
            e+=line(cx[i],cy[0]+j*48+20,cx[i]+120,cy[0]+j*48+20)
    e+=text(30,380,"R=执行者 A=负责人 C=咨询 I=知会",12)
    return scene(e)
add("37-raci-matrix", raci)

# ═══ 38. Impact-Effort Matrix (影响-努力矩阵) ═══
def impact_effort():
    e=[]
    e += text(300,15,"功能优先级 — 影响-努力矩阵",22)
    e+=line(400,70,400,400); e+=line(100,240,700,240)
    e+=text(480,60,"高努力",12,C_RED); e+=text(160,60,"低努力",12,C_GREEN)
    e+=text(90,80,"高影响",12,C_GREEN); e+=text(90,380,"低影响",12,C_RED)
    e+=text(680,380,"努力→",11); e+=text(320,410,"影响力→",11)
    # Quick wins (low effort, high impact - top left)
    e+=box(160,100,140,50,"一键分享",C_GREEN,13)
    e+=box(160,160,100,40,"导出PDF",C_GREEN,13)
    # Major projects (high effort, high impact - top right)
    e+=box(500,100,140,50,"实时协作",C_BLUE,13)
    # Fill-ins (low effort, low impact - bottom left)
    e+=box(160,300,100,40,"换图标",C_GRAY,13)
    # Time sinks (high effort, low impact - bottom right)
    e+=box(500,300,140,50,"自研富文本",C_RED,13)
    return scene(e)
add("38-impact-effort-matrix", impact_effort)

# ═══ 39. Risk Matrix (风险矩阵) ═══
def risk_matrix():
    e=[]
    e += text(300,15,"项目风险矩阵",22)
    # 5x5 grid
    for i in range(5):
        for j in range(5):
            x=120+j*130; y=70+i*80
            fill=C_GREEN if i+j<3 else(C_YELLOW if i+j<6 else C_RED)
            e+=box(x,y,120,70,"",fill,10,roundness=None)
            e+=text(x+5,y+5,f"{'几乎不' if i==0 else '低' if i==1 else '中' if i==2 else '高' if i==3 else '极高'}-{'很低' if j==0 else '低' if j==1 else '中' if j==2 else '高' if j==3 else '很高'}",9)
    e+=text(360,490,"可能性→",11); e+=text(40,300,"影响→",11)
    # Sample bubbles
    e+=ellipse(245,165,50,40,"数据泄露",C_RED,10)
    e+=ellipse(380,180,40,30,"依赖过期",C_YELLOW,10)
    e+=ellipse(200,300,35,25,"UI延期",C_GREEN,10)
    return scene(e)
add("39-risk-matrix", risk_matrix)

# ═══ 40. Stakeholder Map (干系人地图) ═══
def stakeholder_map():
    e=[]
    e += text(300,15,"项目干系人地图",22)
    e+=line(60,300,780,300); e+=line(420,30,420,520)
    e+=text(440,40,"高权力",12); e+=text(200,40,"低权力",12)
    e+=text(30,60,"高兴趣",12); e+=text(30,480,"低兴趣",12)
    # Keep Satisfied (高权力, 低兴趣)
    e+=box(100,70,150,50,"老板/VP",C_BLUE,14)
    # Key Players (高权力, 高兴趣)
    e+=box(480,70,180,50,"技术负责人",C_GREEN,14)
    e+=box(480,140,140,50,"产品总监",C_GREEN,14)
    # Monitor (低权力, 低兴趣)
    e+=box(100,420,120,50,"外包团队",C_GRAY,11)
    # Keep Informed (低权力, 高兴趣)
    e+=box(100,140,150,50,"用户代表",C_YELLOW,14)
    e+=box(100,210,140,50,"运营团队",C_YELLOW,14)
    return scene(e)
add("40-stakeholder-map", stakeholder_map)

# ═══ 41. Value Stream Map (价值流图) ═══
def value_stream():
    e=[]
    e += text(300,15,"需求交付价值流图",22)
    stages=[("需求分析",80,"LT=2d\nPT=4h"),("设计",280,"LT=1d\nPT=6h"),
            ("开发",480,"LT=5d\nPT=20h"),("测试",680,"LT=2d\nPT=8h"),
            ("部署",880,"LT=0.5d\nPT=1h")]
    for i,(name,x,info) in enumerate(stages):
        e+=box(x,80,140,50,name,C_BLUE,14)
        e+=text(x+10,140,info,10)
        if i<len(stages)-1: e+=arrow(x+140,105,stages[i+1][1],105)
    e+=text(40,200,"总周期=10.5天  增值时间=39h  效率=39/(10.5*8)=46%",12)
    e+=line(60,220,1000,220)
    e+=text(100,230,"等待(非增值)",10,C_RED)
    return scene(e)
add("41-value-stream-map", value_stream)

# ═══ 42. Kanban Board (看板) ═══
def kanban():
    e=[]
    e += text(300,15,"Sprint 看板",24)
    cols=["Todo (WIP:8)","In Progress (WIP:4)","Review (WIP:3)","Done"]
    colors={"Todo (WIP:8)":C_GRAY,"In Progress (WIP:4)":C_BLUE,"Review (WIP:3)":C_YELLOW,"Done":C_GREEN}
    # Column headers at y=60, cards start at y=110 (no overlap with header)
    HEADER_Y=60; CARD_Y0=110; CARD_H=42; CARD_GAP=12
    for j,col in enumerate(cols):
        x=40+j*230
        e+=box(x,HEADER_Y,210,35,col,colors[col],13,roundness=None)
        e+=line(x+105,HEADER_Y+35,x+105,HEADER_Y+35+3*(CARD_H+CARD_GAP)+20,dashed=True)
    # Cards — light gray fill (NOT white) so they're visible against the canvas.
    cards=[("Todo (WIP:8)",["用户登录页","支付回调","导出CSV"]),
           ("In Progress (WIP:4)",["商品列表API","订单状态机","缓存优化"]),
           ("Review (WIP:3)",["注册校验","接口文档"]),
           ("Done",["环境配置","Dockerfile","CI模板"])]
    for col,items in cards:
        j=cols.index(col); x=50+j*230
        for i,title in enumerate(items):
            y=CARD_Y0+i*(CARD_H+CARD_GAP)
            e+=box(x,y,190,CARD_H,title,"#f1f3f5",11)
    return scene(e)
add("42-kanban-board", kanban)

# ═══ 44. Event Storming (事件风暴) ═══
def event_storming():
    e=[]
    e += text(280,15,"下单流程 — Event Storming",22)
    events=[("浏览商品",60),("加入购物车",200),("提交订单",340),("选择支付",480),("支付回调",620),("订单确认",760)]
    for i,(ev_name,x) in enumerate(events):
        e+=box(x,70,110,45,ev_name,C_ORANGE,11,roundness={"type":3})
        if i<len(events)-1: e+=arrow(x+110,92,events[i+1][1],92)
    # Commands
    cmds=[("查询商品",80,120),("添加项",220,120),("验证库存",360,120),("发起支付",500,120),("更新状态",640,120)]
    for c_name,x,y in cmds:
        e+=box(x,y,90,30,c_name,C_BLUE,10)
    # External systems
    exts=[("商品服务",100,190),("库存系统",360,190),("支付网关",520,190)]
    for ex_name,x,y in exts:
        e+=box(x,y,90,30,ex_name,C_PINK,10)
    return scene(e)
add("44-event-storming", event_storming)

# ═══ 45. Context Map (限界上下文映射) ═══
def context_map():
    e=[]
    e += text(280,15,"电商系统 — Context Map (DDD)",22)
    e+=box(60,60,160,50,"订单上下文\n(Order)",C_GREEN,13)
    e+=box(300,60,160,50,"支付上下文\n(Payment)",C_BLUE,13)
    e+=box(540,60,160,50,"商品上下文\n(Product)",C_GREEN,13)
    e+=box(60,220,160,50,"用户上下文\n(User)",C_YELLOW,13)
    e+=box(300,220,160,50,"库存上下文\n(Inventory)",C_GREEN,13)
    e+=box(540,220,160,50,"物流上下文\n(Logistics)",C_GRAY,13)
    # relationships
    e+=text(150,125,"U/D",12,C_BLUE)
    e+=text(390,125,"ACL",12,C_RED)
    e+=text(120,160,"OHS",12,C_PURPLE)
    e+=line(220,85,300,85)
    e+=line(460,85,540,85)
    e+=line(140,110,140,220)
    e+=line(380,110,380,220)
    e+=line(620,110,620,220)
    # Legend
    e+=text(60,350,"U/D=上游/下游  ACL=防腐层  OHS=开放主机服务  PL=发布语言  SK=共享内核",11)
    return scene(e)
add("45-context-map", context_map)

# ═══ 48. Git Branch Strategy (Git分支策略) ═══
def git_strategy():
    e=[]
    e += text(300,15,"Git Flow 分支策略",22)
    MAIN_Y=70; DEV_Y=170
    # Branch baselines (colored, thick)
    e+=line(60,MAIN_Y,900,MAIN_Y,color=C_GREEN)
    e+=line(60,DEV_Y,900,DEV_Y,color="#1971c2")
    e+=text(20,MAIN_Y-8,"main",12,C_GREEN)
    e+=text(10,DEV_Y-8,"develop",12,"#1971c2")
    # Commit nodes on main
    for cx in [120,560,760,880]:
        e+=dot(cx,MAIN_Y,r=8,fill=C_GREEN)
    # Tag labels on main
    e+=text(108,MAIN_Y+12,"v1.0",10,C_GREEN)
    e+=text(748,MAIN_Y+12,"v1.1",10,C_GREEN)
    # Commit nodes on develop
    for cx in [120,220,320,440,560,660,760]:
        e+=dot(cx,DEV_Y,r=8,fill="#1971c2")
    # Feature branches: diverge from develop, merge back
    feats=[("feat/login",220,300,"#f08c00"),("feat/cart",320,420,"#ae3ec9"),("feat/pay",440,540,"#e8590c")]
    for name,x0,x1,color in feats:
        FY=DEV_Y+50
        # diverge (develop up? no — down): vertical then horizontal branch line
        e+=polyline([(x0,DEV_Y),(x0,FY),(x1,FY),(x1,DEV_Y)],color=color)
        e+=dot(x0,DEV_Y,r=7,fill=color); e+=dot(x1,DEV_Y,r=7,fill=color)
        e+=text(x0+4,FY+6,name,9,color)
    # Release branch: develop → main
    e+=polyline([(560,DEV_Y),(560,(MAIN_Y+DEV_Y)//2),(760,(MAIN_Y+DEV_Y)//2),(760,MAIN_Y)],dashed=True,color=C_YELLOW)
    e+=text(600,(MAIN_Y+DEV_Y)//2-14,"release/1.1",9,C_YELLOW)
    # Hotfix: from main, back to main + develop
    e+=polyline([(760,MAIN_Y),(760,MAIN_Y-40),(880,MAIN_Y-40),(880,MAIN_Y)],color=C_RED)
    e+=text(790,MAIN_Y-52,"hotfix/bug",9,C_RED)
    # Legend
    e+=text(60,DEV_Y+120,"绿=main  蓝=develop  橙/紫=feature(虚线合并)  黄虚线=release  红=hotfix",10)
    return scene(e)
add("48-git-branch-strategy", git_strategy)

# ═══ 50. System Landscape (系统景观图) ═══
def system_landscape():
    e=[]
    e += text(300,15,"电商平台 — 系统景观图",22)
    e+=region(40,60,300,180,"用户端")
    e+=box(60,100,120,50,"Web App",C_BLUE,14)
    e+=box(200,100,120,50,"小程序",C_BLUE,14)
    e+=box(60,170,120,40,"移动App",C_BLUE,14)
    e+=region(380,60,300,180,"核心服务")
    e+=box(400,100,120,50,"订单服务",C_GREEN,14)
    e+=box(540,100,120,50,"商品服务",C_GREEN,14)
    e+=box(400,170,120,40,"支付服务",C_YELLOW,14)
    e+=region(720,60,260,180,"基础设施")
    e+=box(740,100,100,50,"MySQL",C_GRAY,14)
    e+=box(860,100,100,50,"Redis",C_PURPLE,14)
    e+=box(740,170,100,40,"MQ",C_GRAY,14)
    # Status indicators
    e+=ellipse(180,210,14,14,"",C_GREEN,1)
    e+=ellipse(560,210,14,14,"",C_YELLOW,1)
    e+=ellipse(820,210,14,14,"",C_RED,1)
    e+=text(60,240,"●RUNNING  ●DEGRADED  ●DOWN",11)
    return scene(e)
add("50-system-landscape", system_landscape)

# ═══ 51. Technology Radar (技术雷达) ═══
def tech_radar():
    e=[]
    e += text(300,15,"团队技术雷达 2026H1",22)
    rings=["Adopt(采纳)","Trial(试验)","Assess(评估)","Hold(暂缓)"]
    for i,ring in enumerate(rings):
        r=50+i*55
        e+=ellipse(500-r,280-r,r*2,r*2,"",C_GRAY,1)
        e+=text(520-r,270+i*10,ring,10,"#868e96")
    # Quadrants
    e+=line(500,50,500,510); e+=line(100,280,900,280)
    e+=text(520,60,"技术",11); e+=text(200,60,"工具",11)
    e+=text(200,480,"平台",11); e+=text(520,480,"语言&框架",11)
    # Items
    items=[("Rust",400,180,C_GREEN),("K8s",380,220,C_GREEN),
           ("WASM",550,250,C_BLUE),("Bun",450,200,C_BLUE),
           ("Zig",600,300,C_YELLOW),("GraphQL",500,320,C_YELLOW)]
    for name,x,y,color in items:
        e+=ellipse(x,y,28,28,name,color,8)
    return scene(e)
add("51-technology-radar", tech_radar)

# ═══ 53. NFR / Quality Attribute Tree (质量属性树) ═══
def nfr_tree():
    e=[]
    e += text(280,15,"系统质量属性树 (NFR)",22)
    root=(450,50)
    e+=box(root[0]-40,root[1],80,40,"系统质量",C_GREEN,13)
    branches=[("性能",200,120,C_BLUE),("安全",360,120,C_BLUE),("可用性",520,120,C_BLUE),
              ("可维护性",680,120,C_BLUE),("可扩展性",840,120,C_BLUE)]
    for name,x,y,color in branches:
        e+=box(x-40,y,80,36,name,color,13)
        e+=line(root[0],root[1]+40,x,y)
    leaves=[("响应<200ms",150,190,"性能"),("吞吐>1kTPS",250,190,"性能"),
            ("SQL注入防护",310,190,"安全"),("数据加密",410,190,"安全"),
            ("99.9% SLA",470,190,"可用性"),("自动故障转移",570,190,"可用性"),
            ("单元测试>80%",630,190,"可维护性"),("模块化架构",730,190,"可维护性"),
            ("水平扩展",790,190,"可扩展性"),("微服务拆分",890,190,"可扩展性")]
    bcenter={n:(x,y+18) for n,x,y,c in branches}  # branch bottom-center
    for name,x,y,parent in leaves:
        e+=box(x-30,y,60,28,name,C_GRAY,10,roundness=None)
        px,py=bcenter[parent]
        e+=line(px,py,x,y)   # connect branch → leaf
    return scene(e)
add("53-nfr-quality-tree", nfr_tree)

# ═══ 55. API Service Interaction (API流转图) ═══
def api_flow():
    e=[]
    e += text(300,15,"下单 — API 调用链",22)
    svcs=[("客户端",60,C_BLUE),("API GW",260,C_YELLOW),("订单服务",460,C_GREEN),("支付服务",660,C_RED)]
    for s_name,x,color in svcs:
        e+=box(x-50,70,100,45,s_name,color,14)
        e+=line(x,115,x,380,dashed=True)
    # Calls: (y, x1, x2, label). Lifelines at x=60(客户端),260(GW),460(订单),660(支付).
    calls=[(130, 60,260,"1. POST /order"),
           (180,260,460,"2. createOrder()"),
           (230,460,660,"3. pay()"),
           (290,660,460,"4. success"),
           (340,460,260,"5. confirm")]
    for y,x1,x2,label in calls:
        e+=arrow(x1,y,x2,y,dashed="success" in label or "confirm" in label)
        e+=text((x1+x2)//2-45,y-20,label,10)
    return scene(e)
add("55-api-service-interaction", api_flow)

# ═══ 58. Kano Model (卡诺模型) ═══
def kano_model():
    e=[]
    e+=text(300,15,"产品功能 — Kano 模型分析",22)
    # Axes: x = 功能实现度 (left=未实现, right=已实现), y = 满意度 (down=不满, up=惊喜)
    # Origin at (400,400). Draw axis lines with arrowheads.
    e+=arrow(400,400,860,400)                      # X axis (→ 实现)
    e+=arrow(400,400,400,40)                       # Y axis (↑ 满意)
    e+=text(820,410,"功能实现度→",12)
    e+=text(330,36,"满意度↑",12)
    # Diagonal: 期望需求 (performance, 必过原点的对角线)
    e+=polyline([(430,370),(560,250),(700,130),(820,60)],color=C_BLUE)
    e+=text(740,110,"期望需求 (越多越好)",10,C_BLUE)
    # Excitement curve (上方): 未实现时无所谓, 实现后满意度剧增
    e+=polyline([(430,395),(520,392),(620,360),(720,240),(820,70)],color=C_GREEN)
    e+=text(720,150,"兴奋需求 (惊喜)",10,C_GREEN)
    # Basic needs curve (下方): 未实现时极度不满, 实现后只是"不抱怨"
    e+=polyline([(430,405),(500,410),(560,420),(640,418),(740,412),(820,395)],color=C_RED)
    e+=text(620,435,"基本需求 (必须做)",10,C_RED)
    # Legend box
    e+=box(60,60,170,90,"图例\n蓝=期望\n绿=兴奋\n红=基本",C_GRAY,10)
    return scene(e)
add("58-kano-model", kano_model)

# ═══ 60. Business Model Canvas (商业模式画布) ═══
def bmc():
    e=[]
    e += text(300,15,"商业模式画布 (Business Model Canvas)",22)
    cells=[("关键伙伴",30,70,220,120,C_GRAY),("关键活动",270,70,220,120,C_BLUE),("价值主张",510,70,220,180,C_GREEN),
           ("客户关系",750,70,220,120,C_YELLOW),("客户细分",990,70,220,280,C_PINK),
           ("核心资源",30,210,220,120,C_BLUE),("渠道",270,210,220,100,C_YELLOW),
           ("成本结构",30,420,460,120,C_RED),("收入流",510,420,460,120,C_GREEN)]
    for label,x,y,w,h,color in cells:
        e+=box(x,y,w,h,label,color,12,roundness=None)
        e+=box(x+5,y+20,w-10,h-25,"",color,10)
    return scene(e)
add("60-business-model-canvas", bmc)

# ═══ 63. Threat Model (威胁建模/STRIDE) ═══
def threat_model():
    e=[]
    e += text(300,15,"支付系统 — STRIDE 威胁建模",22)
    e+=box(60,70,120,50,"用户\n(User)",C_BLUE,12)
    e+=box(300,70,140,50,"API Gateway\n(边界)",C_GREEN,12)
    e+=box(560,70,140,50,"支付服务\n(Payment)",C_GREEN,12)
    e+=box(560,220,140,50,"银行接口\n(Bank API)",C_RED,12)
    e+=box(300,220,140,50,"数据库\n(MySQL)",C_GRAY,12)
    e+=arrow(180,95,300,95)
    e+=arrow(440,95,560,95)
    e+=arrow(560,120,560,220)
    e+=arrow(370,245,440,245)
    # Threats
    threats=[("S 欺骗",140,65,C_RED),("T 篡改",370,65,C_RED),
             ("I 泄露",540,140,C_RED),("D 拒绝服务",540,280,C_RED),("E 提权",370,280,C_RED)]
    for name,x,y,color in threats:
        e+=ellipse(x,y,30,25,name,color,8)
    e+=text(60,380,"S=欺骗 T=篡改 R=抵赖 I=信息泄露 D=拒绝服务 E=提权",11)
    return scene(e)
add("63-stride-threat-model", threat_model)

# ═══ 65. Fishbone / Ishikawa (鱼骨图) ═══
def fishbone():
    e=[]
    e+=text(300,15,"线上故障排查 — 鱼骨图 (Ishikawa)",22)
    # Spine: horizontal arrow ending at the "problem" head on the right.
    SPINE_Y=250
    e+=arrow(80,SPINE_Y,720,SPINE_Y)
    e+=box(740,SPINE_Y-30,120,60,"故障:下单502",C_RED,12)
    # 6Ms categories. Diagonal bones pointing INTO the spine.
    cats=[("人 (People)",      180,  UP :=True ,C_BLUE,
           ["值班不熟悉回滚","人手不足"]),
          ("方法 (Method)",    180,  False    ,C_GREEN,
           ["无灰度发布","监控阈值过宽"]),
          ("机器 (Machine)",   340,  True     ,C_YELLOW,
           ["CPU 打满","磁盘写满"]),
          ("物料 (Material)",  340,  False    ,C_PURPLE,
           ["依赖三方超时","配置错误"]),
          ("测量 (Measure)",   520,  True     ,C_ORANGE,
           ["告警延迟5min","日志不全"]),
          ("环境 (Environment)",520, False    ,C_PINK,
           ["机房网络抖动","DNS 污染"])]
    for name,x,up,color,causes in cats:
        # bone start (away from spine) and end (on spine)
        by = SPINE_Y-130 if up else SPINE_Y+130
        e+=polyline([(x,by),(x+90,SPINE_Y)],color="#495057")
        e+=box(x-50,by-22,130,30,name,color,11)
        # sub-cause small branches off the diagonal bone
        for i,ca in enumerate(causes):
            cy = by + (40 if up else -40) + i*(26 if up else -26)
            e+=line(x+30,by+ (60 if up else -60), x+30+ (50 if i==0 else 70), cy, color="#868e96")
            e+=text(x+40+ (50 if i==0 else 70), cy-7, ca, 9)
    return scene(e)
add("65-fishbone", fishbone)

# ═══ 66. Swimlane Flowchart (泳道流程图) ═══
def swimlane():
    e=[]
    e+=text(280,15,"退款流程 — 跨职能泳道图",22)
    lanes=[("用户",60,C_BLUE),("客服",230,C_YELLOW),("财务",400,C_GREEN),("系统",570,C_PURPLE)]
    # Swimlane backgrounds
    for name,x,color in lanes:
        e+=box(x,55,160,360,"",color,1)
        e+=text(x+8,60,name,13)
    # Steps: (lane_x_center, y, label)
    Y0=110
    steps=[(140,Y0,"申请退款",C_BLUE),
           (310,Y0+50,"审核凭证",C_YELLOW),
           (480,Y0+100,"校验金额",C_GREEN),
           (650,Y0+150,"冻结订单",C_PURPLE),
           (650,Y0+230,"原路退回",C_PURPLE),
           (480,Y0+280,"更新账务",C_GREEN),
           (140,Y0+330,"收到退款",C_BLUE)]
    boxes=[]
    for cx,y,label,color in steps:
        # white fill so the step stands out on the colored lane background
        b=box(cx-55,y,110,34,label,"#ffffff",11)
        boxes.append((cx,y,b[0]["id"]))
        e+=b
    # Connect in order (the process flow)
    for i in range(len(boxes)-1):
        cx1,y1,_=boxes[i]; cx2,y2,_=boxes[i+1]
        e+=arrow(cx1+ (55 if cx2>cx1 else -55), y1+17, cx2+(-55 if cx2<cx1 else 55), y2+17)
    return scene(e)
add("66-swimlane", swimlane)

# ═══ 67. User Story Map (用户故事地图) ═══
def story_map():
    e=[]
    e+=text(280,15,"电商 v2.0 — 用户故事地图",22)
    # Backbone: user activities (epics) across the top
    e+=text(20,55,"主线活动:",13)
    backbone=[("浏览",60),("搜索",230),("下单",400),("支付",570),("发货",740)]
    for name,x in backbone:
        e+=box(x,75,130,36,name,C_BLUE,13)
    # Releases (swimlanes)
    e+=text(20,135,"v1.0 MVP:",13,C_GREEN)
    e+=text(20,200,"v1.5:",13,C_YELLOW)
    e+=text(20,265,"v2.0:",13,C_RED)
    # User stories under each activity, grouped by release row
    stories={
        135:[("商品详情",60),("关键词搜",230),("购物车",400),("余额支付",570),("自提",740)],
        200:[("推荐流",60),("筛选",230),("优惠券",400),("微信支付",570),("快递",740)],
        265:[("直播",60),("AI搜",230),("拼团",400),("分期",570),("同城达",740)],
    }
    for y,items in stories.items():
        for name,x in items:
            e+=box(x,y,130,30,name,C_GRAY if y==135 else (C_YELLOW if y==200 else C_RED),10)
    # release priority axis (downward = later)
    e+=arrow(20,320,880,320)
    e+=text(840,330,"时间 / 优先级 →",11)
    return scene(e)
add("67-user-story-map", story_map)

# ═══ 68. Empathy Map (同理心地图) ═══
def empathy_map():
    e=[]
    e+=text(280,15,"目标用户同理心地图 (Empathy Map)",22)
    # 2x2 quadrants + center user
    e+=box(60,60,360,150,"想 (Think)\n「这能解决我的问题吗」\n「会不会很复杂」",C_BLUE,12)
    e+=box(440,60,360,150,"感 (Feel)\n期待 + 焦虑\n怕学不会、怕踩坑",C_YELLOW,12)
    e+=box(60,230,360,150,"说 (Say)\n「先收藏一下」\n「有没有教程」",C_GREEN,12)
    e+=box(440,230,360,150,"做 (Do)\n对比3个竞品\n看评论再决定",C_PURPLE,12)
    # center user circle
    e+=ellipse(370,180,120,80,"用户",C_PINK,16)
    # pains / gains footer
    e+=box(60,400,360,50,"痛点 Pains: 时间紧、选择多、怕被坑",C_RED,11)
    e+=box(440,400,360,50,"收益 Gains: 省时、靠谱、有成就感",C_GREEN,11)
    return scene(e)
add("68-empathy-map", empathy_map)

# ═══ 69. Decision Tree (决策树) ═══
def decision_tree():
    e=[]
    e+=text(300,15,"事件处理 — 决策树",22)
    # root question
    e+=diamond(380,60,140,50,"是否影响\n核心交易?",C_YELLOW,12)
    # Yes branch (left) -> severity
    e+=arrow(420,110,300,150); e+=text(310,125,"是",11,C_RED)
    e+=diamond(180,150,160,50,"影响范围\n>10% 用户?",C_RED,12)
    e+=arrow(220,200,140,250); e+=text(150,220,"是",11,C_RED)
    e+=box(60,250,120,40,"P0 立即回滚",C_RED,11)
    e+=arrow(320,200,420,250); e+=text(330,220,"否",11)
    e+=box(360,250,120,40,"P1 限流修复",C_ORANGE,11)
    # No branch (right) -> routine
    e+=arrow(480,110,620,150); e+=text(540,125,"否",11)
    e+=diamond(560,150,160,50,"可复现?",C_BLUE,12)
    e+=arrow(600,200,540,250); e+=text(545,220,"是",11)
    e+=box(480,250,120,40,"P2 提工单",C_YELLOW,11)
    e+=arrow(700,200,780,250); e+=text(720,220,"否",11)
    e+=box(720,250,120,40,"观察监控",C_GREEN,11)
    e+=text(60,330,"决策: P0=立即回滚 | P1=限流修复 | P2=提工单 | 其他=观察",11)
    return scene(e)
add("69-decision-tree", decision_tree)

# ═══ 70. Burndown Chart (燃尽图) ═══
def burndown():
    e=[]
    e+=text(300,15,"Sprint 燃尽图 (Burndown)",22)
    # Axes
    e+=arrow(80,80,80,380)                      # Y axis
    e+=arrow(80,380,720,380)                    # X axis
    e+=text(40,80,"剩余\n故事点",11)
    e+=text(700,390,"天数 →",11)
    # Y tick labels
    for i,v in enumerate([120,90,60,30,0]):
        y=380-i*60
        e+=line(76,y,84,y); e+=text(48,y-6,str(v),10)
    # X tick labels (days)
    for i,d in enumerate(range(11)):
        x=80+i*60
        e+=line(x,376,x,384); e+=text(x-6,390,f"D{d}",9)
    # Ideal line (linear 120->0)
    ideal=[(80,80),(720,380)]
    e+=polyline(ideal,dashed=True,color="#868e96")
    e+=text(360,250,"理想线 (虚线)",9,"#868e96")
    # Actual line (zigzag, ends above 0 = not all done)
    actual=[(80,80),(140,95),(200,110),(260,130),(320,150),(380,160),
            (440,170),(500,185),(560,200),(620,215),(680,230)]
    e+=polyline(actual,color=C_BLUE)
    e+=text(560,215,"实际剩余",9,C_BLUE)
    # Legend
    e+=box(480,80,220,40,"蓝实线=实际剩余\n灰虚线=理想进度",C_GRAY,9)
    return scene(e)
add("70-burndown", burndown)

# ═══ 71. Org Chart (组织架构图) ═══
def org_chart():
    e=[]
    e+=text(320,15,"研发团队组织架构图",22)
    # CEO/CTO top
    e+=box(370,60,140,40,"CTO",C_PURPLE,14)
    # Layer 2: 3 leads
    leads=[("前端负责人",120,C_BLUE),("后端负责人",370,C_GREEN),("测试负责人",620,C_YELLOW)]
    for name,x,color in leads:
        e+=box(x,150,140,40,name,color,12)
        e+=line(440,100,x+70,150)   # CTO -> lead
    # Layer 3: members under each lead
    members={
        120:[("小程序",C_BLUE),("商家端",C_BLUE)],
        370:[("订单",C_GREEN),("支付",C_GREEN),("基础架构",C_GREEN)],
        620:[("功能测试",C_YELLOW),("自动化",C_YELLOW)],
    }
    for lx,items in members.items():
        n=len(items)
        for i,(name,color) in enumerate(items):
            x=lx + (i-(n-1)/2)*80 - 40
            y=240
            e+=box(x,y,80,36,name,color,10)
            e+=line(lx+70,190,x+40,240)   # lead -> member
    e+=text(60,330,"实线=直接汇报关系",10)
    return scene(e)
add("71-org-chart", org_chart)

# ═══ 72. UML Class Diagram (类图) ═══
def class_diagram():
    e=[]
    e+=text(320,15,"领域模型 — UML 类图",22)
    # Class boxes: name | attributes | methods (3 stacked compartments)
    def classbox(x,y,name,attrs,methods,color):
        e.extend(box(x,y,160,28,name,color,13))
        ay=y+30
        e.extend(box(x,ay,160,len(attrs)*16+8,"",color,1))
        for i,a in enumerate(attrs):
            e.extend(text(x+8,ay+4+i*16,a,10))
        my=ay+len(attrs)*16+10
        e.extend(box(x,my,160,len(methods)*16+8,"",color,1))
        for i,m in enumerate(methods):
            e.extend(text(x+8,my+4+i*16,m,10))
        return (x,y,x+160,my+len(methods)*16+8)  # bbox
    # 3 classes
    o=classbox(60,70,"Order",["-id: Long","-userId: Long","-total: Money","-status: Enum"],
               ["+pay(): void","+cancel(): void"],C_BLUE)
    u=classbox(340,70,"User",["-id: Long","-name: String","-phone: String"],
               ["+login(): Token"],C_GREEN)
    i=classbox(60,260,"OrderItem",["-id: Long","-productId: Long","-qty: Int","-price: Money"],
               ["+subtotal(): Money"],C_YELLOW)
    # Relationships (UML): Order o-- User (association), Order *-- OrderItem (composition)
    # Order right edge -> User left edge (association, simple line)
    e+=arrow(o[2],90,u[0],90)
    e+=text(240,80,"places",10)
    # Order bottom -> OrderItem top (composition = filled diamond at parent)
    e+=line(140,o[3],140,i[1])
    e+=diamond(125,o[3]-6,30,24,"",C_GRAY,1)  # composition diamond on parent end
    e+=text(150,(o[3]+i[1])//2,"1..*",10)
    e+=text(60,400,"UML: 实心菱形=组合(composition)  普通箭头=关联(association)",10)
    return scene(e)
add("72-class-diagram", class_diagram)

# ═══ 73. Data Flow Diagram / DFD (数据流图) ═══
def dfd():
    e=[]
    e+=text(320,15,"订单系统 — 数据流图 (DFD, Level-1)",22)
    # External entities (rectangles), processes (rounded/circle), data stores (open rect)
    # Entities
    e+=box(40,180,110,50,"用户\n(外部实体)",C_BLUE,11)
    e+=box(680,180,110,50,"支付网关\n(外部实体)",C_RED,11)
    # Processes (circles, numbered)
    e+=ellipse(240,120,110,50,"1.创建订单",C_GREEN,11)
    e+=ellipse(240,260,110,50,"2.处理支付",C_YELLOW,11)
    e+=ellipse(460,190,110,50,"3.更新库存",C_PURPLE,11)
    # Data stores (two horizontal lines = open rectangle; emulate with box + line)
    e+=box(420,330,140,36,"D1 订单库",C_GRAY,10)
    e+=box(620,330,140,36,"D2 商品库",C_GRAY,10)
    # Flows (labeled arrows)
    e+=arrow(150,195,235,150); e+=text(160,170,"下单请求",9)
    e+=arrow(295,150,295,255); e+=text(300,200,"订单号",9)
    e+=arrow(295,285,675,200); e+=text(440,235,"支付请求",9)
    e+=arrow(675,210,295,290,dashed=True); e+=text(440,275,"支付结果",9)
    e+=arrow(350,140,420,195); e+=text(370,160,"写入",9)
    e+=arrow(490,210,490,330); e+=text(500,270,"扣减",9)
    e+=arrow(570,330,560,215); e+=text(575,275,"读库存",9)
    e+=text(40,400,"DFD: 圆=处理过程  方框=外部实体  开放矩形=数据存储  箭头=数据流",10)
    return scene(e)
add("73-data-flow-diagram", dfd)

# ═══ Generate all ═══
if __name__=="__main__":
    out_dir=sys.argv[1] if len(sys.argv)>1 else "examples/all"
    import os; os.makedirs(out_dir,exist_ok=True)
    for name,fn in DIAGRAMS:
        PID[0]=0
        s=fn()
        path=f"{out_dir}/{name}.excalidraw"
        with open(path,"w",encoding="utf-8") as f:
            json.dump(s,f,ensure_ascii=False)
        print(f"  {path}  ({len(s['elements'])} elements)")
    print(f"\nGenerated {len(DIAGRAMS)} diagrams.")
