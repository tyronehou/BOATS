# --- json_formatter.py ---
# This file runs by reading the csv files only in the same directory and returns the json object 
# load_csv: 
#			inputs - none
#			outputs - json of the same schema 

import json

def load_csv():

	#json object
	json_data = {}

	with open('students.csv','r') as f: 

		schema = []

		for line_num, line in enumerate(f):

			#remove unicode byte order character, newline and double quotes characters
			line = line.replace(u'\ufeff', '').replace(u'\n', '').replace(u'\"', '').split('\t') 

			if line_num == 0:
				#record schema for dataset
				schema = line
				
			else:
				
				#each zip code missing leading 0
				line[2] = '0' + line[2]

				#convert neighborhood safety score to int
				line[12] = int(line[12])

				#convert max walk distance to float
				line[13] = float(line[13])

				#convert coordinates to floats
				line[4] = float(line[4])
				line[5] = float(line[5])
				line[-1] = float(line[-1])
				line[-2] = float(line[-2])

				#add data to students_data
				datapoint = {}

				for i in range(len(schema)):
					s = schema[i]
					l = line[i]
					datapoint[s] = l

				#key = line number, val = datapoint
				json_data[str(line_num)] = datapoint

	with open('students.json','w') as f:
		json.dump(json_data, f, indent=4)

	#json object
	json_data = {}

	with open('schools.csv','r') as f: 

		schema = []

		for line_num, line in enumerate(f):

			#remove unicode byte order character, newline, double quotes and tab characters
			line = line.replace(u'\ufeff', '').replace(u'\n', '').replace(u'\"', '').replace(u'\t', '').split(',') 

			if line_num == 0:
				#record schema for dataset
				schema = line

			else:

				#append address to zip code
				line[3] = line[3] + ','+ line[4]
				del line[4]

				#convert coordinates to floats
				line[-1] = float(line[-1])
				line[-2] = float(line[-2])

				#add data to school_data
				datapoint = {}

				for i in range(len(schema)):
					s = schema[i]
					l = line[i]
					datapoint[s] = l

				#key = line number, val = datapoint
				json_data[str(line_num)] = datapoint

	with open('schools.json','w') as f:
		json.dump(json_data, f, indent=4)

	# json object
	json_data = {}

	with open('bus_yards.csv','r') as f: 

		schema = []

		for line_num, line in enumerate(f):

			#remove unicode byte order character, newline and double quotes characters
			line = line.replace(u'\ufeff', '').replace(u'\n', '').replace(u'\"', '').split('\t') 

			#drop empty spaces
			line = [i for i in line if i != '']

			if line_num == 0:
				#record schema for dataset
				schema = line

				#rename coordinates
				schema[-2] = 'Latitude'
				schema[-1] = 'Longitude' 

			else:

				#combine addresses
				line[3] = line[3] + line[4] + line[5] + ',' + line[6]
				del line[4]
				del line[4]
				del line[4]

				#convert coordinates to floats
				line[-1] = float(line[-1])
				line[-2] = float(line[-2])

				#add data to school_data
				datapoint = {}

				for i in range(len(schema)):
					s = schema[i]
					l = line[i]
					datapoint[s] = l

				#key = line number, val = datapoint
				json_data[str(line_num)] = datapoint

	with open('bus_yards.json','w') as f:
		json.dump(json_data, f, indent=4)
				
if __name__ == '__main__':
	load_csv()
