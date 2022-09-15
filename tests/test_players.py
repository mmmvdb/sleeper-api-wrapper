import sleeper_wrapper
import os
from datetime import date
import json

def test_get_trending_players(capsys):
	players = sleeper_wrapper.Players()
	added = players.get_trending_players("nfl","add", 1, 4)

	dropped = players.get_trending_players("nfl","drop")

	# with capsys.disabled():
	# 	print(added)
	# 	print(dropped)

def test_get_all_players(capsys):
	### TEST SETUP
	
	# Test cleanup.  We want to test directory and file not being there, so we need to set all
	# that up.
	data_dir  = os.path.join(os.path.dirname(sleeper_wrapper.__file__), 'sleeper_data')
	data_file = 'sleeper_players.json'
	data_full_path = os.path.join(data_dir, data_file)
	
	# Delete the sleeper_players file
	if os.path.isfile(data_full_path):
		os.remove(data_full_path)
		
	# Hopefully, nothing else in that dir.  Try and remove it.
	if os.path.isdir(data_dir):
		os.rmdir(data_dir)
	
	# Testing that I did that right.
	assert os.path.isdir(data_dir) == False
	assert os.path.isfile(data_full_path) == False
	
	
	players = sleeper_wrapper.Players()
	
	### REAL TESTING
	
	### TEST 1
	# Test that after a call, we have player data, and it is stored in a file where we expect.
	data = players.get_all_players()
	
	assert isinstance(data, dict)
	
	assert os.path.isdir(data_dir) == True
	assert os.path.isfile(data_full_path) == True
	
	# Checking the freshness date.
	with open(data_full_path, 'r') as file:
		raw_data = json.loads(file.read())
		
	assert isinstance(raw_data["date"], str)
	
	# Yank out the date, parse the string, then turn them into ints so we can run date on them.
	date_split = list(map(int, raw_data["date"].split('-')))
	file_date = date(date_split[2], date_split[1], date_split[0])
	
	assert file_date == date.today()
	
	### TEST 2
	# Test that if we have old data, we pull fresh data.
	
	# First we have to force old data.  We'll just force the freshness date into the past
	# If I decrement year, I'm sure I won't roll over a month or year boundary, like if I'd decrement months or days.
	old_file_date = date(date_split[2] - 1, date_split[1], date_split[0])
	
	assert isinstance(old_file_date , date)
	
	data_file_content = { "date"        : old_file_date.strftime('%d-%m-%Y')
						, "sleeper_data": data
						}
	
	with open(data_full_path, 'w') as file:
		file.write(json.dumps(data_file_content))
		
	# Being extra here, let's make sure the test file got the update.
	with open(data_full_path, 'r') as file:
		old_raw_data = json.loads(file.read())
	
	date_split = list(map(int, old_raw_data["date"].split('-')))
	file_date = date(date_split[2], date_split[1], date_split[0])
	
	# Just not being equal is good enough
	assert file_date != date.today()
	
	# Now we are set... if we run get all players again, it should hit the API and redo the file
	data = players.get_all_players()
	
	assert isinstance(data, dict)
	
	with open(data_full_path, 'r') as file:
		raw_data = json.loads(file.read())
		
	assert isinstance(raw_data["date"], str)
	
	date_split = list(map(int, raw_data["date"].split('-')))
	file_date = date(date_split[2], date_split[1], date_split[0])
	
	assert file_date == date.today()
	
	### TEST 3
	# Really we should test that if we have fresh data in the file, we use it instead of an API call.
	# I have no idea how I'd know where the data came from at this level though.