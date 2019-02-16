# Eric Garcia 
# Web Scraping Workshop
# 2/14/2019
import sys
import requests
from bs4 import BeautifulSoup

class Description:
	def __init__(self, fn):
		# Get the website and parse 
		page = requests.get('https://forecast.weather.gov/MapClick.php?lat=28.587960000000066&lon=-81.20731999999998#.XGYLiN1KhhE')
		soup = BeautifulSoup(page.content, 'html.parser')

		# List of all containers 
		self.seven_day = soup.find_all(class_='forecast-tombstone')
		self.fn = fn

		# For titles with multiple words, replace breaks with spaces 
		for br in soup.find_all("br"):
			br.replace_with(" ")
        
	def today(self):
		# Grab description
		desc = self.seven_day[0].find(class_='short-desc').getText()

		# Check for day or night 
		hightemp = self.seven_day[0].find(class_='temp temp-high')
		
		# If nightime 
		if(hightemp == None):
			low_temp = self.seven_day[0].find(class_='temp temp-low').getText()
            
			# Write info to output file
			self.fn.write('Tonight\n')
			self.fn.write(desc + '\n')
			self.fn.write(low_temp + '\n')
        
		# If daytime
		else:
			low_temp = self.seven_day[1].find(class_='temp temp-low').getText()

			# Write to output file
			self.fn.write('Today\n')
			self.fn.write(desc + '\n')
			self.fn.write(hightemp.getText() + '\n')
			self.fn.write(low_temp + '\n')

	def tomorrow(self):
		hightemp = self.seven_day[1].find(class_='temp temp-high')

		if hightemp == None:
			desc = self.seven_day[2].find(class_='short-desc').getText()
			hightemp = self.seven_day[2].find(class_='temp temp-high').getText()
			low_temp = self.seven_day[3].find(class_='temp temp-low').getText()

			self.fn.write('Tomorrow\n')
			self.fn.write(desc + '\n')
			self.fn.write(hightemp + '\n')
			self.fn.write(low_temp + '\n')
        
		else:
			desc = self.seven_day[1].find(class_='short-desc').getText()
			low_temp = self.seven_day[2].find(class_='temp temp-low').getText()

			self.fn.write('Tomorrow\n')
			self.fn.write(desc + '\n')
			self.fn.write(hightemp.getText() + '\n')
			self.fn.write(low_temp + '\n')

	def week(self):
		hightemp = self.seven_day[0].find(class_='temp temp-high')

		if hightemp == None:
			tonight_desc = self.seven_day[0].find(class_='short-desc').getText()
			low_temp = self.seven_day[0].find(class_='temp temp-low').getText()

			self.fn.write('Tonight\n')
			self.fn.write(tonight_desc + '\n')
			self.fn.write(low_temp + '\n\n')

			days = [1,3,5,7]
			for i in days:
				period = self.seven_day[i].find(class_='period-name').getText()
				desc = self.seven_day[i].find(class_='short-desc').getText()
				hightemp = self.seven_day[i].find(class_='temp temp-high').getText()
				low_temp = self.seven_day[i + 1].find(class_='temp temp-low').getText()

				self.fn.write(period + '\n')
				self.fn.write(desc + '\n')
				self.fn.write(hightemp + '\n')
				self.fn.write(low_temp + '\n\n')
		else:
			days = [0,2,4,6]
			for i in days:
				period = self.seven_day[i].find(class_='period-name').getText()
				desc = self.seven_day[i].find(class_='short-desc').getText()
				hightemp = self.seven_day[i].find(class_='temp temp-high').getText()
				low_temp = self.seven_day[i + 1].find(class_='temp temp-low').getText()

				self.fn.write(period + '\n')
				self.fn.write(desc + '\n')
				self.fn.write(hightemp + '\n')
				self.fn.write(low_temp + '\n\n')


def main():
	_string = sys.argv[1]
	fn = open('output.txt', 'w')
	weather = Description(fn)


	if _string == 'today':
		weather.today()
	elif _string == 'tomorrow':
		weather.tomorrow()
	elif _string == 'week':
		weather.week()
	else:
		fn.write('Invalid argument')

	fn.close()

if __name__ == '__main__':
	main()