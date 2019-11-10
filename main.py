from brainscript import *

def main():
	if len(sys.argv) == 2: 
		prgm = open(sys.argv[1]).read()
		b = BrainScript(prgm)
		b.execute()
	else: print("Usage:", sys.argv[0], "filename")

if __name__ == "__main__": main()