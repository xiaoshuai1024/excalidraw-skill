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

def line(x1,y1,x2,y2,dashed=False):
    return [base(type="line",id=nid(),x=x1,y=y1,width=x2-x1,height=y2-y1,roundness={"type":2},
                strokeStyle="dashed" if dashed else "solid",
                lastCommittedPoint=None,points=[[0,0],[x2-x1,y2-y1]])]

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
    return {"type":"excalidraw","version":2,"source":"https://excalidraw.com",
            "elements":elements,"appState":{"viewBackgroundColor":"#ffffff"},"files":{}}

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
    for j,col in enumerate(cols):
        x=40+j*230
        e+=box(x,60,210,35,col,colors[col],13,roundness=None)
        e+=line(x+105,95,x+105,500,dashed=True)
    # Cards
    cards=[("Todo (WIP:8)",[("用户登录页",80),("支付回调",130),("导出CSV",180)]),
           ("In Progress (WIP:4)",[("商品列表API",80),("订单状态机",130),("缓存优化",180)]),
           ("Review (WIP:3)",[("注册校验",80),("接口文档",130)]),
           ("Done",[("环境配置",80),("Dockerfile",130),("CI模板",180)])]
    for col,cards_list in cards:
        j=cols.index(col); x=50+j*230
        for title,y in cards_list:
            e+=box(x,y,190,40,title,"#ffffff",11)
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
    # main branch
    e+=line(40,60,900,60)
    e+=text(40,50,"main",14)
    e+=ellipse(100,50,30,20,"v1.0",C_GREEN,8)
    e+=ellipse(400,50,30,20,"v1.1",C_GREEN,8)
    # develop branch
    e+=line(40,120,900,120)
    e+=text(40,110,"develop",14)
    # feature branches
    for x,name in [(150,"feat/login"),(250,"feat/cart"),(350,"feat/pay")]:
        e+=line(x,120,x,80)
        e+=text(x-20,75,name,9,C_BLUE)
    # release branch
    e+=line(500,120,500,60)
    e+=text(490,45,"release/1.1",9,C_YELLOW)
    # hotfix
    e+=line(600,60,600,20)
    e+=text(590,15,"hotfix/bug",9,C_RED)
    # merge arrows
    e+=arrow(350,120,380,120)
    e+=arrow(500,120,550,60,dashed=True)
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
    leaves=[("响应<200ms",150,190),("吞吐>1kTPS",250,190),
            ("SQL注入防护",310,190),("数据加密",410,190),
            ("99.9% SLA",470,190),("自动故障转移",570,190),
            ("单元测试>80%",630,190),("模块化架构",730,190),
            ("水平扩展",790,190),("微服务拆分",890,190)]
    for name,x,y in leaves:
        e+=box(x-30,y,60,28,name,C_GRAY,10,roundness=None)
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
    # Calls
    calls=[(135,110,260,"1. POST /order"),(180,260,460,"2. createOrder()"),
           (230,460,660,"3. pay()"),(290,660,460,"4. success"),(350,460,260,"5. confirm")]
    for y,x1,x2,label in calls:
        e+=arrow(x1,y,x2,y,dashed="success" in label or "confirm" in label)
        e+=text((x1+x2)//2-40,y-20,label,10)
    return scene(e)
add("55-api-service-interaction", api_flow)

# ═══ 58. Kano Model (卡诺模型) ═══
def kano_model():
    e=[]
    e += text(300,15,"产品功能 — Kano 模型分析",22)
    e+=line(80,380,880,380); e+=line(80,40,80,380)
    e+=text(90,50,"满意度",12); e+=text(840,390,"功能实现度",12)
    # Basic needs (bottom curve)
    e+=text(600,180,"基本需求(必须做)",10,C_RED)
    e+=line(100,340,300,340)
    e+=line(300,340,500,300)
    e+=line(500,300,700,280)
    # Performance needs (linear)
    e+=text(600,130,"期望需求(越多越好)",10,C_BLUE)
    e+=line(100,380,200,290)
    e+=line(200,290,400,200)
    e+=line(400,200,600,110)
    # Excitement (top curve)
    e+=text(600,80,"兴奋需求(惊喜)",10,C_GREEN)
    e+=line(100,380,250,380)
    e+=line(250,380,350,250)
    e+=line(350,250,500,140)
    e+=line(500,140,700,60)
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

# ═══ Generate all ═══
if __name__=="__main__":
    out_dir=sys.argv[1] if len(sys.argv)>1 else "test/all"
    import os; os.makedirs(out_dir,exist_ok=True)
    for name,fn in DIAGRAMS:
        PID[0]=0
        s=fn()
        path=f"{out_dir}/{name}.excalidraw"
        with open(path,"w",encoding="utf-8") as f:
            json.dump(s,f,ensure_ascii=False)
        print(f"  {path}  ({len(s['elements'])} elements)")
    print(f"\nGenerated {len(DIAGRAMS)} diagrams.")
