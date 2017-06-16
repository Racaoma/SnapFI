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

#Usage: python RMSD.py <Output_File> <IDs_File> <Model PDB> <Start-Residue> <Ending-Residue>

import sys, os, shutil


def main(argv):

	#Get Inputs
	if(len(argv) < 5):
		print("Error! RMSD.py requires 5 arguments: <Output_File> , <IDs_File> , <Model PDB> , <Start-Residue> and <Ending-Residue>")
		sys.exit(2)

	#Get the Results File Name
	try:
		input_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[1] + ".txt"
		output_file = os.environ.get('TOOLHOME') + "/Results/" + argv[0]
		model_pdb = os.path.abspath(argv[2])
		
	except TypeError:
		print("TOOLHOME Environment not Set. Are you running Main.py?")
		sys.exit(2)
		
	#Get Start Residues
	try:
		start_res = int(argv[3])
		if(start_res < 0):
			raise
	except:	
		print("Specified <Start-Residue> is invalid")
		sys.exit(2)
	
	#Get End Residues
	try:	
		end_res = int(argv[4])
		if(end_res < 0):
			raise
	except:	
		print("Specified <Ending-Residue> is invalid")
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
	print("Extracting RMSD from \"" + "Step_" + argv[1] + ".txt\"")

	#Create PRMTOP File
	leap_file = open("TEMP.in", 'w+')
	leap_file.write("source leaprc.ff12SB\n")
	leap_file.write("TARGET = loadpdb " + model_pdb + "\n")
	leap_file.write("SaveAmberParm TARGET TEMP.prmtop TEMP.incpcrd\n")
	leap_file.write("quit")
	leap_file.close()
	os.system("tleap -f TEMP.in")

	#Iterate IDs
	for id_num in ids:
		
		#Get Model File
		model_file = models_folder + "ID_" + id_num + ".pdb"
		
		#Format Input Command
		cmd = """
		parm TEMP.prmtop
		trajin %s [in]
		reference %s [pdb-file]
		rms [in] ref [pdb-file] :%s-%s@CA out rmsd.dat
		""" % (model_file, model_pdb, str(start_res), str(end_res))
		
		#RUN RMSD
		os.system("cpptraj <<EOF\n" + cmd + "\nEOF")	
		
		#Get Results from Temp File	
		out_file = open("rmsd.dat")
		output.write(id_num + "\t" + out_file.readlines()[1].split()[1] + "\n")
		out_file.close()
		
		#Delete Temporary Files
		os.remove("rmsd.dat")
	
	
	#Delete Temporary Files	
	os.remove("leap.log")	
	os.remove("TEMP.in")
	os.remove("TEMP.incpcrd")
	os.remove("TEMP.prmtop")
		
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
