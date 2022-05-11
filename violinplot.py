import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import seaborn as sns
def plot_probe(probe_results,probe):
	plt.ioff()
	plt.tight_layout()
	df=pd.DataFrame(data={"Sample type":["Normal"]*len(probe_results[probe][2])+["ccRCC"]*len(probe_results[probe][3]),"log2(Expression)":probe_results[probe][2]+probe_results[probe][3]})
	sns.set(font_scale = 0.7)
	sns.set_style({'axes.edgecolor': 'white','axes.labelcolor': 'white','text.color': 'white','axes.facecolor': '#000d1a','figure.facecolor': '#000d1a','xtick.color': 'white','ytick.color':'white'})
	sns.set_palette("Paired")
	fig=plt.figure(figsize=(5,5))
	sns.violinplot(x="Sample type",y="log2(Expression)",data=df)
	figure=fig.get_figure()
	figure.savefig(f"plots/{probe}.png")
	return None