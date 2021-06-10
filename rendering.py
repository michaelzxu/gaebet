#import seaborn as sns

def plot_odds(odds1, odds2):
  return sns.barplot(x=[1,2], y=[2,3]).get_figure()

def render_bet(bet):
  return "formatted_text", "image"