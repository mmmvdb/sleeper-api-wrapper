import sleeper_wrapper
import os
from datetime import date
import json

class Players(sleeper_wrapper.BaseApi):
	def __init__(self):
		pass

	def get_all_players(self, force=False):
		# To limit API calls to once a day (as requested by API docs) we'll try and save data
		# and check for existance and "freshness" before calling API
		
		# Needed os.path.join to keep platform agnostic
		# needed API.__FILE__ to make this the api.py location, so that if multiple uses in diff projects, we still limit by day
		data_dir  = os.path.join(os.path.dirname(sleeper_wrapper.__file__), 'sleeper_data')
		data_file = 'sleeper_players.json'
		
		# Needed os.path.join to keep platform agnostic
		data_full_path = os.path.join(data_dir, data_file)

		if not os.path.isdir(data_dir):
			os.mkdir(data_dir)

		if os.path.isfile(data_full_path) and not force:
			# The file exists, we can read from it and check "freshness"
			with open(data_full_path, 'r') as file:
				data = json.loads(file.read())
			
			# Yank out the date, parse the string, then turn them into ints so we can run date on them.
			date_split = list(map(int, data["date"].split('-')))
			
			# date(year, month, day)
			file_date = date(date_split[2], date_split[1], date_split[0])
			
			if file_date == date.today():
				# Just return up the json dictionary.  No freshness stuff.
				return data["sleeper_data"]
		
		# Now... We've either exited with file data, or got here.  If we got here, the file doesn't exist
		# or it is out of date.  Or we are forcing.  So we can fetch and store.
		data = self._call("https://api.sleeper.app/v1/players/nfl")
		
		# Trying to make the json... more json like with a date more like you'd see in the wild.
		# That'll give us more work above unpacking it.  But makes the json file more... nice if someone
		# needs it externally.
		data_file_content = { "date"        : date.today().strftime('%d-%m-%Y')
							, "sleeper_data": data
							}
		
		with open(data_full_path, 'w') as file:
			file.write(json.dumps(data_file_content))
	
		return data

	def get_trending_players(self,sport, add_drop, hours=24, limit=25 ):
		return self._call("https://api.sleeper.app/v1/players/{}/trending/{}?lookback_hours={}&limit={}".format(sport, add_drop, hours, limit))