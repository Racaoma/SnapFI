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

# Usage: python Probscore.py <Output_File> <IDs_File>

import sys, os


def main(argv):
	
	#Get Inputs
	if(len(argv) < 2):
		print("Error! Probscore.py requires 2 arguments: <Output_File> and <IDs_File>")
		sys.exit(2)

	#Get the Results File Name
	try:
		input_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[1] + ".txt"
		output_file = os.environ.get('TOOLHOME') + "/Results/" + argv[0]
		
	except TypeError:
		print("TOOLHOME Environment not Set. Are you running Main.py?")
		sys.exit(2)

	#Get IDs & Models Folder Locations
	try:
		ids = open(input_file).read().split()
		models_folder = ids[0]
		ids = ids[1:]

	except:
		print("Specified <IDs_File> could not be located or is invalid")
		sys.exit(2)

	#Delete Previous Runs & Write Header
	out_file = open(output_file, 'w+')
	out_file.write(models_folder + "\n")

	#Save Previous Working Directory
	previious_dir = os.getcwd()
		
	#Change Current Working Directory
	os.chdir(os.path.dirname(__file__))
	
	#Display Progress
	print("Extracting Probscore from \"" + "Step_" + argv[1] + ".txt\"")
	
	#Iterate IDs
	for id_num in ids:
		
		#Get Model File
		model_file = models_folder + "ID_" + id_num + ".pdb"

		# Create Analysis Files
		os.system("phenix.clashscore " + model_file + " | grep \"clashscore\" | cut -d \" \" -f 3 > Clashscore.dat")
		os.system("phenix.ramalyze " + model_file + " | grep \"favored (G\" | cut -d \" \" -f 2 | cut -d % -f 1 > Ramalyze.dat")
		os.system("phenix.rotalyze " + model_file + " | grep \"outliers (G\" | cut -d \" \" -f 2 | cut -d % -f 1 > Rotalyze.dat")

		# Compute Probscore
		os.system("probityScore.py Clashscore.dat Rotalyze.dat Ramalyze.dat Probscore.tmp")
		
		# Write Results
		temp_file = open("Probscore.tmp")
		out_file.write(id_num + "\t" + temp_file.readline())
		temp_file.close()
		
		# Remove Temp Files
		os.remove("Probscore.tmp")
		os.remove("Clashscore.dat")
		os.remove("Ramalyze.dat")
		os.remove("Rotalyze.dat")

	#Finally...
	out_file.close()
	
	#Return to Previous Working Directory
	os.chdir(previious_dir)	


#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])
