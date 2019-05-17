# Biosystems project

## Goal
 Design a program which extracts biochemical networks from kegg database
 and find an optimal path from molecule A to molecule B 
 
 See [KEGG](https://kegg.jp) (Kyoto Encyclopedia of Genes and Genomes)
 
## Design
 1. Extraction - KEGG rest api
 2. Organization
 3. Path Identification - depth-first search algorithm
 4. Optimization
 
## Dependencies
 - python >3.0
 - urllib3; for information see [Repository here](https://github.com/urllib3/urllib3)
 - certifi; to install: `pip install certify`
 - requests; to install: `pip install requests`

## How to use
```
	This is a command-line interface program for interacting with
	the KEGG database. It operates by entering lines in the following
	format:
		<command> <arguement 1> <arguement 2> ... <arguement n> <ENTER>

	where < > is replaced by what the word within the brackets represent
	(WITHOUT the brackets themselves.) The number of arguements required
	for each command various. Here is a list of all commands, the arguements
	required (if any), and what they do:

		help (no arguements) - print this message
		exit (no arguements) - end program
		list <database> - lists all entries in the database specified (see below for possible databases)
		find <database> <term to search> - returns all entries in database with term specified
		get <kegg id> - returns information about object with specified kegg id
		info <database> - returns information about the database
		set <setting> <value> - change settings
		define <database> <name> - will make <name> interchangeable with its kegg id in the cli
		see-defined (no arguements) - see a list of all defined names/kegg ids
		see-settings (no arguements) - print settings
		search-pathway <compound A> <compound B> - depth-first search of biological pathway from A to B
		search-reaction <compound A> <compound B> - depth-first search of reaction series from A to B
		
	The databases in KEGG include but are not limited to:
		reaction
		enzyme
		compound
		pathway

	Possible settings to change are:
		list-limit -> maximum number of elements to output from a list, set to -1 for no limit
		output-line-limit -> maximum number of lines to output (excluding lists), set to -1 for no limit
		search-depth-limit -> Equals the exponent of exponential O(n) run time of search-pathway; the 
			bigger this number is, the exponentially larger the loading time. Too high of a number may 
			improve search results but will exponentially increase search time.
		verbose -> prints detailed output on what the program is doing, either True/False
				
	See https://kegg.jp for more information on KEGG.
```

## License
