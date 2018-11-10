import requests
import pandas as pd

URL = 'https://www.bbc.com/sport/football/spanish-la-liga/table'



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
	last_updated = df.iat[20,0]
	
	df = df.drop([20])
	df = df.dropna()	#Removes blank (NaN) values
	df = df.rename(columns = {'Unnamed: 0' : 'Position', 'Unnamed: 1' : 'Change'})
	df = clean_position_change(df)
	return df

def clean_position_change(df):
	#Replaces position change text with symbols for cleaner look.
	for column in range(0,20):
		if df.iat[column,1] == "team hasn't moved":
			df.iat[column,1] = 'x'
		elif df.iat[column,1] == "team has moved up":
			df.iat[column,1] = '+' 
		elif df.iat[column,1] == "team has moved down":
			df.iat[column,1] = '-'
	return df

def main():
	set_dataframe_options()
	
	req = requests.get(URL).text
	pd_html = pd.read_html(req)[0]
	df = pd.DataFrame(pd_html)	#Converts html table to pandas dataframe
	df = clean_table(df)

	print(df)
	print(last_updated)
main()
