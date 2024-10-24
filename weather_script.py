import requests	
import math
import time
from pprint import pprint
import geocoder 


# function to find your current gps coordinates using your current IP address location
def get_current_gps_coordinates():
	
    	g = geocoder.ip("me")
    		#g.latlng tells if the coordiates are found or not
    	if g.latlng is not None: 
  			# create location dictionary and add latitude,longitude and city for easier access
    		location={}
    		location["latitude"]= g.lat
    		location["longitude"]=g.lng
    		location["city"]=g.city
    		# print("dictionary:",location)
    		return location
    	else:
    		return None
    

# function to retrive weather data from API endpoint 
# return the data as json if the status code 200 which is success otherwise return None
def Get_weather_Data(url):
	try:
		res = requests.get(url,timeout=10)
		# return response if the status is OK
		if res.status_code==200:
			# print(res.json())
			return res.json()
		else:
			print("failed to fetch data:",res.status_code)

			return None
	except requests.exceptions.ConnectionError as err:
		print("Please check if your PC has internet connection!!")
		# print(f" connection failed:{err}")
	

# function to calculate heat index based on the formula from 
# https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
def calculate_Heat_Index(temperature,humidity):
	# assign temperature and humidity to local variables
	T=temperature
	RH=humidity

	# calculate with simple formula 
	# In practice, the simple formula is computed first and the result averaged with the temperature.
	# If this heat index value is 80 degrees F or higher, 
	# the full regression equation along with any adjustment as described above is applied. 
	# calculate heat index using simple formula 
	HI = 0.5 * (T + 61.0 + ((T-68.0)*1.2) + (RH*0.094))
	# Average Heat Index with temperature 
	Temp_HI_average = (HI+T)/2
	# print(f"Temperature and Calculated Heat Index Average: {Temp_HI_average:.2f}°F")
	# check if result averaged with the temperature is equal 80 or greater than 80
	if Temp_HI_average>=80:
		# print("hit me!!")
		if (T>80 and T<112) and RH<13:
			# The regression equation of Rothfusz is 
			# print("(Temperature>80 and Temperature<112) and Relative Humidity<13")
			HI = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
			# If the RH is less than 13% and the temperature is between 80 and 112 degrees F, 
			# then the following adjustment is subtracted from HI: 
			# ADJUSTMENT_ONE = [(13-RH)/4]*SQRT{[17-ABS(T-95.)]/17} 
			ADJUSTMENT_ONE = ((13-RH)/4)* math.sqrt(17-abs(T-95.)/17)
			HI = HI - ADJUSTMENT_ONE
			

		elif(T>80 and T<87) and RH>85:
			# The regression equation of Rothfusz is 
			# print("(Temperature>80 and Temperature<87) and Relative Humidity>85")
			HI = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
			# On the other hand, if the RH is greater than 85% and the temperature is between 80 and 87 degrees F, 
			# then the following adjustment is added to HI: 
			# ADJUSTMENT_TWO = [(RH-85)/10] * [(87-T)/5]
			ADJUSTMENT_TWO = ((RH-85)/10) * ((87-T)/5)
			HI = HI + ADJUSTMENT_TWO
		else:
			# print(f"Temperature is equal to 80°F")
			HI = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
		
		return HI
	else:
		# The Rothfusz regression is not appropriate when conditions of temperature and humidity 
		# warrant a heat index value below about 80 degrees F. 
		# In those cases, a simpler formula is applied to calculate values consistent with Steadman's results: 
		# The Rothfusz regression is not appropriate when conditions of temperature and humidity 
		# warrant a heat index value below about 80 degrees F. 
		# In those cases, a simpler formula is applied to calculate values consistent with Steadman's results: 
		# print(f"Temperature is less than 80°F")
		HI = 0.5 * (T + 61.0 + ((T-68.0)*1.2) + (RH*0.094))
		return HI
	


# function to print out the result
# this script retrieve weather data from http://api.openweathermap.org
# API documentation  is here https://openweathermap.org/api/one-call-3
# Steps:
# 1. Signup  2. create an API KEY      
# 3. APIKEY= ee4dc890d8502f3bd43b7dc69q={}&appid={}&units=metricd23ba6d
# 4. Concatenate API KEY in the URL http://api.openweathermap.org/data/2.5/weather?q={}&{APIKEY HERE }&units=metric

def LetStart(location):
	# print location dictionary to the screen
	print(" your current location: ", location)
    #  API KEY 
	APIKEY='ee4dc890d8502f3bd43b7dc69d23ba6d'
	# If retrieve weather data using city name then using this one
	# set parameters variables such as q={} & appid={} & units=metric to the API end point
	# Base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
	# units=imperial to get temperature in Farenheit unit
	# format city name and API KEY as the values of  q and appid parameters in the url
	# url = Base_url.format(location['city'],APIKEY)

	# Retrieve weather data using latitude and longitude coordinates
	Base_url = 'https://api.openweathermap.org/data/2.5/weather'
	print("API endpoint: ",Base_url)
	# append lat,lang, appid and units parameters variable to the API url
	Base_url = Base_url+'?lat={}&lon={}&appid={}&units=imperial'
	# check if the location return values is not None
	if location is not None:
		# format latitude, longitude and API KEY as the values of lat, lon and appid parameters in the url
		url= Base_url.format(location['latitude'],location['longitude'],APIKEY)
		data = Get_weather_Data(url)
		# print(data)
		if data:
		#extracting temperature and humidity
			try:
				temperature = data['main']['temp']
				humidity = data['main']['humidity']
				print(f"Temperature: {temperature}°F")
				print(f"Humidity: {humidity}%")
            	# call function to calculate heat index by passing temperature and humidity as parameters
				heat_index =calculate_Heat_Index(temperature,humidity)
				print(f"Heat Index: {heat_index:.2f}°F")
			except KeyError as e:
				print(f"KeyError: {e}")

# main program start here
# script start here
if __name__ == "__main__":
	#time variable in seconds	
	# set timer to 10 minutes in seconds is 600
	timer=600
	# infinite loop 
	while(True):
		print("-------------------------------------------------------------------------------------")
		print(f"---This script is printed to screnn every: {int(timer/60)} minutes")
		print(" ---This script using your current IP to get your current location---")
		print(" ---Then retrieve temperature and relative humidity from api.openweathermap.org---")
		print(" ---Then calculate Heat Index---")
		#Get current
		location = get_current_gps_coordinates()
		# start fetch weather API data and calculate heat index
		LetStart(location)
		# pause the execution of the program for 10 minutes
		print("Start : %s" % time.ctime())
		print("-------------------------------------------------------------------------------------")
		time.sleep(timer)
		print("End : %s" % time.ctime())


