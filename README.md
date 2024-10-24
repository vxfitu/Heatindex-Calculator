

What this program does:
1. This program runs infinitely 
2. For every 10 minutes it will retrieve your current location(latitude and longitude), then retrieve weather data from openweathermap API: http://api.openweathermap.org
4. Extract temperature and relative humidity data from the retrived dataset then calculate heat index based on this formula https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
5. Then print out the temperature, humidity and calculated heat index to the screen and repeat the cycle every 10 minutes.

How to execute the script:
1. Make sure you hava python and pip installed
2. Install following python modules using pip: requests, math, time, pprint and geocoder if they have not installed
3. Pull/download this script to your computer 
4. Open CMD/terminal  and change the directory to the directory where this script located.
5. Type --> python3/python weather_script.py  then press "enter" to start the script.
6. It will run in the terminal or CMD and update every 10 minutes.

NOTES: Since the script using geocoder(user's IP) to retrieve current location and openweathermap API: http://api.openweathermap.org to retrieve weather information, therefore internet is required to get those data.

  
