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

#Usage: python Retrieve_Model.py <Pbd_File> <Model_Number> <Absolute ID>
#Retrieve a predicted structure from a trajectory file, creating a sepparate pdb file.

import sys, os, subprocess


def main(argv):
	
	#Get Inputs
	if(len(argv) < 3):
		print("Error! Retrieve_Model.py requires 3 arguments: <Pdb_File> , <Model_Number> and <Absolute ID>")
		sys.exit(2)
	else:
		pdb_file = argv[0]
		model_num = argv[1]
		model_id = str(argv[2])

	#Path & File Variables
	base_dir = os.path.dirname(os.path.realpath(pdb_file)) + "/Models/"
	index_file = base_dir + os.path.basename(os.path.splitext(pdb_file)[0]) + ".index"

	#Set Output Name
	output_file = base_dir + "ID_" + model_id + ".pdb"

	#Check if Directory Exists
	if (not os.path.exists(base_dir)):
		os.makedirs(base_dir)

	#Check if Model Wasn't Already Retrieved
	if(not os.path.isfile(output_file) or os.path.getsize(output_file) == 0):
		
		#Create Index if Wasn't Already Created
		if(not os.path.isfile(index_file) or os.path.getsize(index_file) == 0):
			os.system("sed -n '/MODEL/ =' " + pdb_file + " > " + index_file)

		#Get Model
		line = subprocess.check_output("sed -n ' " + str(model_num) + " 'p " + index_file, shell=True).strip()
		os.system("sed -n ' " + line + " {n; :loop /ENDMDL/ q; p; n; b loop;}' " + pdb_file + " > " + output_file)


#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])
