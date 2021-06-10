COMMANDS = {
  "!new": {
    "description": "注册新账户",
    "usage": "!new"
  },
  "!gae": {
    "description": "显示账户余额；每天第一次使用该命令可以签到领取随机 50~150 gae的签到福利！",
    "usage": "!gae"
  },
  "!send": {
    "description": "转账到被@的人",
    "usage": "!send @user [amt] [unit]\t 单位默认为1 gae. 以下物品代表单位：bmw=50 gae; airplane=100 gae; rocket=500 gae, spaceship=1000 gae."
  },
  #!send @someone gae
  "!list": {
    "description": "显示可押注的盘口",
    "usage": "!list"
  },
   "!bets": {
    "description": "显示用户的现有押注记录",
    "usage": "!bets"
  },
  "!go": {
    "description": "押注[amount]的gae币给[Book-ID]盘上的[team-id]，可使用allin代替金额押注全部余额。\n=============================\n结算方法：赔率在0.01到9.99之间，\n买家每笔押注获胜所得=押注额x(1+下注时实时赔率)，失败输掉全部。\n庄家盈亏=盘总盈亏。每方可押注额度=庄家的活动押金/该方赔率",
    "usage": "!go [Book-ID] [team id] [amount]"
  },
  "!book": {
    "description": "开盘，庄家押[amount]的gae币",
    "usage": "!book [team1-id] [team2-id] [odd1] [odd2] [amount]"
  },
  "!odd": {
    "description": "庄家修改盘[Book-ID]的赔率",
    "usage": "!odd [Book-ID] [odd1] [odd2]"
  },
  "!close": {
    "description": "庄家暂停接受盘[Book-ID]的押注",
    "usage": "!close [Book-ID]"
  },
  "!open": {
    "description": "庄家重新接受盘[Book-ID]的押注",
    "usage": "!open [Book-ID]"
  },
  "!result": {
    "description": "庄家结算盘[Book-ID]。[code]可以用`1`（team1胜利）, `2`（team2胜利）, 或者`3`（平局/流局）",
    "usage": "!result [Book-ID] [code]"
  },
  "!top": {
    "description": "查看gae币排行榜的排名前[topn]的玩家",
    "usage": "!top [topn]"
  },
}
