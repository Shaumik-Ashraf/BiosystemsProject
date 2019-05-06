# cli.py
# a command-line interface with the kegg module
# enter <command> <args> ... to use
# current commands are help, exit, list, find, get

import kegg;

help_text = """
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
				set <setting> <value>

	The databases in KEGG include but are not limited to:
		reaction
		enzyme
		genes
		compound
		pathway

		Possible settings to change are:
				list-limit -> maximum number of elements to output from a list, set to -1 for no limit
				output-line-limit -> maximum number of lines to output (excluding lists), set to -1 for no limit
				search-depth-limit -> Equals the base-n logrithm of O(n) of run time of search-pathway; the 
					bigger this number is, the exponentially larger the loading time. Too high of a number may 
					improve search results but may also cause the program to crash.
				verbose -> prints detailed output on what the program is doing, either True/False
				
	See https://kegg.jp for more information on KEGG.
"""

def needs_args(n):
	if len(command) < n:
		print("Warning, at least " + str(n-1) + " command arguement(s) required.");

def print_list(lst, limit):
	if limit > 0 and limit < len(lst):
		for i in range( limit ):
			print( str(lst[i]) );
	else:
		for i in range( len(lst) ):
			print( str(lst[i]) );

def print_text(t, limit):
	if limit > 0:
		print( t[0:limit] );
	else:
		print( t );

def singularize(s):
        if s.endswith('s'):
                return s[:len(s)-1]

# ========command-line loop================================
print( "Start KEGG Command-Line Interface" );
list_limit = 20;
output_line_limit = 20;
depth_limit = 50;
verbose = False;
defined = {'water':'C00001', 'H20':'C00001'}
print("Settings: " + str( {'list-limit':list_limit, 'output-line-limit':output_line_limit, 'verbose':verbose, 'depth-limit':depth_limit} ) + "\n");
while 1==1:
	print("kegg-cli>>", end="");
	command = input().strip().split(" ");
	for i in range(len(i)):
                if i==1:
                        command[i] = singularize(command[i])
                if defined.has_key(command[i]):
                        command[i] = defined[command[i]]
        
	if command[0] == "help":
		print(help_text);
	elif command[0] == "exit":
		break;
	elif command[0] == "set":
		if len(command) < 3:
			print("Usage: set <setting> <value>");
		elif command[1]=="list-limit":
			list_limit = int(command[2]);
		elif command[1]=="output-line-limit":
			output_line_limit = int(command[2]);
		elif command[1]=="depth-limit":
			depth_limit = int(command[2]);
		elif command[1]=="verbose":
			if command[2] == "true":
				verbose = True;
			else:
				verbose = False;
		else:
			print( command[1] + " unrecognized" );
	elif command[0] == "list":
		needs_args(2);
		out = kegg.list(command[1]);
		print_list( out, list_limit );
	elif command[0] == "find":
		needs_args(3);
		out = kegg.find2( command[1], command[2] );
		print_list( out, list_limit );
	elif command[0] == "get":
		needs_args(2);
		out = kegg.get(command[1]);
		print_text( out, output_line_limit );
	elif command[0] == "info":
		needs_args(2);
		out = kegg.info(command[1]);
		print_text( out, output_line_limit );
	elif command[0] == "link":
		needs_args(2);
		out = kegg.link(command[1], command[2]);
		print_list(out, list_limit);
	elif command[0] == "extract":
		needs_args(2);
		if not command[1].numeric():
			print('Require kegg id')
		dct = get_extract(command[1]);
		print( str(dct) );
	elif command[0] == "search-pathway":
		print("unimplemented")
		
	elif command[0] == "search" and command[1] == "pathway":
		print("You mean search-pathway");

	elif command[0] == "define":
                kid = get_id(command[1], command[2]);
                kid = remove_id_prefix(kid);
                defined[command[2]] = kid;
        elif command[0] == "see-defined":
                for k in defined.keys():
                        print( k + ": " + defined[k] );
	else:
		print("Command unrecognized");

print( "End" )
