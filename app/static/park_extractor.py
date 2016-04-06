import requests, xmltodict, datetime, parks.py

def extractor():
	state_list = ["AL"]
#state_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
	for x in state_list:
		parkdata = parks.get_state_parks(x)
		print("{\n\t\"stateid\": \"" + x +"\",\n \"campgrounds\":\n[")
		i = 0
		for y in parkdata:
			if(i % 2 == 0):
				print("{site:" + y + ",")
			else:
				print(" photo" + y +"},")
			i += 1
		print("],\n}")
	#time.sleep(30)