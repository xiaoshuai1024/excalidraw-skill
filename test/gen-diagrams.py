#!/usr/bin/env python3
"""Generate 10 different business-system diagrams as .excalidraw scenes.

Each diagram showcases a common type: architecture, deployment, flowchart,
sequence, ER, state machine, mindmap, network topology, user journey, component.
All use the same helper primitives so labels center correctly (the renderer
re-centers bound text via containerId).
"""
import json
import sys

PID = [0]
def nid():
    PID[0] += 1
    return f"e{PID[0]}"

def base(**kw):
    d = {"angle":0,"strokeColor":"#1e1e1e","backgroundColor":"transparent","fillStyle":"solid",
         "strokeWidth":2,"strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],
         "roundness":None,"seed":None,"version":1,"versionNonce":None,"isDeleted":False,
         "boundElements":[],"updated":1,"link":None,"locked":False}
    d.update(kw); return d

def box(x,y,w,h,label,fill,fs=18,dashed=False,stroke="#1e1e1e"):
    b = base(type="rectangle",id=nid(),x=x,y=y,width=w,height=h,backgroundColor=fill,
             strokeColor=stroke,roundness={"type":3},strokeStyle="dashed" if dashed else "solid")
    t = base(type="text",id=nid(),x=x,y=y,width=80,height=24,fontSize=fs,fontFamily=1,
             textAlign="center",verticalAlign="middle",containerId=b["id"],
             text=label,originalText=label,lineHeight=1.25)
    b["boundElements"]=[{"id":t["id"],"type":"text"}]
    return [b,t]

def ellipse(x,y,w,h,label,fill,fs=18):
    e = base(type="ellipse",id=nid(),x=x,y=y,width=w,height=h,backgroundColor=fill)
    t = base(type="text",id=nid(),x=x,y=y,width=80,height=24,fontSize=fs,fontFamily=1,
             textAlign="center",verticalAlign="middle",containerId=e["id"],
             text=label,originalText=label,lineHeight=1.25)
    e["boundElements"]=[{"id":t["id"],"type":"text"}]
    return [e,t]

def diamond(x,y,w,h,label,fill,fs=18):
    d = base(type="diamond",id=nid(),x=x,y=y,width=w,height=h,backgroundColor=fill)
    t = base(type="text",id=nid(),x=x,y=y,width=60,height=24,fontSize=fs,fontFamily=1,
             textAlign="center",verticalAlign="middle",containerId=d["id"],
             text=label,originalText=label,lineHeight=1.25)
    d["boundElements"]=[{"id":t["id"],"type":"text"}]
    return [d,t]

def arrow(x1,y1,x2,y2,dashed=False,color="#1e1e1e"):
    return base(type="arrow",id=nid(),x=x1,y=y1,width=x2-x1,height=y2-y1,strokeColor=color,
                roundness={"type":2},strokeStyle="dashed" if dashed else "solid",
                startBinding=None,endBinding=None,lastCommittedPoint=None,
                startArrowhead=None,endArrowhead="arrow",points=[[0,0],[x2-x1,y2-y1]])

def line(x1,y1,x2,y2):
    return base(type="line",id=nid(),x=x1,y=y1,width=x2-x1,height=y2-y1,roundness={"type":2},
                lastCommittedPoint=None,points=[[0,0],[x2-x1,y2-y1]])

def text(x,y,s,size=18,color="#1e1e1e"):
    return base(type="text",id=nid(),x=x,y=y,width=len(s)*10,height=size+4,fontSize=size,
                fontFamily=1,textAlign="left",verticalAlign="top",containerId=None,
                text=s,originalText=s,lineHeight=1.25,strokeColor=color)

def region(x,y,w,h,title,color="#1971c2"):
    r = base(type="rectangle",id=nid(),x=x,y=y,width=w,height=h,strokeColor=color,
             backgroundColor="transparent",strokeStyle="dashed",roundness={"type":3})
    t = text(x+14,y+8,title,16,color)
    return [r,t]

def scene(elements, bg="#ffffff"):
    return {"type":"excalidraw","version":2,"source":"https://excalidraw.com",
            "elements":elements,"appState":{"viewBackgroundColor":bg},"files":{}}

# Color palette
C_BLUE="#a5d8ff"; C_GREEN="#b2f2bb"; C_YELLOW="#ffec99"; C_RED="#ffc9c9"
C_PURPLE="#eebefa"; C_GRAY="#e9ecef"; C_ORANGE="#ffd8a8"

# ── 1. Business Architecture (业务架构) ──────────────────────────────────────
def biz_arch():
    e = []
    e += [text(280,20,"电商业务架构图",24)]
    e += region(40,70,720,140,"用户层")
    e += box(80,110,140,60,"Web商城",C_BLUE)
    e += box(260,110,140,60,"移动App",C_BLUE)
    e += box(440,110,140,60,"小程序",C_BLUE)
    e += box(620,110,120,60,"后台管理",C_BLUE)
    e += region(40,230,720,140,"业务服务层")
    e += box(80,270,120,60,"商品服务",C_GREEN)
    e += box(230,270,120,60,"订单服务",C_GREEN)
    e += box(380,270,120,60,"支付服务",C_GREEN)
    e += box(530,270,120,60,"用户服务",C_GREEN)
    e += box(680,270,80,60,"搜索",C_GREEN)
    e += region(40,390,720,120,"数据层")
    e += box(80,420,140,60,"MySQL集群",C_GRAY)
    e += box(260,420,140,60,"Redis缓存",C_PURPLE)
    e += box(440,420,140,60,"ElasticSearch",C_GRAY)
    e += box(620,420,120,60,"MQ消息",C_GRAY)
    e += arrow(150,170,150,270); e += arrow(330,170,290,270)
    e += arrow(510,170,440,270); e += arrow(680,170,720,270)
    e += arrow(140,330,150,420); e += arrow(290,330,330,420)
    e += arrow(440,330,510,420); e += arrow(590,330,680,420)
    return scene(e)

# ── 2. Deployment Architecture (部署架构) ────────────────────────────────────
def deploy_arch():
    e=[]
    e+=[text(260,20,"Kubernetes部署架构",24)]
    e+=region(40,70,720,360,"K8s Cluster")
    e+=box(80,110,160,50,"Ingress\nController",C_BLUE,16)
    e+=box(280,110,160,50,"API Gateway",C_BLUE)
    e+=box(500,110,200,50,"Load Balancer",C_BLUE)
    e+=region(70,190,300,200,"API Pods")
    e+=box(90,220,120,50,"API Pod 1",C_GREEN)
    e+=box(230,220,120,50,"API Pod 2",C_GREEN)
    e+=box(90,290,120,50,"API Pod 3",C_GREEN)
    e+=box(230,290,120,50,"Pod N",C_GREEN)
    e+=region(410,190,300,200,"Data Pods")
    e+=box(430,220,120,50,"MySQL\n(Primary)",C_GRAY,16)
    e+=box(570,220,120,50,"MySQL\n(Replica)",C_GRAY,16)
    e+=box(430,290,120,50,"Redis\nCluster",C_PURPLE,16)
    e+=box(570,290,120,50,"ES Nodes",C_GRAY)
    e+=box(80,420,300,40,"Auto Scaler",C_YELLOW)
    e+=arrow(160,160,150,220); e+=arrow(360,160,290,220)
    e+=arrow(600,160,500,220); e+=arrow(210,270,230,270)
    e+=arrow(550,270,570,270); e+=arrow(150,360,180,420)
    return scene(e)

# ── 3. Flowchart (流程图) ────────────────────────────────────────────────────
def flowchart():
    e=[]
    e+=[text(250,20,"用户注册流程",24)]
    e+=ellipse(280,70,140,60,"开始",C_GREEN)
    e+=box(270,160,160,50,"填写手机号",C_BLUE)
    e+=box(270,240,160,50,"发送验证码",C_BLUE)
    e+=box(270,320,160,50,"输入验证码",C_BLUE)
    e+=diamond(270,400,160,80,"验证\n成功?",C_YELLOW,16)
    e+=box(500,420,140,50,"重新输入",C_RED)
    e+=box(270,520,160,50,"创建账户",C_GREEN)
    e+=ellipse(280,610,140,60,"完成",C_GREEN)
    e+=arrow(350,130,350,160); e+=arrow(350,210,350,240)
    e+=arrow(350,290,350,320); e+=arrow(350,370,350,400)
    e+=arrow(430,440,500,440); e+=arrow(570,470,570,340,dashed=True)
    e+=arrow(570,340,430,340,dashed=True)
    e+=arrow(350,480,350,520); e+=arrow(350,570,350,610)
    return scene(e)

# ── 4. Sequence Diagram (时序图) ────────────────────────────────────────────
def sequence():
    e=[]
    e+=[text(40,20,"支付时序图",24)]
    actors=[("用户",60),("API网关",260),("支付服务",460),("银行",660)]
    for name,x in actors:
        e+=box(x-50,60,100,40,name,C_BLUE,16)
        e+=line(x,100,x,560)
    def msg(y,x1,x2,label,dashed=False):
        e.append(arrow(x1,y,x2,y,dashed=dashed))
        mx=(x1+x2)//2-30
        e.append(text(mx,y-22,label,13))
    msg(140,60,260,"发起支付"); msg(170,260,460,"创建订单")
    msg(200,460,660,"扣款请求"); msg(240,660,460,"扣款成功",dashed=True)
    msg(280,460,260,"支付成功",dashed=True); msg(320,260,60,"返回结果",dashed=True)
    e+=box(200,580,300,40,"saga事务补偿",C_RED,16)
    return scene(e)

# ── 5. ER Diagram (实体关系图) ───────────────────────────────────────────────
def er_diagram():
    e=[]
    e+=[text(40,20,"订单系统ER图",24)]
    e+=box(60,70,160,50,"用户 users",C_GREEN)
    e+=box(60,140,160,30,"id, name, phone",C_GRAY,13)
    e+=box(340,70,160,50,"订单 orders",C_GREEN)
    e+=box(340,140,160,30,"id, total, status",C_GRAY,13)
    e+=box(620,70,160,50,"商品 products",C_GREEN)
    e+=box(620,140,160,30,"id, name, price",C_GRAY,13)
    e+=box(340,300,160,50,"订单项 items",C_YELLOW)
    e+=box(340,370,160,30,"id, qty, price",C_GRAY,13)
    e+=text(240,80,"1 : N",14)
    e+=text(520,80,"1 : N",14)
    e+=text(400,230,"1 : N",14)
    e+=text(560,310,"N : 1",14)
    e+=line(220,95,340,95); e+=line(500,95,620,95)
    e+=line(420,170,420,300); e+=line(500,325,620,160)
    return scene(e)

# ── 6. State Machine (状态机) ────────────────────────────────────────────────
def state_machine():
    e=[]
    e+=[text(40,20,"订单状态机",24)]
    e+=ellipse(60,80,120,50,"待支付",C_YELLOW)
    e+=ellipse(280,80,120,50,"已支付",C_BLUE)
    e+=ellipse(500,80,120,50,"已发货",C_GREEN)
    e+=ellipse(500,200,120,50,"已完成",C_GREEN)
    e+=ellipse(280,200,120,50,"已取消",C_RED)
    e+=arrow(180,105,280,105); e+=text(210,85,"支付",13)
    e+=arrow(400,105,500,105); e+=text(430,85,"发货",13)
    e+=arrow(560,130,560,200); e+=text(575,160,"签收",13)
    e+=arrow(280,130,280,200); e+=text(295,160,"取消",13)
    e+=arrow(340,200,500,200); e+=text(400,180,"超时取消",13)
    return scene(e)

# ── 7. Mindmap (思维导图) ────────────────────────────────────────────────────
def mindmap():
    e=[]
    e+=[text(280,20,"产品规划思维导图",24)]
    e+=ellipse(330,100,140,60,"核心产品",C_PURPLE)
    branches=[("用户增长",60,200,C_BLUE),("商业化",300,200,C_GREEN),
              ("技术架构",560,200,C_YELLOW),("运营策略",300,320,C_RED)]
    for name,x,y,c in branches:
        e+=ellipse(x,y,140,50,name,c,16)
        e+=line(400,130,x+70,y)
    subs={"用户增长":[("拉新",20,280),("留存",120,320),("召回",60,360)],
          "商业化":[("订阅",280,280),("广告",420,280),("增值",350,360)],
          "技术架构":[("微服务",540,280),("监控",660,280),("CI/CD",600,360)]}
    for branch,items in subs.items():
        for sname,sx,sy in items:
            e+=box(sx,sy,90,36,sname,C_GRAY,14)
    return scene(e)

# ── 8. Network Topology (网络拓扑) ───────────────────────────────────────────
def topology():
    e=[]
    e+=[text(40,20,"网络拓扑图",24)]
    e+=ellipse(340,60,120,50,"Internet",C_BLUE)
    e+=box(330,150,140,50,"防火墙",C_RED)
    e+=box(330,230,140,50,"路由器",C_YELLOW)
    e+=region(60,310,280,160,"DMZ区")
    e+=box(90,340,100,40,"Web服务器",C_GREEN,14)
    e+=box(210,340,100,40,"API服务器",C_GREEN,14)
    e+=box(150,400,100,40,"负载均衡",C_GREEN,14)
    e+=region(400,310,320,160,"内网区")
    e+=box(420,340,100,40,"数据库",C_GRAY,14)
    e+=box(540,340,100,40,"缓存",C_PURPLE,14)
    e+=box(480,400,100,40,"文件存储",C_GRAY,14)
    e+=arrow(400,110,400,150); e+=arrow(400,200,400,230)
    e+=arrow(360,280,200,340); e+=arrow(420,280,520,340)
    e+=line(200,360,150,400); e+=line(540,360,500,400)
    return scene(e)

# ── 9. User Journey (用户旅程图) ────────────────────────────────────────────
def journey():
    e=[]
    e+=[text(280,20,"购物用户旅程图",24)]
    stages=[("发现",80,C_GREEN),("浏览",240,C_BLUE),("决策",400,C_YELLOW),
            ("购买",560,C_GREEN),("收货",720,C_BLUE),("复购",880,C_GREEN)]
    for i,(name,x,c) in enumerate(stages):
        e+=box(x,80,120,40,name,c,16)
        e+=text(x+10,140,f"触点:{name}",13)
        e+=text(x+10,170,"评分:",13)
        for star in range(5):
            fill = C_YELLOW if star < (4-i%2) else C_GRAY
            e+=ellipse(x+10+star*22,200,18,18,"",fill,1)
    e+=text(40,250,"情绪曲线:",16)
    pts_y=[280,260,270,240,250,230]
    for i in range(len(stages)-1):
        x1=stages[i][1]+60; x2=stages[i+1][1]+60
        e+=line(x1,pts_y[i],x2,pts_y[i+1])
    return scene(e)

# ── 10. Component Diagram (组件关系图) ──────────────────────────────────────
def component():
    e=[]
    e+=[text(280,20,"系统组件关系图",24)]
    e+=box(300,60,200,50,"前端应用\n(Frontend)",C_BLUE,16)
    e+=box(300,150,200,50,"API Gateway",C_YELLOW)
    e+=region(60,230,260,200,"核心服务")
    e+=box(90,260,100,40,"Auth",C_GREEN,14)
    e+=box(210,260,90,40,"User",C_GREEN,14)
    e+=box(90,320,100,40,"Order",C_GREEN,14)
    e+=box(210,320,90,40,"Payment",C_GREEN,14)
    e+=region(420,230,320,200,"基础设施")
    e+=box(440,260,120,40,"数据库",C_GRAY,14)
    e+=box(580,260,120,40,"消息队列",C_GRAY,14)
    e+=box(440,330,120,40,"缓存",C_PURPLE,14)
    e+=box(580,330,120,40,"日志系统",C_GRAY,14)
    e+=box(300,460,200,40,"监控告警",C_RED,16)
    e+=arrow(400,110,400,150); e+=arrow(360,200,190,260)
    e+=arrow(440,200,530,260); e+=line(140,300,210,280)
    e+=line(490,300,580,280); e+=arrow(400,480,400,440,dashed=True)
    return scene(e)

# ── generate all ─────────────────────────────────────────────────────────────
DIAGRAMS = [
    ("01-business-architecture", biz_arch),
    ("02-deployment-architecture", deploy_arch),
    ("03-flowchart", flowchart),
    ("04-sequence-diagram", sequence),
    ("05-er-diagram", er_diagram),
    ("06-state-machine", state_machine),
    ("07-mindmap", mindmap),
    ("08-network-topology", topology),
    ("09-user-journey", journey),
    ("10-component-diagram", component),
]

if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    for name, fn in DIAGRAMS:
        PID[0] = 0  # reset id counter
        s = fn()
        path = f"{out_dir}/{name}.excalidraw"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False)
        print(f"  {path}  ({len(s['elements'])} elements)")
    print(f"\nGenerated {len(DIAGRAMS)} diagrams.")
