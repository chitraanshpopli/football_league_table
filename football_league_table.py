"""Fetches and displays table of 5 major European football leagues from https://www.bbc.com."""

import sys
import requests
import pandas as pd
import ftg_graphing as ftgg

league_numbers = {
1 : 'LaLiga',
2 : 'EPL',
3 : 'Bundesliga',
4 : 'SerieA',
5 : 'Ligue1',
}

URLs = {
'LaLiga' : 'https://www.bbc.com/sport/football/spanish-la-liga/table',
'EPL' : 'https://www.bbc.com/sport/football/premier-league/table',
'Bundesliga' : 'https://www.bbc.com/sport/football/german-bundesliga/table',
'SerieA' : 'https://www.bbc.com/sport/football/italian-serie-a/table',
'Ligue1' : 'https://www.bbc.com/sport/football/french-ligue-one/table',
}

graph_choices = {
'1' : 'Won',
'2' : 'Draw',
'3' : 'Lost',
'4' : 'Goals For',
'5' : 'Goals Against',
'6' : 'Goal Difference',
'7' : 'Points',
'13' : ('Won', 'Lost'),
'45' : ('Goals For', 'Goals Against'),
'123' : ('Won', 'Draw', 'Lost'),
'457' : ('Goals For', 'Goals Against', 'Points'),
}

column_headings = {
'Won' : 'W',
'Draw' : 'D',
'Lost' : 'L',
'Goal For' : 'F' ,
'Goals Against' : 'A',
'Goals Difference' : 'GD',
'Points' : 'Pts',
('Won', 'Lost') : ('W', 'L'),
('Goals For', 'Goals Against') : ('F', 'A'),
('Won', 'Draw', 'Lost') : ('W', 'D', 'L'),
('Goals For', 'Goals Against', 'Points') : ('F', 'A', 'Pts'),
}



def set_number_of_teams(league_URL):
	global rows
	rows = 20	#Defines the total number of rows.
	if league_URL == URLs['Bundesliga']:	
		rows -= 2	#Bundesliga has 18 teams. Other leagues have 20.
	
def get_URL():
	#Retrieves and returns URL of the required league.
	#URL can be retrieved either via command line argument or
	#by entering the serial number of league.
	
	if len(sys.argv) == 2:
		try:
			league_URL = URLs[sys.argv[1]]
			set_number_of_teams(league_URL)
			print('Loading table for ' + sys.argv[1])
			return league_URL
		except KeyError:
			print('No such league found.')
	
	for number, name in league_numbers.items():
		print(str(number) + '. ' + name)
	no_league = True
	while no_league:
		try:
			league_number = int(input('Enter the serial number of league you want to see: '))
		except ValueError:
			print('\nWrong input.\n')
			continue

		try:
			print('\nLoading table for ' + league_numbers[league_number])
			no_league = False
		except KeyError:
			print('\nWrong input.\n')
			continue
	set_number_of_teams(URLs[league_numbers[league_number]])
	return URLs[league_numbers[league_number]]

def set_dataframe_options():
	#Options for dataframe display.
	pd.set_option('display.max_rows', 50)
	pd.set_option('display.max_columns', 50)
	pd.set_option('display.width', 1000)

def clean_table(df):
	#Returns a better formatted and readable dataframe.
	#Also sets last_updated time.
	df = df.drop(columns = ['Form'],axis = 1)
	
	#Replaces NaN with ''. 
	#For some reason, this also converts numeric values from decimal to non-decimal.
	df = df.fillna('')
	
	global last_updated
	last_updated = df.iat[rows,0]
	
	df = df.drop([rows])
	df = df.dropna()	#Removes blank (NaN) values
	df = df.rename(columns = {'Unnamed: 0' : 'Position', 'Unnamed: 1' : 'Change'})
	df = clean_position_change(df)
	return df

def clean_position_change(df):
	#Replaces position change text with symbols for cleaner look.
	for column in range(rows):
		if df.iat[column,1] == "team hasn't moved":
			df.iat[column,1] = 'x'
		elif df.iat[column,1] == "team has moved up":
			df.iat[column,1] = '+' 
		elif df.iat[column,1] == "team has moved down":
			df.iat[column,1] = '-'
	return df
	
def plot_graph(df):
	for num, choice in graph_choices.items():
			print(num, '  ', choice)

	graph_choice = input('Choose graph:\t')
	if graph_choice not in graph_choices:
		print('Invalid input.')
	else:
		my_plot = ftgg.Graph(df)
		column_heading = column_headings[graph_choices[graph_choice]]
		graph_label = graph_choices[graph_choice]
		
		if int(graph_choice) < 8:
			my_plot.plot_onebar(column_heading, graph_label)
		elif int(graph_choice) > 100:
			my_plot.plot_threebar(column_heading, graph_label)
		else:
			my_plot.plot_twobar(column_heading, graph_label)

def main():
	set_dataframe_options()
	
	league_URL = get_URL()
	req = requests.get(league_URL).text
	pd_html = pd.read_html(req)[0]
	
	df = pd.DataFrame(pd_html)	#Converts html table to pandas dataframe
	df = clean_table(df)

	print(df)
	print(last_updated)
	
	graph = input("Enter 'y' to plot graph: ")
	if graph.lower() == 'y':
		plot_graph(df)

	qv = input('Press enter to exit.')
main()

