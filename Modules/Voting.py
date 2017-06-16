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

#Usage: python Voting.py <Output_File> <Votes Required> <Metric Files [2+]>
#Retrieve an ensemble of IDs using common IDs from several Metrics Files

import sys, os, numpy


def main(argv):
	
	#Get Inputs
	if(len(argv) < 4):
		print("Error! Voting.py requires at least 4 arguments: <Output_File> , <Votes Required> and <Metric Files [2+]>")
		sys.exit(2)
	else:
		
		try:
			votes_required = int(argv[1])
			if(votes_required <= 0):
				raise
		except:
			print("Parameter <Votes Required> is invalid")
			sys.exit(2)
		
		metric_files = argv[2:]

	#Get the Results File Name
	try:
		output_file = os.environ.get('TOOLHOME') + "/Results/" + argv[0]
		
	except TypeError:
		print("TOOLHOME Environment not Set. Are you running Main.py?")
		sys.exit(2)

	#Get IDs & Models Folder Locations
	ids = {}
	models_folders = []
	for pos in range(0, len(metric_files)):
		
		input_file = os.environ.get('TOOLHOME') + "/Results/Step_" + metric_files[pos] + ".txt"
		content = open(input_file).readlines()
		models_folders.append(content[0])
		
		for val in range(1, len(content)):
			if(content[val].strip() != ""):
				str_id = content[val].split()[0]			
				dict_val = ids.get(str_id)
				if(dict_val == None):
					ids[str_id] = 1
				else:
					ids[str_id] = dict_val + 1
		
				
	#Display Progress
	print("Computing Votes...")
	
	#Compute Votes
	final_ids = []
	for key, value in ids.items():
			
		if(value >= votes_required):
			final_ids.append(int(key))

	#Delete Previous Runs & Write Header
	out_file = open(output_file, 'w+')
	out_file.write(models_folders[0] + "\n")
	
	#Sort & Write Ids
	final_ids.sort()
	for entry in final_ids:
		out_file.write(str(entry) + "\n")
	
	#Finally...
	out_file.close()
	

#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])
