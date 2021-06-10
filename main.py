import discord
import os
from datetime import date, timedelta
from replit import db
from wake import wake
from commands import COMMANDS
from utils import choose_status_embed_color
import random
import userfunct
import bookmaker

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
  if message.content=='!init' and str(message.author)==superusr:
    for k in db.keys():
      del db[k]
    db["user"] = {  "gaebet": {"gae": 1500000,      "date": date.today().isoformat() }               }
    db["user"][superusr]={"gae": 1500,      "date": (date.today()-timedelta(days=1)).isoformat() }
    db["book"] = {}
    await message.channel.send("Server initiated!")
  #add
  if message.content.startswith('!add') and str(message.author)==superusr:
      s=str(message.content)
      
      if s[5:] in db["user"].keys():
        await message.channel.send("该用户已经存在！")
      else:
        db["user"][s[5:]]={'gae':1500, 'date': date.today().isoformat()}
        st="User "+s[5:]+" added!"
        await message.channel.send(st)
  #del
  if message.content.startswith('!del') and str(message.author)==superusr:
      s=str(message.content)
      
      if s[5:] in db["user"].keys():
        del db["user"][s[5:]]
        st="User "+s[5:]+" deleted!"
        await message.channel.send(st)
      else:
        await message.channel.send("该用户不存在！")
  if message.content.startswith('!set') and str(message.author)==superusr:
      s=str(message.content)
      ss=s.split()
      try:
        gae=int(ss[2])
      except:
        gae=1500
      if ss[1] in db["user"].keys():
        db["user"][ss[1]]['gae']=gae
        db["user"][ss[1]]['date']=date.today().isoformat()
        if gae==1500:
          st="用户 "+ss[1]+" 已被重置！余额为 1500 gae."
        else:
          st="用户 "+ss[1]+" 余额改为"+str(gae)+" gae."
        await message.channel.send(st)
      else:
        await message.channel.send("该用户不存在！")

  if message.content.startswith('!date') and str(message.author)==superusr:
      usr=str(message.mentions[0])
      if usr in db["user"].keys():
        db["user"][usr]['date']=(date.today()-timedelta(days=1)).isoformat()
        st="用户 "+usr+"时间设为昨天！"
        await message.channel.send(st)
      else:
        await message.channel.send("该用户不存在！")
  #users
  #register
  if message.content.startswith('!new'):
    newuser=str(message.author)
    msg=userfunct.reg(newuser)
    await message.channel.send(msg)
  #account balance
  if message.content.startswith('!gae'):
    usr=str(message.author)
    msg = userfunct.gae(usr)
    await message.channel.send(msg)

  #!send @someone amt gae
  if message.content.startswith('!send'):
    amt=message.content.split()
    if len(amt)==4:
      unit=amt[3]
    else:
      unit=1
    if not amt[2].isnumeric():
      await message.channel.send("金额格式不对！请输入整数！")
    else:
      amt=int(amt[2])
      to=str(message.mentions[0])
      fr=str(message.author)
      trans={"from":fr, "to":to, "amt":amt, "unit":unit}
      msg=userfunct.send(trans)
      await message.channel.send(msg)
  
  #placing bet !go bookID player amount
  if message.content.startswith('!go'):
    s=str(message.content)
    sl=s.split()
    if len(sl)==4 and sl[1].isnumeric() and sl[1] in db["book"].keys():
      usr=str(message.author)
      if sl[3].isnumeric():
         gae=int(sl[3])
      elif sl[3]=="allin":
        gae=db["user"][usr]["gae"]
      else:
        await message.channel.send("请输入整数押注额或者使用allin押注所有余额。")
        return
      bid=sl[1]
      pp=sl[2]
      if bid not in db["book"].keys():
        await message.channel.send("没有该盘，请检查整数盘ID。")
        return
      if pp in db["book"][bid]["team"]:
        if pp==db["book"][bid]["team"][0]:
          pid=0
        elif pp==db["book"][bid]["team"][1]:
          pid=1
      else:
        await message.channel.send("押注失败！没有该选手。请检查拼写。")
        return
      if usr==superusr and db["book"][bid]["bm"]=="gaebet":
        usr="gaebet"
      if usr==db["book"][bid]["bm"]:
        await message.channel.send("押注失败！庄家不能押注自己开的盘。")
      elif db["book"][bid]["status"]=="closed":
        await message.channel.send("押注失败！庄家暂停接受押注！")
      elif gae>db["book"][bid]["lm"][pid]:
          await message.channel.send("盘口不足，请押注该选手限额(limit)以内。")
      elif gae>db["user"][usr]["gae"]:
        await message.channel.send("押注失败！您的余额不足。")
      else:
        betdata={"bid":bid,"usr":usr, "pid":pid, "gae":gae}
        msg=userfunct.go(betdata)
        await message.channel.send(msg)
    else: await message.channel.send("押注失败！押注请使用!go [book-ID] [team-id] [amount]")
  
  #view active betting and rates
  if message.content.startswith('!list'):
    if len(db["book"].keys())==0:
        msg="没有庄家开盘！"
        await message.channel.send(msg)
    else:
        embed = discord.Embed(
        #title='',
          color=discord.Color.blue())
        books=userfunct.list()
        for bid in books.keys():
          embed.add_field(
          name="Book ID\t"+bid, 
          value='`{bet_list}`'.format(bet_list=books[bid]), inline=False)
        await message.channel.send(embed=embed)
  
  #view my bets !bets
  if message.content.startswith('!bets'):
    usr=str(message.author)
    embed = discord.Embed(
      #title='',
        color=discord.Color.blue())
    betrec=userfunct.bets(usr)
    embed.add_field(
          name='用户'+usr+"现有押注记录：", 
          value=betrec) 
    await message.channel.send(embed=embed)

  #view top players:
  if message.content.startswith('!top'):
    try:
      topn = int(message.content.replace("!top", ""))
    except:
      topn = 10
    toplist=userfunct.top(topn)
    embed=discord.Embed(
      #title="", 
      color=discord.Color.blue())
    embed.add_field(name='GAE排行榜Top {}'.format(str(topn)), value=toplist)
    if toplist!='': await message.channel.send(embed=embed)
  
  #BookMaker:
  #!book alex unreal 1.0 0.7 300
  if message.content.startswith('!book'):
    s=str(message.content)
    sl=s.split()
    if len(sl)==6 and isnumber(sl[-3]) and isnumber(sl[-2]) and sl[-1].isnumeric():
      bm=str(message.author)
      if bm==superusr: bm="gaebet"
      p1=sl[1]
      p2=sl[2]
      r1=round(float(sl[-3]),2)
      r2=round(float(sl[-2]),2)
      bgae=int(sl[-1])
      lm1=int(bgae/r1)
      lm2=int(bgae/r2)
      if bgae>db["user"][bm]["gae"]:
        await message.channel.send("余额不足！")
      elif 0.01<=r1<=9.99 and 0.01<=r2<=9.99 and 300<=bgae:
        bookdata={"bm":bm, "team":[p1,p2],"odd":[r1,r2],"bgae":bgae}
        bookmsg=bookmaker.book(bookdata)
        embed = discord.Embed(
        #title='',
        color=discord.Color.blue())
        embed.add_field(
          name="庄家"+bm+"开盘成功！Book ID\t"+bookmsg[0], 
          value='`{bet_list}`'.format(bet_list=bookmsg[1]), inline=False)
        await message.channel.send(embed=embed)
      else:
        await message.channel.send("请确保赔率在0.01到9.99范围内，庄家必须押注300 gae以上。")
    else:
        await message.channel.send("开盘请使用!book [team1-id] [team2-id] [odd1] [odd2] [amount]")
  
  #close a list
  if message.content.startswith('!close'):
    lid=str(message.content).split()
    bm=str(message.author)
    #if bm==superusr: bm="gaebet"
    if len(lid) ==2 and lid[1] in db["book"].keys():
      data={"bm":bm, "bid":lid[1]}
      msg=bookmaker.close(data)
      await message.channel.send(msg)
    else:
      await message.channel.send("没有该记录！!open [book-ID]")
  
  #reopen a list
  if message.content.startswith('!open'):
    lid=str(message.content).split()
    bm=str(message.author)
    #if bm==superusr: bm="gaebet"
    if len(lid) ==2 and lid[1] in db["book"].keys():
      data={"bm":bm, "bid":lid[1]}
      msg=bookmaker.open(data)
      await message.channel.send(msg)
    else:
      await message.channel.send("没有该记录！!open [book-ID]")
  
  #result
  if message.content.startswith('!result'):
    lid=str(message.content).split()
    if len(lid) !=3:
      await message.channel.send("格式不对！结算请用!result [book-ID] [code]\n 结果编号[code]：1-左边赢；2-右边赢；3-平局/流局")
      return
    if not lid[2].isnumeric() and int(lid[2]) not in range(1,4):
      await message.channel.send("请使用结果编号：1-左边赢；2-右边赢；3-平局/流局")
      return
    if lid[1] not in db["book"].keys():
      await message.channel.send("没有该盘！")
      return
    
    bm=str(message.author)
    #if bm==superusr: bm="gaebet"
    if db["book"][lid[1]]["bm"]!=bm:
      await message.channel.send("只有庄家可以结算！")
    else:
      result_data={"bid":lid[1], "win":int(lid[2])}
      msg=bookmaker.result(result_data)
      await message.channel.send(msg)
  
  #odd
  if message.content.startswith('!odd'):
    lid=str(message.content).split()
    bm=str(message.author)
    if bm==superusr: bm="gaebet"
    if len(lid) !=4 and not lid[1].isnumeric() and not isnumber(lid[2]) and not isnumber(lid[3]):
      await message.channel.send("格式不对！修改赔率使用!odd [book-ID] [odd1] [odd2]")
    elif lid[1] not in db["book"].keys():
      await message.channel.send("没有该盘！请检查盘id（整数）。")
    elif 0.01>float(lid[2]) or float(lid[2])>9.99 or 0.01>float(lid[3]) or float(lid[3])>9.99:
      await message.channel.send("修改失败！赔率必须在0.01到9.99之间。")
    elif bm!=db["book"][lid[1]]["bm"]:
      await message.channel.send("修改失败！只有庄家可以修改赔率。")
    else:
      data={"bid":lid[1], "odd":[round(float(lid[2]),2),round(float(lid[3]),2)]}
      msg=bookmaker.odd(data)
      await message.channel.send(msg)
        
  #ghelp
  if message.content.startswith('!ghelp'):
    
    embed = discord.Embed(
      title='gaebet指令',
      color=discord.Color.blue())
    for k,v in COMMANDS.items():
      embed.add_field(name="`"+k+"` "+v["usage"].replace(k, ""), value=v["description"], inline=False)
    await message.channel.send(embed=embed)
  #fuck lulu
  if message.content.startswith('!fuck'):
    msg = " ".join(message.content.split(" ")[1:])
    if "lulu" in msg.lower():
      amt = int( ( random.random() - 0.49 ) * 20 )
      if db["user"][str(message.author)]["gae"]<=10:
        await message.channel.send("你实在太穷了，没嫖资fuck lulu！")
        return
      else:
        db["user"][str(message.author)]["gae"] += amt
        await message.channel.send(f"淦得漂亮，奖励你{amt}gae！")
    elif any([x in msg.lower() for x in ["dqq", "一力挺", "mike"]]):
      db["user"][str(message.author)]["gae"] -= 5
      await message.channel.send("哪个没素质得辱骂程序员？肯定是lulu。提示:输入`!fuck lulu`可得5gae！")
    else:
      await message.channel.send("没有说出关键词！")

wake()
client.run(os.environ['token'])