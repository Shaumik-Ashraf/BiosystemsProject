# kegg.py
# database_access_code.py consolodated into a module
# requires: urllib3

import urllib3;

http = urllib3.PoolManager();

#direct simply joins the array with slashes and sends request to kegg
def direct(arg_list):
	request = "http://rest.kegg.jp/"
	request += "/".join(arg_list);
	response = http.request('GET', request).data.decode() #decode() turns it into string
	return(response);

def list2(database):
	newstr = direct(['list', database]);
	newlist = newstr.split('\n');
	retlist = newlist.copy(); #for preallocation
	for i in range( len(newlist) ):
		retlist[i] = newlist[i].split('\t');
	return(retlist);   #returns list of lists
		
def find(datatype):
	newstr = str(http.request('GET', 'http://rest.kegg.jp/find/{datatype}/'.format(datatype=datatype)).data)
	newstr = newstr.replace("\\t", "\t");
	newlist = newstr.split('\\n');
	newlist[0] = newlist[0][2:]; #shave off trash at beggining of first element
	del newlist[len(newlist)-1]; #shave off last element (trash)
	return(newlist);

def find2(database, query): #this is used in cli
	newstr = direct(['find', database, query])
	#newstr = newstr.replace("\\t", "\t");
	newlist = newstr.split("\n");
	newlist[0] = newlist[0][2:]; #shave off trash at beggining of first element
	del newlist[len(newlist)-1]; #shave off last element (trash)
	return(newlist);

def get(query):
	text = direct(['get', query]);
	text = text.replace("\\t", "\t");
	text = text.replace("\\n", "\n");
	#text = text[2:len(text)-1]; #rm first 2 and last characters (trash)
	return(text)

def info(database):
	text = direct(['info', database]);
	text = text.replace("\\t", "\t");
	text = text.replace("\\n", "\n");
	text = text[2:len(text)-1]; #rm first 2 and last characters (trash)
	return(text)

#def conv(two_ids)
#       text = direct(['conv', two_ids[0], two_ids[1]]);
		
def link(database, query):
        temptext = direct(['link', database, query])
        templist = temptext.split('\n')
        retlist = templist.copy();  #preallocate
        for i in range(len(templist)):
        	retlist[i] = templist[i].split('\t')[1]
        return(retlist);

#get_extract returns a dictionary containing any info
#provided in from a get command
#i.e.: get/md:M00377 => { "ENTRY":M00377, "NAME":"Reductive ... }
def get_extract(query):
	toparse = get(query);
	lines = toparse.splitlines();
	ret = {}; #new dictionary

	for line in lines:
		tokens = line.split(' ')
		while '' in tokens:
			tokens.remove('')
		if tokens[0] == '///':
			break;
		elif tokens[0].isupper():
			key = tokens[0]
			ret[ key ] = tokens[1:].join(' ')
		else:
			ret[ key ].append( tokens.join(' ') );

	#if ret.has_key( 'REACTION' ):
		#polish...
        
	return ret;

def param(RN):
    import re
    newstr = str(http.request('GET', 'http://rest.kegg.jp/get/rn:{RN}').data) #get enzyme number
    EC = newstr.split("ENZYME")[1].split("\\n")[0].strip()
    brstr = str(http.request('GET', 'https://www.brenda-enzymes.org/enzyme.php?ecno={EC}').data) #get brenda text

    return newstr
    


"""
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
	
	templist = link("module", idA);
	if( templist == [] ):
		#print warning and use link/reaction/idA
	i = 0;
	while i < :
		extract = get_extract(idA)
		#....


def A2B_helper()
"""
