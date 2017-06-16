#   This file is part of SnapFi.
#   Copyright 2017 Rafael Cauduro Oliveira Macedo
#
#   SnapFi is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   SnapFi is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with SnapFi. If not, see <http://www.gnu.org/licenses/>.

#Usage: python Retrieve_Metric.py <Output_File> <ID File> <Metric File>
#Retrieve an already computed metric using a file of IDs

import sys, os, numpy


def main(argv):
	
	#Get Inputs
	if(len(argv) < 3):
		print("Error! Retrieve_Metric.py requires at least 3 arguments: <Output_File> , <ID File> and <Metric File>")
		sys.exit(2)
	else:
		try:
			output_file = os.environ.get('TOOLHOME') + "/Results/" + argv[0]
			id_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[1] + ".txt"
			metric_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[2] + ".txt"
			
		except TypeError:
			print("TOOLHOME Environment not Set. Are you running Main.py?")
			sys.exit(2)

	#Variables
	ids = {}

	#Get IDs & Models Folder Locations
	try:
		content = open(id_file).readlines()
		
		for val in range(1, len(content)):
			if(content[val].strip() != ""):
				str_id = content[val].split()[0]			
				dict_val = ids.get(str_id)
				ids[str_id] = "null"
	except:
		print("Specified <ID_File> could not be located or is invalid")
		sys.exit(2)
		
	#Display Progress
	print("Extracting Metric...")
	
	#Extract Metric
	models_folder = ""
	try:
		content = open(metric_file).readlines()
		models_folder = content[0].strip()
		metric = []
				
		for val in range(1, len(content)):
			if(content[val].strip() != ""):
				str_id = content[val].split()[0]
				dict_val = ids.get(str_id)
				if(dict_val != None):
					ids[str_id] = content[val].split()[1]

	except:
		print("Specified <Metric_File> could not be located or is invalid")
		sys.exit(2)
	
	
	#Delete Previous Runs & Write Header
	out_file = open(output_file, 'w+')
	out_file.write(models_folder + "\n")
	
	#Sort & Write Ids
	for key, value in ids.items():
		out_file.write(key + "\t" + value + "\n")
	
	#Finally...
	out_file.close()
	

#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])
