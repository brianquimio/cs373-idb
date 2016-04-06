from parks import *
#from cs373-idb.app.Secrets import *

def extractor():
	park = Parks("8ht7msbmzmvdv6xatyw6twu9")
	state_list = ["AL"]
#state_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
	for x in state_list:
		parkdata = park.get_state_parks(x)
		print("{\n\t\"stateid\": \"" + x +"\",\n \t\t\"campgrounds\":\n\t\t[")
		i = 0
		for y in parkdata:
			if(i % 2 == 0):
				print("\t\t\t{site:" + y + ",")
			else:
				print("\t\t\t photo" + y +"},")
			i += 1
		print("],\n}")
	#time.sleep(30)

if __name__ == "__main__":
	extractor()