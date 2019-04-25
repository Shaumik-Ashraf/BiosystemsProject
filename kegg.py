# kegg.py
# database_access_code.py consolodated into a module
# requires: urllib3

import urllib3;

http = urllib3.PoolManager();

#direct simply joins the array with /s and sends request to kegg
def direct(arg_list):
	request = "http://rest.kegg.jp/"
	request += "/".join(arg_list);
	#print( request );
	response = http.request('GET', request).data.decode();
	#print( response );
	return(response);

def list(database):
	newstr = direct(['list', database]);
	#newstr = newstr.replace("\\t", "\t");
	newlist = newstr.split('\\n');
	#newlist[0] = newlist[0][2:]; #shave off trash at beggining of first element
	#del newlist[len(newlist)-1]; #shave off last element (trash)
	retlist = newlist.copy(); #for preallocation
	for i in range( len(newlist) ):
		retlist[i] = newlist[i].split('\\t');
	return(retlist);   #returns list of lists
		
def find(datatype):
	newstr = str(http.request('GET', 'http://rest.kegg.jp/find/{datatype}/'.format(datatype=datatype)).data)
	newstr = newstr.replace("\\t", "\t");
	newlist = newstr.split('\\n');
	newlist[0] = newlist[0][2:]; #shave off trash at beggining of first element
	del newlist[len(newlist)-1]; #shave off last element (trash)
	return(newlist);

def get(query):
	if query[0] == "R":
		prefix = "rn"
	elif query[0] == "C":
		prefix = "cpd"
	elif query[0:3] == "map":
		prefix = "path"
	elif len(query.split('.')) == 4:
		prefix = "ec"
	else:
		print("Warning: query type unindentified");
		
	text=str(http.request('GET', 'http://rest.kegg.jp/get/{0}:{1}'.format(prefix,query)).data);
	text = text.replace("\\t", "\t");
	text = text.replace("\\n", "\n");
	text = text[2:len(text)-1]; #rm first 2 and last characters (trash)
	return(text)

#get command id format to prefix map
#reaction: <id> = Rxxxxx, <prefix> = rn
#enzyme: <id> = n.n.n.n, <prefix> = ec
#path: <id> = mapxxxxx, <prefix> = path
#compound: <id> = Cxxxxx, <prefix> = cpd

def info(database):
	text=str(http.request('GET', 'http://rest.kegg.jp/info/{0}'.format(database)).data);
	#print("DEBUG: ", "text=", text);
	text = text.replace("\\t", "\t");
	text = text.replace("\\n", "\n");
	text = text[2:len(text)-1]; #rm first 2 and last characters (trash)
	return(text)


#def conv(two_ids)
#       text = direct(['conv', two_ids[0], two_ids[1]]);
		
def link(args):
        text = direct(['link', args[0], args[1]])
	

#def ddi()



ignore_this_string = """
def A2B(compoundA, compoundB):
	#set variable idA, ask if compoundA is correctly found
	templist = find( 'compound/{0}'.format(compoundA) );
	found = False;
	for i in range(len(templist)):
		templist2 = templist[i].split('\t')
		idA = templist2[0]
		print( 'Is your first compound also known as: {0}? [y/n]'.format(templist2[1]) )
		in_buffer = input();
		if in_buffer.upper().startswith('Y'):
			found = True;
			break;
		else:
			continue;
	if( !found ):
		print( '{0} could not be found.'.format(compoundA.capitalize()) )
		return( -1 );
	
	#set variable idB, ask if compoundB is correctly found
	templist = find( 'compound/{0}'.format(compoundB) );
	found = False;
	for i in range(len(templist)):
		templist2 = templist[i].split('\t')
		idB = templist2[0]
		print( 'Is your last compound also known as: {0}? [y/n]'.format(templist2[1]) )
		in_buffer = input();
		if in_buffer.upper().startswith('Y'):
			found = True;
			break;
		else:
			continue;
	if( !found ):
		print( '{0} could not be found.'.format( compoundB.capitalize() ) )
		return( -1 );
	
	#To be continued....
"""
