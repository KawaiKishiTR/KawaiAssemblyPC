import assemble, newSchem, mcschematic, os
from colorama import Fore


#minecraft version
minecraft_version = mcschematic.Version.JE_1_16_1

#finding paths
main_folder = "\\".join(__file__.split("\\")[:-1])
programs = "programs"
binaryCode = "__binaryCode__"
schems = "__schems__"

#collecting written programs
written_programs = os.listdir(f"{main_folder}\\{programs}")
for index, program in enumerate(written_programs):
    print(f"{Fore.RED}({index}) {Fore.BLUE}>>> {Fore.GREEN}{program}{Fore.RESET}")

#selecting a program 
selection = written_programs[int(input(f"{Fore.BLUE}select a program number>>> {Fore.RED}"))]
print(Fore.RESET)
#assembling selected program to binary code
assemble.main(main_folder + "\\" + programs + "\\" + selection)

#assembling selected program to schematic
newSchem.main(main_folder + "\\" + binaryCode + "\\" + selection, minecraft_version)

