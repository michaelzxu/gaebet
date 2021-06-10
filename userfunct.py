from replit import db
from datetime import date, timedelta
import time
import random
superusr="GaeBolg#4816"

def reg(usr):
  if usr in db["user"].keys():
    return "用户"+str(usr)+"已经存在！"
  else:
    db["user"][usr]={'gae':1500,"date":(date.today()-timedelta(days=1)).isoformat()}
    return "注册"+usr+"成功！您的余额是1500 gae"

def gae(usr):
  if usr not in db["user"].keys():
     return "用户不存在！请用!new 注册新账户！"
  else:
    epochtolocal = time.localtime()
    bonus=0
    if usr in db["user"].keys():
      today=date.today()
      odate=db["user"][usr]["date"]
      odate=date.fromisoformat(odate)
      if odate!=today:
        bonus=int(50+random.random()*100)
        db["user"][usr]["gae"]+=bonus
      db["user"][usr]["gae"]=int(db["user"][usr]["gae"])
      db["user"][usr]["date"]=today.isoformat()
    if bonus!=0:
        s="恭喜你！领到今天签到福利"+str(bonus)+" gae！"
    else: s=''
    s+=usr[:-5]+"的账户余额是"+str(db["user"][usr]['gae'])+" gae\nUTC "+time.strftime("%A %B %d %H:%M %Y", epochtolocal)
    return s

def send(trans):
  unit=trans["unit"]
  amt=trans["amt"]
  fr=trans["from"]
  to=trans["to"]
  if fr not in db["user"].keys():
      return "发款用户不存在！请用!new 注册新账户！"
  elif to not in db["user"].keys():
      return "收款用户不存在！"
  else:
    rand_amt = int( random.normalvariate(0, 5) )
    if unit=='bmw': unitn=50
    elif unit=='airplane': unitn=100
    elif unit=='rocket': unitn=500
    elif unit=='spaceship': unitn=1000
    elif unit=='fuck': unitn=rand_amt
    elif unit==1: unitn=1
    else: return "请输入转账数量或者使用以下代码：bmw=50 gae, airplane=100 gae, rocket=500 gae, spaceship=1000 gae."
    tamt=amt*unitn
    if tamt>db['user'][fr]['gae']:
        return "对不起，您的余额不足本次转账！"
    else:
      db['user'][fr]['gae']-=tamt
      db['user'][to]['gae']+=tamt
      if unit=='fuck':
        if 'fuck_cnt' in db['user'][to].keys():
          db['user'][to]['fuck_cnt'] += 1
          db['user'][to]['fuck_amt'] += rand_amt
        else:
          db['user'][to]['fuck_cnt'] = 1
          db['user'][to]['fuck_amt'] = rand_amt
      if unit==1:
          return fr[:-5]+"成功转账"+str(tamt)+" gae币到账户"+to[:-5]+". 您的账户余额是："+str(db['user'][fr]['gae'])+' gae.'
      elif unit=='bmw':
          unit='宝马！'
          cnt='辆'
      elif unit=='airplane':
          unit='大飞机！'
          cnt='架'
      elif unit=='spaceship':
          unit='星舰！'
          cnt='艘'
      elif unit=='rocket':
          unit='火箭！'
          cnt='个'
      if unit == 'fuck':
          if rand_amt == 0:
              return f"{fr[:-5]} 和 {to[:-5]} 淦了一夜互有进出，最终和平分手"
          elif rand_amt < 0:
              rr = random.random()
              return f"{fr[:-5]} 淦了一把 {to[:-5]} 但对方竟然付了自己{abs(rand_amt)}GAE"
          elif rand_amt > 0:
              return f"{fr[:-5]} 淦了一把 {to[:-5]} 潇洒完后付了{abs(rand_amt)}GAE"
      if unit!=1:
          return fr[:-5]+"送给"+to[:-5]+" "+str(amt)+" "+cnt+unit

def go(betdata):
  bid=betdata["bid"]
  usr=betdata["usr"]
  pid=betdata["pid"]
  gae=betdata["gae"]
  if db["book"][bid]["status"]=="active":
    pp=db["book"][bid]["team"][pid]
    odd=db["book"][bid]["odd"][pid]
    db["user"][usr]["gae"]-=gae
    db["book"][bid]["lm"][pid]-=gae
    if usr in db["book"][bid]["bets"].keys():
        db["book"][bid]["bets"][usr].append([pp,odd,gae])
    else:
        db["book"][bid]["bets"][usr]=[[pp,odd,gae]]
    return usr[:-5]+"押注成功！Book ID "+bid+":\t" + pp +" "+str(gae) +" gae at "+str(odd)

def list():
      books={}
      for bid in db["book"].keys():
        r1=db["book"][bid]["odd"][0]
        r2=db["book"][bid]["odd"][1]
        p1=db["book"][bid]["team"][0]
        p2=db["book"][bid]["team"][1]
        lm1=db["book"][bid]["lm"][0]
        lm2=db["book"][bid]["lm"][1]
        bm=db["book"][bid]["bm"]
        if bm!="gaebet":
          bm=bm[:-5]
        line1 = '{player1:{fill}^21}vs{player2:{fill}^21}'.format(
          player1=p1, player2=p2,
          fill=' ')
        line2 = '{stats1:{fill}^21} {stats2:{fill}^21} '.format(
              stats1='{odd1} ({lmt1})'.format(odd1=r1, lmt1=lm1), 
              stats2='{odd2} ({lmt2})'.format(odd2=r2, lmt2=lm2),
              fill=' ')
        #separator = '-'*44
        line3 = '{status:{fill}^21}  {host:{fill}^21}'.format(
              status="status: " + db["book"][bid]["status"],
              #result="结果: " + db["book"][bid]["result"], 
              host="BookMaker: "+bm,
              fill=' ')
        books[bid]='\n'.join([line1, line2, line3])
      return books

def bets(usr):
    
    betexist=0
    for bid in db["book"].keys():
      if usr in db["book"][bid]["bets"].keys():
        betexist=1
        break
    if betexist==0:
      return "您没有任何押注！"
    else:
      betrec=''
      for bid in db["book"].keys():
        if usr in db["book"][bid]["bets"].keys():
          bets = db["book"][bid]["bets"][usr]
          for rec in bets:
            pp=rec[0]
            odd=rec[1]
            gae=int(rec[2])
            betrec+="Book ID "+bid+": 押注"+pp+" "+str(gae)+" gae，赔率"+str(odd)+"\n"
      return betrec

def top(topn, format="text"):
  if format == "list":
    return [(i[0], i[1]["gae"], i[1].get("fuck_cnt", ''), i[1].get("fuck_amt", '')) for i in sorted(db["user"].items(), key=lambda item: (-item[1]["gae"], item[0])) if i[0] != "gaebet"]
  else:
    s = ''
    top=dict(sorted(db["user"].items(), key=lambda item: -item[1]["gae"]))
    i=1
    topn=min(topn, len(db["user"].keys())-1)
    maxn=0
    for usr in db["user"].keys():
      if db["user"][usr]["gae"]>maxn: maxn=db["user"][usr]["gae"]
    maxn=len(str(maxn))
    for k in top.keys():
      if i<=topn and k!="gaebet":
        usr=k[:-5]
        s+="\n"+("`#"+str(i)).ljust(4)+" "+usr[:16].ljust(20)+str(int(db["user"][k]["gae"])).rjust(maxn)+"`"
        i+=1
    return s

