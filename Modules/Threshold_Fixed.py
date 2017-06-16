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

#Usage: python Threshold_Fixed.py <Output_File> <Threshold> <Metric File> <Comparison Type [LT|LE|GT|GE]>
#Apply a fixed threshold on a Metric File, eliminating unsatisfactory structures.

import sys, os, numpy


def main(argv):
	
	#Get Inputs
	if(len(argv) < 4):
		print("Error! Threshold_Fixed.py requires at least 4 arguments: <Output_File> , <Threshold> , <Metric File> and <Comparison Type>")
		print("Comparison Types: LT = Less Than | LE = Less Than or Equal | GT = Greater Than | GE = Greater Than or Equal")
		sys.exit(2)
	else:
		
		try:
			threshold = float(argv[1])
		except:
			print("Parameter <Threshold> is invalid")
			sys.exit(2)
			
		comparison_type = argv[3].upper()
		if(not(comparison_type == "LE" or comparison_type == "LT" or comparison_type == "GT" or comparison_type == "GE")):
			print("Comparison Type not Recognized. Aborting")
			sys.exit(2)

	#Get the Results File Name
	try:
		input_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[2] + ".txt"
		output_file = os.environ.get('TOOLHOME') + "/Results/" + argv[0]
	
	except TypeError:
		print("TOOLHOME Environment not Set. Are you running Main.py?")
		sys.exit(2)

	try:
		#Get IDs & Models Folder Locations
		temp = open(input_file).read().split()
		models_folder = temp[0]
		temp = temp[1:]
		
		#Fix Ids
		ids = []
		for val in range(0, len(temp), 2):
			ids.append((temp[val+1], temp[val]))
	
	except:
		print("Specified <IDs_File> could not be located or is invalid")
		sys.exit(2)

	#Display Progress
	print("Applying Threshold on \"" + "Step_" + argv[2] + ".txt\"")
	
	#Delete Previous Runs & Write Header
	out_file = open(output_file, 'w+')
	out_file.write(models_folder + "\n")
	
	#Apply Threshold & Write Results
	for val in ids:
			
		if(comparison_type == "LT" and float(val[0]) < threshold):
			out_file.write(str(val[1]) + "\t" + str(val[0]) + "\n")
		elif(comparison_type == "LE" and float(val[0]) <= threshold):
			out_file.write(str(val[1]) + "\t" + str(val[0]) + "\n")
		elif(comparison_type == "GT" and float(val[0]) > threshold):
			out_file.write(str(val[1]) + "\t" + str(val[0]) + "\n")
		elif(comparison_type == "GE" and float(val[0]) >= threshold):
			out_file.write(str(val[1]) + "\t" + str(val[0]) + "\n")
	
	#Finally...
	out_file.close()
	

#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])
