from parser import serverwide_advancements
from sheet import write_sheet

def main():
	advancements = serverwide_advancements()
	write_sheet(advancements)

if __name__=="__main__":
	main()
