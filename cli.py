# cli.py
# a command-line interface with the kegg module
# enter <command> <args> ... to use
# current commands are help, exit, list, find, get

import kegg;

help_text = """
	Please give us an extension
"""

def needs_args(n):
	if len(command) < n:
		print("Warning, at least " + str(n-1) + " command arguement(s) required.");

# ========command-line loop================================
print( "Start" );
while 1==1:
	command = input().strip().split(" ");
	if command[0] == "help":
		print(help_text)
	elif command[0] == "exit":
		break;
	elif command[0] == "list":
		needs_args(2);
		out = kegg.list(command[1])
		print( str(out) );
	elif command[0] == "find":
		needs_args(2);
		out = kegg.find(command[1])
		print( str(out) );
	elif command[0] == "get":
		needs_args(2);
		out = kegg.get(command[1])
		print( str(out) );
	else:
		print("Command unrecognized");

