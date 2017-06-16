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

#Usage: python Load_PDB.py <Output_File> <Pbd_Files>
#Merge several PDBs and give each prediction an ID.

import sys, os, subprocess, Retrieve_Model


def main(argv):
	
	#Get Inputs
	if(len(argv) < 2):
		print("Error! Load_PDB.py requires 2 arguments: <Output_File> and <Pbd_Files>")
		sys.exit(2)
	else:
		pdb_files = argv[1:]

	#ID Count Variable
	id_count = 1

	#Iterate Through PDB Files
	for pdb_file in pdb_files:
		
		#Display Progress
		print("Extracting Models from \"" + os.path.basename(pdb_file) + "\"")
		
		try:
			#Get Number of Models
			models = int(subprocess.check_output("grep -c 'MODEL' " + pdb_file, shell=True).strip())
			
			#Extract Models
			for model in range(1,models+1):
				arguments = [pdb_file, model, id_count]
				Retrieve_Model.main(arguments)
				id_count = id_count + 1
		except:
			print("Specified <Pdb_File> is invalid")
			sys.exit(2)
			
			
	#Get the Results File Name
	try:
		results_file_name = os.environ.get('TOOLHOME') + "/Results/"
		if(not os.path.exists(results_file_name)):
			os.mkdir(results_file_name)
		results_file_name = results_file_name + argv[0]
		
	except TypeError:
		print("TOOLHOME Environment not Set. Are you running Main.py?")
		sys.exit(2)
		
	#Open Results File for Writing
	results_file = open(results_file_name, 'w+')

	#Write Header Contained Models Location
	results_file.write(os.path.dirname(os.path.realpath(pdb_files[0])) + "/Models/\n")

	#Write IDs
	for model in range(1,id_count):
		results_file.write(str(model) + "\n")
		
	#Finally...
	results_file.close()
		


#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])
