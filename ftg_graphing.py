"""Class to plot graph for different columns of league table.""" 

import matplotlib.pyplot as plt
import numpy as np

class Graph():
	def __init__(self, df):
		#Initialize variables and set graph properties.
		
		#Positions for xticks
		self.positions =  np.arange(len(df.loc[:,'Team']))	
		
		#Names for xticks
		self.teams = df.loc[:,'Team']
		
		self.df = df
		plt.xticks(self.positions , self.teams, rotation = -45)
	
	#fa0000 - shade of red
	#ffae00 - shade of yellow/orange
	#09b800 - shade of green
	def plot_onebar(self, column_heading, graph_label):
		plt.bar(
		self.positions, self.df.loc[:,column_heading], 
		color = '#09b800', label = graph_label)
		plt.legend()
		plt.show()

	def plot_twobar(self, column_heading, graph_label):
		plt.bar(
		self.positions-0.2, self.df.loc[:,column_heading[0]], 
		color = '#fa0000', width = 0.4, label = graph_label[0])
		plt.bar(
		self.positions+0.2, self.df.loc[:,column_heading[1]], 
		color = '#09b800', width = 0.4, label = graph_label[1])		
		plt.legend()
		plt.show()
		
	def plot_threebar(self, column_heading, graph_label):
		plt.bar(
		self.positions-0.3, self.df.loc[:,column_heading[0]], 
		color = '#fa0000', width = 0.3, label = graph_label[0])
		plt.bar(
		self.positions, self.df.loc[:,column_heading[1]], 
		color = '#ffae00', width = 0.3, label = graph_label[1])
		plt.bar(
		self.positions+0.3, self.df.loc[:,column_heading[2]], 
		color = '#09b800', width = 0.3, label = graph_label[2])		
		plt.legend()
		plt.show()
