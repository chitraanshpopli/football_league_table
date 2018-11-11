#global URLs

#Fetches and displays La Liga table from https://www.bbc.com

import requests
import pandas as pd

league_numbers = {
1 : 'LaLiga',
2 : 'EPL',
3 : 'Bundesliga',
4 : 'SerieA',
5 : 'Ligue1'
}

URLs = {
'LaLiga' : 'https://www.bbc.com/sport/football/spanish-la-liga/table',
'EPL' : 'https://www.bbc.com/sport/football/premier-league/table',
'Bundesliga' : 'https://www.bbc.com/sport/football/german-bundesliga/table',
'SerieA' : 'https://www.bbc.com/sport/football/italian-serie-a/table',
'Ligue1' : 'https://www.bbc.com/sport/football/french-ligue-one/table'
}
def set_number_of_teams(league_URL):
	global rows
	rows = 20	#Defines the total number of rows.
	if league_URL == URLs['Bundesliga']:	
		rows -= 2	#Bundesliga has 18 teams. Other leagues have 20.
	
def get_URL():
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

def main():
	set_dataframe_options()
	
	league_URL = get_URL()
	req = requests.get(league_URL).text
	pd_html = pd.read_html(req)[0]
	
	df = pd.DataFrame(pd_html)	#Converts html table to pandas dataframe
	df = clean_table(df)

	print(df)
	print(last_updated)
	qv = input('Press enter to exit.')
main()

