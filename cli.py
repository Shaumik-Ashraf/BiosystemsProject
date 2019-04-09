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

        The databases in KEGG include but are not limited to:
                reaction
                enzyme
                genes
                compound
                pathway

        Note for get command:
                possible KEGG IDs include R03544, 3.2.42.1, C00116, and map12345
                the get command has only been programmed to check fo reaction,
                enzyme, compound, and map databases.

        See https://kegg.jp for more information on KEGG.
                
        Also, please give us an extension.
"""

def needs_args(n):
        if len(command) < n:
                print("Warning, at least " + str(n-1) + " command arguement(s) required.");

# ========command-line loop================================
print( "Start\n" );
while 1==1:
        print("kegg-cli>>", end="");
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
                needs_args(3);
                out = kegg.find( "{0}/{1}".format(command[1],command[2]) );
                print( str(out) );
        elif command[0] == "get":
                needs_args(2);
                out = kegg.get(command[1])
                print( str(out) );
        elif command[0] == "info":
                needs_args(2);
                out = kegg.info(command[1])
                print( str(out) );
        else:
                print("Command unrecognized");

print( "End" )
