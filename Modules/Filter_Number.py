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

#Usage: python Filter_Number.py <Output_File> <Number of Values Retrieved> <Metric File> <OptionaL: Reversed=True/False> (Default False)
#Sort a Metric File and retrieve a fixed number of entries

import sys, os, numpy

def main(argv):
	
	#Get Inputs
	if(len(argv) < 3):
		print("Error! Filter_Number.py requires at least 3 arguments: <Output_File> , <Number of Values Retrieved> , <Metric File> and <Optional: Reversed=True/False> (Default: False)")
		sys.exit(2)
	else:
		try:
			total_retrived = int(argv[1])
		except:
			print("Parameter <Number of Values Retrieved> is invalid")
			sys.exit(2)
			
		revert = False
		if(len(argv) == 4):
			if(argv[3].upper() == "REVERSED=TRUE"):
				print("Reversed = True")
				revert = True
			

	#Get the Results File Name
	try:
		input_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[2] + ".txt"
		output_file = os.environ.get('TOOLHOME') + "/Results/" + argv[0]
		
	except TypeError:
		print("TOOLHOME Environment not Set. Are you running Main.py?")
		sys.exit(2)

	#Get IDs & Models Folder Locations
	try:
		temp = open(input_file).read().split()
		models_folder = temp[0]
		temp = temp[1:]
	
		#Fix Ids
		ids = []
		for val in range(0, len(temp), 2):
			ids.append((temp[val+1], temp[val]))
		ids.sort(reverse=revert)
	
	except:
		print("Specified <IDs_File> could not be located or is invalid")
		sys.exit(2)
	
	#Display Progress
	print("Applying Filter on \"" + "Step_" + argv[2] + ".txt\"")
	
	#Delete Previous Runs & Write Header
	out_file = open(output_file, 'w+')
	out_file.write(models_folder + "\n")
	
	#Write Results
	total_retrived = min(len(ids), total_retrived)
	for pos in range(0, total_retrived):
		out_file.write(str(ids[pos][1]) + "\t" + str(ids[pos][0]) + "\n")
	
	#Finally...
	out_file.close()
	

#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])
