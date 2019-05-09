# kegg.py
# database_access_code.py consolodated into a module
# requires: urllib3

import urllib3;
import re;

http = urllib3.PoolManager();

#direct simply joins the array with slashes and sends request to kegg
def direct(arg_list):
	while '' in arg_list:
		arg_list.remove('');
	while None in arg_list:
		arg_list.remove(None);
	request = "http://rest.kegg.jp/";
	request += ('/'.join(arg_list));
	response = http.request('GET', request).data.decode()
	#decode() turns it into string
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
	#newlist[0] = newlist[0][2:]; #shave off trash at beggining of first element
	#del newlist[len(newlist)-1]; #shave off last element (trash)
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
	#text = text[2:len(text)-1]; #rm first 2 and last characters (trash)
	return(text)

#def conv(two_ids)
#       text = direct(['conv', two_ids[0], two_ids[1]]);
		
def link(database, query):
	temptext = direct(['link', database, query])
	templist = temptext.splitlines();
	while '' in templist:
		templist.remove('');
	retlist = []
	for i in range(len(templist)):
		linelist = templist[i].split();
		retlist.append( linelist[1] )
	return(retlist);

#get_extract returns a dictionary containing any info
#provided in from a get command
#i.e.: get/md:M00377 => { "ENTRY":M00377, "NAME":"Reductive ... "REACTION":{"rnxxx":[[a,b][c,d]]}}
#THIS ONLY ENTERS THE FIRST ENTRY FOR SOME REASON 
def get_extract(query):
	to_parse = get(query);
	lines = to_parse.splitlines();  
	ret = {};

	while '' in lines:
		lines.remove('')
	 
	blocks = [];
	j = -1;
	i = 0;
	while i < len(lines): #parse keys and blocks
		if lines[i] == '///':
			break;
		elif lines[i].startswith(' ') or lines[i].startswith('\t'): #if first character is a space
			blocks[j] += ('\n' + lines[i].strip()); #concat strings
		else:
			#start a new block
			j += 1; #start next blocks array element
			#print( "DEBUG: " + str(lines[i]) );
			temparray = lines[i].split();
			while '' in temparray:
				temparray.remove('');
			#print( "DEBUG: " + str(temparray) );
			#print( "DEBUG: " + str(temparray[1]) );
			key = temparray[0];
			ret[temparray[0]] = j;
			del temparray[0];
			blocks.insert(j, temparray);
			blocks[j] = " ".join(blocks[j]) #list => string
			if key == "ENTRY":
				tokens = blocks[j].split();
				ret[key] = tokens[0];
				ret["TYPE"] = tokens[1:];
		i += 1;
	keys2 = list(ret.keys());
	keys2.remove('ENTRY');
	keys2.remove('TYPE');
	
	for key in keys2: #parse blocks into structured dicts
		#print("DEBUG: " + key )
		#print("DEBUG: " + str(ret[key]))
		#print("DEBUG: " + blocks[ ret[key] ] )
		#print("DEBUG: " + str(int(ret[key])))
		block = blocks[ret[key]]
		if key == '///': #shouldnt occur
			break;
		elif key == "ENTRY":
			continue; 
		elif key == "COMPOUND":
			ret[key] = []
			lines = block.splitlines()
			for i in range(len(lines)):
				line = lines[i].strip()
				match_obj = re.match(r'(C[0-9]{5})[\s]+(.*)', line, 0);
				id = match_obj.group(1);
				name = match_obj.group(2);
				(ret[key]).append( {'ID':id, 'NAME':name} );
		elif (key == "REACTION") and ('Module' in ret["TYPE"]):
			ret[key] = [] # [{'ID':<id>, 'REACTANTS':[...], 'PRODUCTS':[...]}]
			lines = block.splitlines();
			for i in range(len(lines)): #parsing each line
				d = {'ID':'', 'REACTANTS':[], 'PRODUCTS':[] }
				line = lines[i].strip();
				tokens = line.split();
				while '' in tokens:
					tokens.remove('');
				
				if tokens == []:
					break;

				if ',' in tokens[0]:
					d['ID'] = tokens[0].split(',')[0];
				else:
					d['ID'] = tokens[0];
					#doesn't consider case of RX,RY+RZ
				
				passed_arrow = False;
				j = 1;
				while j < len(tokens): #parsing each token
					#print('parsing react')
					if tokens[j] == '->':
						passed_arrow = True;
					elif( (not passed_arrow) and (tokens[j] != '+') ):
						d['REACTANTS'].append(tokens[j]);
					elif( passed_arrow and (tokens[j] != '+') ):
						d['PRODUCTS'].append(tokens[j])
					j += 1

				ret[key].append(d);     
		elif (key == "REACTION") and ('Compound' in ret["TYPE"]):
			ret[key] = [];
			lines = block.splitlines();
			for each in lines:
				line = each.trim;
				tokens = line.split();
				while '' in tokens:
					tokens.remove('')
				for token in tokens:
					ret[key].append(token)
		elif (key == "EQUATION") and ('Reaction' in ret["TYPE"]):
			ret[key] = {'REACTANTS':[], 'PRODUCTS':[], 'RATIOS':[]}
			tokens = block.trim.split();
			while '' in tokens:
				tokens.remove('')
			
			passed_arrow = False;
			for token in tokens:
				if token == "<=>":
					passed_arrow = True;
				elif isdigit(token):
					ret[key]['RATIOS'].append(token);
				elif( token.startswith('C') and (not passed_arrow)):
					ret[key]['REACTANTS'].append( token );
				elif( token.startswith('C') ): #and passed_arrow (implied):
					ret[key]['PRODUCTS'].append( token );
					
		else:
			ret[ key ] = block;

	return ret;

"""IGNORE ME
def get_extract_module(md):
	text = get(md)
	#parse out first line, rest of text intact
	tup = text.partition('\n');
	firstline = tup[0];
	text = tup[2];  #without first line
	
	#extract data from first line
	data = text.split(" \t\n")
	ret['ENTRY'] = data[1];
	ret['TYPE'] = data[2:];
	
	#abuse regulaur expressions
	data = re.compile("^[A-Z]{2,}[\s]+").split(text);
"""

def A2B(compoundA, compoundB, depth_limit):
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
	if( not found ):
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
	if( not found ):
		print( '{0} could not be found.'.format( compoundB.capitalize() ) )
		return( -1 );
	
	solution = {'found':False, 'modules':[], 'reactions':[], 'enzymes':[]};
	mdlist = link("module", idA);
	if( mdlist == [] ):
		return solution; #no solution for module based search
		
	for md in mdlist:
		x = module_helper(idB, md, [], 0, depth_limit)
		if x[ len(x)-1 ]:
			#x is solution
			solution['found'] = True;
			solution['modules'] = x;
			break;
		else:
			#solution not found
			return( solution );
	
	for md in solution['modules']:
		md_data = get_extract(md);
		for i in md_data['REACTION']:
			r = md_data['REACTION'][i]['id']
			r_data = get_extract(r);
			solution['enzymes'].append( r_data['ENZYME'] )
			solution['reactions'].append(r)
		solution['modules'].append( md )
	
	return solution;
	
def module_helper(cpdB, module, past_modules, depth, limit):
	print( "Trying " + str(past_modules + [module]) );
	if depth > limit:
		return [False]
	elif module in past_modules:
		return [False]
	else:
		md_data = get_extract(module);
		rxns = [];
		#print(md_data['REACTION'])
		for i in range(len(md_data['REACTION'])):
			rxns = rxns + [ md_data['REACTION'][i]['ID'] ]
			if cpdB in md_data['REACTION'][i]['PRODUCTS']:
				return [module];

		rxns.reverse(); #optimizes for assimilatory pathways
		for r in rxns:
			next_md_list = link('module', r);
			for next_module in next_md_list:
				x = [module] + module_helper(cpdB, next_module, past_modules + [module], depth+1, limit); #recurse
				if x[ len(x)-1 ]: #if last element is not False
					#found!
					return x; #returns array of modules
				else:
					continue;

		return [False]; #no solutions


def reaction_helper(cpd_start, cpdB, reaction, past_reactions, depth, limit):
	#print( "Trying " + str(past_reactions + [reaction]) );
	if depth > limit:
		return [False];
	if reaction in past_reactions:
		return [False];
	rxn_data = get_extract(reaction);
	if cpd_start not in rxn_data['EQUATION']['REACTANTS']:
		return [False];
	products = rxn_data['EQUATION']['PRODUCTS'];
	if cpdB in products:
		return [reaction];
	else:
		for p in products:
			next_rxn_list = link('reaction', p);
			for next_reaction in next_rxn_list:
				x = [reaction] + reaction_helper(p, cpdB, next_reaction, past_reactions + [reaction], depth+1, limit);
				if x[ len(x)-1 ]: #if last element not False
					return x;
				else:
					continue;
					
		return [False];

def remove_id_prefix(s):
	i = s.index(':')
	return s[(i+1):]

def get_id(database, obj):
	templist = find2( database, obj );
	found = False;
	for i in range(len(templist)):
		templist2 = templist[i].split('\t')
		print( 'Is {0} the correct {1}? [y/n]'.format(templist2[1], database) )
		in_buffer = input();
		if in_buffer.upper().startswith('Y'):
			found = True;
			return templist2[0];
		else:
			continue;
	if( not found ):
		print( '{0} could not be found.'.format(compoundA.capitalize()) )
		return( -1 );

def GIBBS(RN): #Finds the Gibbs free energy for any kegg reaction via the reaction number
        newstr = http.request('GET', 'http://rest.kegg.jp/get/rn:{0}'.format(RN)).data.decode() 
        EC = newstr.split("ENZYME")[1].split("\n")[0].strip() 
        bcdat = http.request('GET', 'https://biocyc.org/META/NEW-IMAGE?type=EC-NUMBER&object=EC-{0}'.format(EC)).data.decode("utf-8", "ignore")
        bclink = bcdat.split("Reaction: \n                              \n <br> <a href=\"")[1].split("\" class=\"REACTION\"")[0].strip()
        brstr = http.request('GET', 'https://biocyc.org{0}'.format(bclink)).data.decode("utf-8", "ignore")
        if "Standard Gibbs Free Energy" in brstr:
                GFE = (brstr.split("kcal/mol")[0]).split("Standard Gibbs Free Energy (&Delta;<sub>r</sub>G<sup>\'&deg;</sup>): \n")[1].strip()
        else: 
                GFE = "Error, database does not have Gibbs Free Energy"
	
        return GFE


