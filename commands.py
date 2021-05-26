COMMANDS = {
  "!new": {
    "description": "注册新账户",
    "usage": "!new"
  },
  "!gae": {
    "description": "显示账户余额",
    "usage": "!gae"
  },
  "!list": {
    "description": "显示可押注的盘口",
    "usage": "!list"
  },
  "!go": {
    "description": "押注[amount]的gae币给[bet-ID]盘上的[team-id]\n=============================\n结算方法：赔率在0.01到9.99之间，\n买家每笔押注获胜所得=押注额x(1+下注时实时赔率)，失败输掉全部。\n庄家盈亏=盘总盈亏。每方可押注额度=庄家的活动押金/该方赔率",
    "usage": "!go [bet-ID] [team id] [amount]"
  },
  "!book": {
    "description": "开盘，庄家押[amount]的gae币",
    "usage": "!book [team1-id] [team2-id] [rate1] [rate2] [amount]"
  },
  "!rate": {
    "description": "庄家修改盘[bet-ID]的赔率",
    "usage": "!rate [bet-ID] [rate1] [rate2]"
  },
  "!!close": {
    "description": "庄家暂停接受盘[bet-ID]的押注",
    "usage": "!close [bet-ID]"
  },
  "!open": {
    "description": "庄家重新接受盘[bet-ID]的押注",
    "usage": "!open [bet-ID]"
  },
  "!result": {
    "description": "庄家结算盘[bet-ID]。[code]可以用`1`（team1胜利）, `2`（team2胜利）, 或者`3`（平局/流局）",
    "usage": "!result [bet-ID] [code]"
  },
  "!top": {
    "description": "查看gae币排行榜的排名前[topn]的玩家",
    "usage": "!top [topn]"
  },
}
