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

#Usage: python Main.py <Input File>
import sys, os

def main(argv):
		
	#Get Inputs
	if(len(argv) < 1):
		print("Error! Main.py requires 1 argument: <Input File>")
		sys.exit(2)
		
	#Define TOOLHOME Environment
	if(os.environ.get('TOOLHOME') == None):
		os.environ["TOOLHOME"] = os.path.dirname(os.path.abspath(__file__))
		
	#Commands Array (Step Name, Command, Module)
	commands = []
	
	#Read Input File
	with open(sys.argv[1]) as input_file:
		
		#Read Line
		for line in input_file:
		
			#Check for Comments
			if(line[0] == '#'):
				continue
				
			else:
				
				#Eliminate Comments & Split Line
				line = line.split('#', 1)[0]
				line_words = line.split('=', 1)
				
				if(len(line_words) == 2):
				
					#Check for STEP
					if(line_words[0].split()[0] == "STEP"):
						step_file = "Step_" + line_words[0].split()[1] + ".txt"
						commands.append((step_file, line_words[1].strip(), line_words[1].split(".py")[0].strip() + ".py"))
	
	#Import Modules
	for x in range(0, len(commands)):
		
		sys.path.append(os.path.dirname(os.path.realpath(commands[x][2])))
		
		try:
			imported = __import__(os.path.basename(os.path.splitext(commands[x][2])[0]))
		except:
			print("Could not locate " + commands[x][2])
			sys.exit(2)
		
		commands[x] = (commands[x][0], commands[x][1], imported)
		
	#Execute Commands
	for command in commands:
		
		#Split Parameters
		parameters = [command[0]]
		parameters[1:] = command[1].split(".py", 1)[1][1:-1].split(",")
		parameters = map(str.strip, parameters)
		
		#Execute Module
		print("-----------------------------------------------")
		command[2].main(parameters)
	
	#Finally...
	print("-----------------------------------------------")
	print("All Done!")
	
#DEFINE MAIN
if __name__ == "__main__":
	main(sys.argv[1:])

