from replit import db

def book(bookdata):
  bm=bookdata["bm"]
  team=bookdata["team"]
  odd=bookdata["odd"]
  bgae=bookdata["bgae"]
  lm=[int(bgae/odd[0]),int(bgae/odd[1])]
  if len(db["book"].keys())>=5:
    for bid in db["book"].keys():
      if db["book"][bid]["status"]=="ended":
        del db["book"][bid]
  
  if len(db["book"].keys())==0:
    nbook=1
  else:
    nbook=int(max(db["book"].keys()))+1
  
  db["book"][str(nbook)]={
    'bm':bm,
    'team':team,
    'odd':odd,
    'bgae':bgae,
    'lm':lm, 
    'status':'active','result':'tbd',
    'bets':{} }
  db["user"][bm]['gae']-=bgae
  if bm!="gaebet":
    bm=bm[:-5]
  line1 = '{player1:^21}vs{player2:^21}'.format(player1=team[0], player2=team[1])
  line2 = '{stats1:^21}  {stats2:^21}'.format(
        stats1='{odd1} ({lmt1})'.format(odd1=odd[0], lmt1=lm[0]), 
        stats2='{odd2} ({lmt2})'.format(odd2=odd[1], lmt2=lm[1]))
  #separator = '-'*44
  line3 = '{status:^21}  {host:^21}'.format(
        status="status: " + db["book"][str(nbook)]["status"],
        #result="结果: " + db["book"][str(nbook)]["result"], 
        host="BookMaker: "+bm)
  return [str(nbook), '\n'.join([line1,line2,line3]), f"{bm}开了新盘口：{team[0]} ({odd[0]}) --vs-- {team[1]} ({odd[1]})"]

def close(data):
  bm=data["bm"]
  bid=data["bid"]
  if bm==db["book"][bid]["bm"]:
    db["book"][bid]["status"]="close"
    return "Book ID "+bid +": \t 庄家暂停接受押注！"
  else:
    return "只有庄家可以修改状态！!open [book-ID]"

def open(data):
  bm=data["bm"]
  bid=data["bid"]
  if bm==db["book"][bid]["bm"]:
    db["book"][bid]["status"]="active"
    return "Book ID "+bid +": \t 庄家重新接受押注！"
  else:
    return "只有庄家可以修改状态！!open [book-ID]"

def odd(data):
  bid=data["bid"]
  nr=data["odd"]
  lm1=db["book"][bid]["lm"][0]
  lm2=db["book"][bid]["lm"][1]
  r1=db["book"][bid]["odd"][0]
  r2=db["book"][bid]["odd"][1]
  nr1=nr[0]
  nr2=nr[1]
  db["book"][bid]["odd"][0]=nr1
  db["book"][bid]["odd"][1]=nr2
  db["book"][bid]["lm"][0]=int(lm1*r1/nr1)
  db["book"][bid]["lm"][1]=int(lm2*r2/nr2)
  msg="BookID "+bid+"赔率改为："+str(nr1)+" : "+str(nr2)
  return msg

def result(result_data):
  bid=result_data["bid"]
  code=result_data["win"]-1
  tt=0
  pf=0
  bm=db["book"][bid]["bm"]
  usrgl=''
  gae = 0
  if code==0 or code==1:
    win=db["book"][bid]["team"][code]
    for usr in db["book"][bid]["bets"].keys():
      for betrec in db["book"][bid]["bets"][usr]:
        pp=betrec[0]
        odd=betrec[1]
        gae=int(betrec[2])
        tt+=gae
        if pp==win:
          db["user"][usr]["gae"]+=int(gae*(1+odd))
          pf-=int(gae*(odd))
          usrgl+=usr[:-5]+"押注胜利方"+str(gae)+" gae，获利"+str(int(gae*(odd)))+" gae. \n"
        else:
          pf+=gae
          usrgl+=usr[:-5]+"押注失败方"+str(gae)+" gae，亏损"+str(int(gae))+" gae. \n"
    db["user"][bm]["gae"]+=pf+db["book"][bid]["bgae"]
    if pf>=0:
      wl='盈利'
    else:
      wl='亏损'
    db["book"][bid]['status']='ended'
    msg="本盘（ID "+bid+"）结算完毕！胜利方："+win+"。总押注量："+str(tt)+" gae. 庄家"+wl+"："+str(abs(pf))+" gae币。\n"+usrgl
    db["book"][bid]['result']="胜利方："+win
    db["book"][bid]['summary']=msg
    return msg
  elif code==2:
    for usr in db["book"][bid]["bets"].keys():
      for bet in db["book"][bid]["bets"][usr]:
        db["user"][usr]["gae"]+=bet[2]
        usrgl+="返还"+usr[:-5]+str(int(gae))+" gae. \n"
    db["user"][bm]["gae"]+=db["book"][bid]["bgae"]
    db["book"][bid]['status']='ended'
    db["book"][bid]['result']="平局"
    msg="本盘（ID "+bid+"）结算完毕！gae币全部返还玩家。\n"+usrgl
    db["book"][bid]['summary']=msg
    return msg