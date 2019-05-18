# Biosystems project

## What This Is
 This program is a cross-platform command-line interface for interacting with the Kyoto 
 Encyclopedia of Genes and Genomes (KEGG). It provides easy commands to find, list, and
 get information on any compound, enzyme, or reaction in the KEGG database. It also provides
 a depth-first search algorithm for finding a series biological pathways that convert a given
 starting compound to a desired end compound. This can be done either through a pathway (KEGG 
 module) based search or a reaction based search, in `search-pathway` and `search-reactions`
 commands, respectively. 
 
 See [KEGG here](https://kegg.jp) (Kyoto Encyclopedia of Genes and Genomes)
 
 This project was in partial completement of BEE3600 - Biological and Cellular Enginerring,
 Cornell University
 
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
 This project is under the MIT License. See LICENSE.txt for more details.

## Possible Future Improvements
 It is unknown if this project will remain under active developement/support in the future, but 
 there some improvements which may be made to this program:
 - breadth-first search algorithm
 - thread optimization to reduce runtime
   + (A thread class based on Python threading.Thread was made, but not implemented)
 - parsing additional databases for pH, temperature, and other reaction conditions
 
 And as always, no program is made perfect; feel free to report issues or fork.
 
 ## (Code) Contributors
  - Shaumik Ashraf
  - Aaron-Earle Richardson
 
 
 
