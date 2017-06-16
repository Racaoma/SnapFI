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

#Usage: python GDT.py <Output_File> <IDs_File> <Model PDB>

import sys, os, shutil


def main(argv):

	#Get Inputs
	if(len(argv) < 3):
		print("Error! GDT.py requires 3 arguments: <Output_File> , <IDs_File> and <Model PDB>")
		sys.exit(2)

	#Get the Results File Name
	try:
		input_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[1] + ".txt"
		output_file = os.environ.get('TOOLHOME') + "/Results/" + argv[0]
		model_pdb = os.path.abspath(argv[2])

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
	
	#Open Output File
	output = open(output_file, "w+")
	output.write(models_folder + "\n")

	#Save Previous Working Directory
	previious_dir = os.getcwd()
		
	#Change Current Working Directory
	os.chdir(os.path.dirname(__file__))

	#Display Progress
	print("Extracting GDT from \"" + "Step_" + argv[1] + ".txt\"")

	#Iterate IDs
	for id_num in ids:
		
		#Get Model File
		model_file = models_folder + "ID_" + id_num + ".pdb"

		#Copy PDB File & Append MODEL and ENDMDL
		shutil.copy(model_file, "temp.pdb")
		os.system("sed -i '1iMODEL	1' temp.pdb")
		os.system("echo ENDMDL >> temp.pdb")
		
		#RUN GDT
		os.system("clusco_cpu -t temp.pdb -s gdt -e " + model_pdb + " -o gdt.dat")
		
		#Get Results from Temp File
		out_file = open("gdt.dat")
		output.write(id_num + "\t" + out_file.readline().split()[2] + "\n")
		out_file.close()
		
		#Delete Temporary Files
		os.remove("temp.pdb")
		os.remove("gdt.dat")
		
	# Finally...
	output.close	

	#Return to Previous Working Directory
	os.chdir(previious_dir)	


#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])
