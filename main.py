import discord
import os
import datetime
import time
from replit import db
from wake import wake
from commands import COMMANDS
from utils import choose_status_embed_color
import random

#intents = intents.all()
def isnumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

client = discord.Client()
init=1
superusr="GaeBolg#4816"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
        return
  #super user commands
  if message.content.startswith('!init') and str(message.author)==superusr:
        for dd in db.keys():
          del db[dd]
        db["gaebet"]=15000000
        await message.channel.send("Server initiated!")
  #add
  if message.content.startswith('!add') and str(message.author)==superusr:
      s=str(message.content)
      if s[5:] in db.keys():
        await message.channel.send("该用户已经存在！")
      else:
        db[s[5:]]=1500
        st="User "+s[5:]+" added!"
        await message.channel.send(st)
  #del
  if message.content.startswith('!del') and str(message.author)==superusr:
      s=str(message.content)
      if s[5:] in db.keys():
        del db[s[5:]]
        st="User "+s[5:]+" deleted!"
        await message.channel.send(st)
      else:
        await message.channel.send("该用户不存在！")
  if message.content.startswith('!set') and str(message.author)==superusr:
      s=str(message.content)
      if s[5:] in db.keys():
        db[s[5:]]=155
        st="User "+s[5:]+" reset!"
        await message.channel.send(st)
      else:
        await message.channel.send("该用户不存在！")
  #users
  #register
  if message.content.startswith('!new'):
    if str(message.author) in db.keys():
      msg="用户"+str(message.author)+"已经存在！"
      await message.channel.send(msg)
    else:
      db[str(message.author)]=1500
      await message.channel.send("注册"+str(message.author)+"成功！您的余额是1500 gae")
  #account balance
  if message.content.startswith('!gae'):
    if str(message.author) not in db.keys():
        await message.channel.send("用户不存在！请用!new 注册新账户！")
    else:
        epochtolocal = time.localtime()
        s="您的账户余额是"+str(db.get(str(message.author),"0"))+" gae\nUTC "+time.strftime("%A %B %d %H:%M %Y", epochtolocal)
        #embed=discord.Embed(
        #  title="您的账户余额是", 
        #  description=s,
        #  color=discord.Color.blue())
        await message.channel.send(s)
  #placing bet !go betID player
  if message.content.startswith('!go'):
    s=str(message.content)
    sl=s.split(" ")
    nbook=0
    book = open("book")
    for row in book:
        srow=row.split(",")
        if int(srow[1])>nbook: nbook=int(srow[1])
    if len(sl)==4 and isnumber(sl[1]) and int(sl[1]) in range(1,nbook+1):
      betid=sl[1]
      pp=sl[2]
      gae=int(sl[3])
      rate=0
      with open("limits","r") as limits:
        for lmline in limits:
          lms=lmline.split(",")
          if betid==lms[0]:
            r1=float(lms[2])
            r2=float(lms[3])
            lm1=int(float(lms[4]))
            lm2=int(float(lms[5]))
      book = open("book")
      for row in book:
        rs=row.split(",")
        if betid==rs[1]:          
          if pp==rs[2] and rs[-3]=="active" and str(message.author)!=rs[0]:
            if 0<gae<=lm1:
              rate=r1
              lm1-=gae
              lmlines=[]
              with open("limits","r") as limits:
                for line in limits:
                  lines=line.split(",")
                  if betid!=lines[0]:
                    lmlines.append(line)
                  else:
                    lines[4]=str(lm1)
                    lmlines.append(",".join(lines))
              with open("limits","w") as limits:
                limits.writelines(lmlines)
            else:
              await message.channel.send("盘口不足，请押注该选手限额(limit)以内。")
          elif pp==rs[3] and rs[-3]=="active" and str(message.author)!=rs[0]:
            if 0<gae<=lm2:
              rate=r2
              lm2-=gae
              lmlines=[]
              with open("limits","r") as limits:
                for line in limits:
                  lines=line.split(",")
                  if betid!=lines[0]:
                    lmlines.append(line)
                  else:
                    lines[5]=str(lm2)
                    lmlines.append(",".join(lines))
              with open("limits","w") as limits:
                limits.writelines(lmlines)
            else:
              await message.channel.send("盘口不足，请押注该选手限额(limit)以内。")
      book.close()
      if rate==0 or gae>db.get(str(message.author)):
        await message.channel.send("押注失败！押注请使用!go [bet-ID] [team id] [amount]")
      else:
        with open("bets", "a") as bet:
          bet.write(",".join([str(message.author),betid,pp,str(gae),str(rate)+"\n"]))
        db[str(message.author)]-=gae
        wgae=int(gae*(1+rate))
        msg=str(message.author)+"成功押注：betID-" +str(betid)+"\t\t选手："+pp+"\t\t数额："+str(gae)+" gae"+"\t\t赔率："+str(rate)+"\t\t您的余额是："+str(db[str(message.author)])+" gae. 如果获胜将获得："+str(wgae)+" gae"
        await message.channel.send(msg)
    else:
        await message.channel.send("请检查押注信息格式")
  #view active betting and rates
  if message.content.startswith('!list'):
    nbook=0
    embed = discord.Embed(
      #title='',
      color=discord.Color.blue())
    with open("book") as book:
        for row in book:
          bs=row.split(",")
          lm1=''
          lm2=''
          with open("limits","r") as limits:
            for lmline in limits:
              lms=lmline.strip('\n').split(",")
              if bs[1]==lms[0]:
                lm1=lms[4]
                lm2=lms[5]
          line1 = '{player1:^21}vs{player2:^21}'.format(player1=bs[2], player2=bs[3])
          line2 = '{stats1:^21} {stats2:^21} '.format(
            stats1='{odd1} ({lmt1})'.format(odd1=bs[4], lmt1=lm1), 
            stats2='{odd2} ({lmt2})'.format(odd2=bs[5], lmt2=lm2))
          separator = '-'*44
          line3 = ' {status:^10} {result:^11} {host:^16}'.format(
            status="状态: " + bs[6],
            result="结果: " + bs[7], 
            host="庄家: "+bs[0])
          embed.add_field(
            name="betID\t"+bs[1], 
            value='`{bet_list}`'.format(bet_list='\n'.join(
              [line1, separator, line2, separator, line3])), inline=False)
          nbook+=1
    if nbook==0:
      await message.channel.send("没有庄家开盘！")
    else:
      await message.channel.send(embed=embed)
  #view top players:
  if message.content.startswith('!top'):
    try:
      topn = int(message.content.replace("!top", ""))
    except:
      topn = 10
    s = ''
    top=dict(sorted(db.items(), key=lambda item: -item[1]))
    s = "`\n".join([f"`#{i+1:02}: {k[:15]:<16}|{([f'{v/uv:,.2f}{uk}`' for uk, uv in {'M': 10**6, 'B': 10**9, 'T': 10**12}.items() if 1000 > v/uv > 0.8] or [f'{v:,}'])[0]:>8}" for i, (k,v) in enumerate(top.items()) if i < topn and k!= "gaebet"]) + "`"
    embed=discord.Embed(
      #title="", 
      color=discord.Color.blue())
    embed.add_field(name='GAE排行榜Top {}'.format(str(topn)), value=s)
    await message.channel.send(embed=embed)
  #BookMaker:
  #!book alex unreal 1.0 0.7 300
  if message.content.startswith('!book'):
    s=str(message.content)
    sl=s.split(" ")
    p1=sl[1]
    p2=sl[2]
    nbook=0
    book = open("book")
    for row in book:
      rows=row.split(",")
      if int(rows[1])>nbook: nbook=int(rows[1])
    book.close()
    if len(sl)==6 and isnumber(sl[-3]) and isnumber(sl[-2]) and sl[-1].isnumeric():
      r1=int(100*float(sl[-3]))
      r2=int(100*float(sl[-2]))
      gae=int(sl[-1])
      nbook+=1
      if 1<=r1<=999 and 1<=r2<=999 and 300<=gae:
        with open("book", "a") as book:
          book.write(",".join([str(message.author),str(nbook),p1,p2,str(r1/100.00), str(r2/100.00),"active","tbd,"+sl[-1]+"\n"]))
        lm1=int(int(sl[-1])/float(r1)*100)
        lm2=int(int(sl[-1])/float(r2)*100)
        with open("limits", "a") as limits:
          limits.write(",".join([str(nbook),sl[-1],str(r1/100.00), str(r2/100.00), str(lm1), str(lm2)+"\n"]))
        msg="庄家-"+str(message.author)+"-开始接受押注：betID-"+str(nbook)+"\t\t\t"+p1+" vs "+p2 +"\t\t\t(lmt: "+str(lm1)+") "+str(r1/100.00)+"  :  "+str(r2/100.00)+" (lmt: "+str(lm2)+")"
        await message.channel.send(msg)
      else:
        await message.channel.send("请确保赔率在0.01到9.99范围内，庄家必须押注300 gae以上。")
    else:
        await message.channel.send("开盘请使用!book [team1-id] [team2-id] [rate1] [rate2] [amount]")
  #close a list
  if message.content.startswith('!close'):
    lid=str(message.content).split(" ")
    nbook=[]
    with open("book", "r") as book:
      for line in book:
        lines=line.split(",")
        nbook.append(lines[1])
    if len(lid) ==2 and lid[1].isnumeric() and lid[1] in nbook:
      iline=[]
      rev=0
      inum=0
      with open("book","r") as book:
        for line in book:
          xx=line.split(",")
          iline.append(xx)
          if xx[0]==str(message.author) and xx[1]==lid[1]:
            iline[-1][-3]="closed"
            msg="betID-"+lid[1]+"停止押注"
            await message.channel.send(msg) 
            rev=1
      if rev==1:
        with open("book","w") as book:
          for i in range(0,len(iline)):
            s=",".join(iline[i])
            book.write(s)
    else:
        await message.channel.send("没有该记录！!close [bet-ID]")
  #reopen a list
  if message.content.startswith('!open'):
    lid=str(message.content).split(" ")
    nbook=[]
    with open("book", "r") as book:
      for line in book:
        lines=line.split(",")
        nbook.append(lines[1])
    if len(lid) ==2 and lid[1].isnumeric() and lid[1] in nbook:
      iline=[]
      rev=0
      with open("book","r") as book:
        for line in book:
          xx=line.split(",")
          iline.append(xx)
          if xx[0]==str(message.author) and xx[1]==lid[1]:
            iline[-1][-3]="active"
            msg="ID-"+lid[1]+"开放押注"
            await message.channel.send(msg) 
            rev=1
      if rev==1:
        with open("book", "w") as book:
          for i in range(0,len(iline)):
            s=",".join(iline[i])
            book.write(s)
    else:
        await message.channel.send("没有该记录！!open [bet-ID]")
  #result
  if message.content.startswith('!result'):
    lid=str(message.content).split(" ")
    nbook=[]
    with open("book", "r") as book:
      for line in book:
        lines=line.split(",")
        nbook.append(lines[1])
    if len(lid) ==3 and lid[1].isnumeric() and lid[2].isnumeric() and lid[1] in nbook and int(lid[2]) in range(0,4):
      iline=[]
      rev=0
      with open("book","r") as book:
        for line in book:
          xx=line.split(",")
          iline.append(xx)
          if xx[0]==str(message.author) and xx[1]==lid[1]:
            if int(lid[2])==0:
              win="tbd"
            elif int(lid[2]) in range(1,3):
              win=xx[int(lid[2])+1]
              bgae=xx[-1]
            else:
              win="平局"
            iline[-1][-2]=win
            rev=1
      if rev==1:
        with open("book","w") as book:  
          for i in range(0,len(iline)):
            s=",".join(iline[i])
            book.write(s)
    #calculate results and revise user gaes:
      if win=="tbd":
        return
      else:
        pf=0
        tt=0
        with open ("bets","r") as bets:
            for line in bets:
              lines=line.split(",")
              if lid[1]==lines[1] and win=="平局":
                db[lines[0]]+=int(lines[3])
                tt+=int(lines[3])
              elif lid[1]==lines[1] and win==lines[2]:
                db[lines[0]]+=int(int(lines[3])*(1+float(lines[4])))
                pf-=int(int(lines[3])*(float(lines[4])))
                tt+=int(lines[3])
              elif lid[1]==lines[1] and win!=lines[2]:
                pf+=int(lines[3])
                tt+=int(lines[3])
        db[str(message.author)]+=pf
        if pf>=0:
          wl="盈利："
        else:
          wl="亏损："
        msg="betID-"+lid[1]+"胜者："+win+".\ngae币结算完毕！总押注额为"+str(tt)+", 庄家"+wl+str(pf)+" gae."
        await message.channel.send(msg) 
        #删除bets记录
        iline=[]
        with open ("bets","r") as bets:
          for line in bets:
            lines=line.split(",")
            if lid[1]!=lines[1]:
              iline.append(line)
        with open("bets","w") as bets:  
          for i in range(0,len(iline)):
            bets.write(iline[i])
        #删除book记录
        iline=[]
        with open ("book","r") as book:
          for line in book:
            lines=line.split(",")
            if lid[1]!=lines[1]:
              iline.append(line)
        with open("book","w") as book:
            book.writelines(iline)
        iline=[]
        with open ("limits","r") as lmt:
          for line in lmt:
            lines=line.split(",")
            if lid[1]!=lines[0]:
              iline.append(line)
        with open("limits","w") as lmt:
            lmt.writelines(iline)
    else:
        await message.channel.send("格式不对！结算请用!result [bet-ID] [code]\n code: 1-team1 wins, 2-team2 wins, 3-平局]")
  #rates
  if message.content.startswith('!rate'):
    lid=str(message.content).split(" ")
    nbook=[]
    with open("book", "r") as book:
      for line in book:
        lines=line.split(",")
        nbook.append(lines[1])
    if len(lid) ==4 and lid[1].isnumeric() and isnumber(lid[2]) and isnumber(lid[3]) and lid[1] in nbook and 0.01<=float(lid[2])<=9.99 and 0.01<=float(lid[3])<=9.99:
      iline=[]
      rev=0
      #0bm, 1betid, 2p1, 3p2, 4r1, 5r2, 6amount
      with open("book","r") as book:
        for line in book:
          xx=line.split(",")
          iline.append(xx)
          if xx[0]==str(message.author) and xx[1]==lid[1]:
            iline[-1][4]=lid[2]
            iline[-1][5]=lid[3]
            lm_line=[]
            with open("limits",'r') as limits:
              for line in limits:
                lines=line.split(",")
                if lines[0]!=lid[1]:
                  lm_line.append(line)
                else:
                  #id, bgae, r1, r2, lm1, lm2
                  r1=float(lines[2])
                  r2=float(lines[3])
                  lm1=int(float(lines[4]))
                  lm2=int(float(lines[5]))
                  bgae=min(lm1*r1,lm2*r2)
                  lines[1]=str(bgae)
                  lines[2]=lid[2]
                  lines[3]=lid[3]
                  r1=float(lid[2])
                  r2=float(lid[3])
                  lines[4]=str(int(bgae/r1))
                  lines[5]=str(int(bgae/r2))
                  lm_line.append(",".join(lines))
            with open("limits",'w') as limits:
              limits.writelines(lm_line)
            rev=1
            msg="betID-"+lid[1]+"赔率改为："+lid[2]+" : "+lid[3]
            await message.channel.send(msg) 
      if rev==1:
        with open("book","w") as book:  
          for i in range(0,len(iline)):
            s=",".join(iline[i])
            book.write(s)
    else:
        await message.channel.send("格式不对！修改赔率使用!rate [bet-ID] [rate1] [rate2]")
  if message.content.startswith('!ghelp'):
    embed = discord.Embed(
      title='gaebet指令',
      color=discord.Color.blue())
    for k,v in COMMANDS.items():
      embed.add_field(name="`"+k+"` "+v["usage"].replace(k, ""), value=v["description"], inline=False)
    await message.channel.send(embed=embed)
  if message.content.startswith('!web'):
    lid=str(message.content).split(" ")
    await message.author.send(lid[1])
  if message.content.startswith('!fuck'):
    msg = " ".join(message.content.split(" ")[1:])
    if "lulu" in msg.lower():
      amt = int( ( random.random() - 0.49 ) * 20 )
      db[str(message.author)] += amt
      await message.channel.send(f"淦得漂亮，奖励你{amt}gae！")
    elif any([x in msg.lower() for x in ["dqq", "一力挺", "mike"]]):
      db[str(message.author)] -= 5
      await message.channel.send("哪个没素质得辱骂程序员？肯定是lulu。提示:输入`!fuck lulu`可得5gae！")
    else:
      await message.channel.send("没有说出关键词！")
wake()
client.run(os.environ['token'])