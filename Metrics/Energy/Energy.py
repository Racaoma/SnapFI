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

#Usage: python Energy.py <Output_File> <IDs_File> <Minimization Parameters File> <Number of CORES>

import sys, os

def main(argv):

	#Get Inputs
	if(len(argv) < 4):
		print("Error! Energy.py requires 4 arguments: <Output_File> , <IDs_File> , <Minimization Parameters File> and <Number of CORES>")
		sys.exit(2)

	#Get the Results File Name
	try:
		input_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[1] + ".txt"
		output_file = os.environ.get('TOOLHOME') + "/Results/" + argv[0]
		minimization_par = os.getcwd() + "/" + argv[2]

	except TypeError:
		print("TOOLHOME Environment not Set. Are you running Main.py?")
		sys.exit(2)

	#Get Number of Core
	try:
		cores = int(argv[3])
		if(cores <= 0):
			raise
		
	except:
		print("Invalid Number of Cores")
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
	print("Extracting Energy from \"" + "Step_" + argv[1] + ".txt\"")

	#Iterate IDs
	for id_num in ids:
		
		#Get Model File
		model_file = models_folder + "ID_" + id_num + ".pdb"

		#Define File Names
		in_file = "leap_id_" + id_num + ".in"
		prmtop_file = "job_id_" + id_num + ".prmtop"
		inpcrd_file = "job_id_" + id_num + ".inpcrd"
		
		#Write Leap Input File
		leap_file = open(in_file, 'w+')
		leap_file.write("source leaprc.ff12SB\n")
		leap_file.write("TARGET = loadpdb " + model_file + "\n")
		leap_file.write("SaveAmberParm TARGET " + prmtop_file + " " + inpcrd_file + "\n")
		leap_file.write("quit")
		leap_file.close()

		#Run Energy Minimization
		os.system("tleap -f " + in_file)
		os.system("mpirun -np " + str(cores) + " $AMBERHOME/bin/sander.MPI -O -i " + minimization_par + " -o output.out -p " + prmtop_file + " -c " + inpcrd_file + " -r mini.rst")

		#Open Results File
		results_file = open("output.out")
			
		#Read Output File & Write Final Results
		lines = results_file.readlines()
		for x in range(0, len(lines)):
			if(lines[x].strip() == "FINAL RESULTS"):
				output.write(id_num + "\t" + lines[x+5].split()[1] + "\n")
			
		#Close Output File
		results_file.close()

		#Remove Temporary Files
		os.remove(in_file)
		os.remove(prmtop_file)
		os.remove(inpcrd_file)
		os.remove("output.out")
		os.remove("mdinfo")
		os.remove("leap.log")
		os.remove("mini.rst")
		
		
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
