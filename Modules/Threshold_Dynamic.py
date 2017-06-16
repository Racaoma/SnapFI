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

#Usage: python Threshold_Dynamic.py <Output_File> <Threshold Position> <Threshold Margin> <Metric File> <Comparison Type [LT|LE|GT|GE]> <OptionaL: Reversed=True/False> (Default False)
#Sort a Metric File and apply a filter based on a threshold from the best or worst prediction.

import sys, os, numpy


def main(argv):
	
	#Get Inputs
	if(len(argv) < 5):
		print("Error! Threshold_Dynamic.py requires at least 4 arguments: <Output_File> , <Threshold Position> , <Threshold Margin> , <Metric File> , <Comparison Type> and <OptionaL: Reversed=True/False> (Default False)")
		print("Comparison Types: LT = Less Than | LE = Less Than or Equal | GT = Greater Than | GE = Greater Than or Equal")
		sys.exit(2)
	else:
		
		try:
			threshold_pos = int(argv[1])
			if(threshold_pos < 0):
				raise
		except:
			print("Parameter <Threshold Position> is invalid")
			sys.exit(2)
		
		try:
			threshold_margin = float(argv[2])
		except:
			print("Parameter <Threshold Margin> is invalid")
			sys.exit(2)
		
		comparison_type = argv[4].upper()
		if(not(comparison_type == "LE" or comparison_type == "LT" or comparison_type == "GT" or comparison_type == "GE")):
			print("Comparison Type not Recognized. Aborting")
			sys.exit(2)
			
		inverted = False
		if(len(argv) == 6):
			if(argv[5].upper() == "REVERSED=TRUE"):
				print("Reversed = True")
				inverted = True

	#Get the Results File Name
	try:
		input_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[3] + ".txt"
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
			ids.append((float(temp[val+1]), int(temp[val])))
		
		#Sort IDs
		ids.sort(reverse=inverted)
		
	except:
		print("Specified <IDs_File> could not be located or is invalid")
		sys.exit(2)
	
	#Display Progress
	print("Applying Threshold on \"" + "Step_" + argv[3] + ".txt\"")
	
	#Delete Previous Runs & Write Header
	out_file = open(output_file, 'w+')
	out_file.write(models_folder + "\n")
	
	#Define Threshold
	if(threshold_pos > len(ids)):
		threshold_pos = len(ids)
		
	threshold = float(ids[threshold_pos][0]) * (1.0 + threshold_margin)

	print("Base Value = " + str(ids[threshold_pos][0]))
	print("Threshold = " + str(threshold))
	
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
