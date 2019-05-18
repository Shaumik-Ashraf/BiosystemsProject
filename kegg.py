# kegg.py
# database_access_code.py consolodated into a module
# requires: urllib3, certifi (usually installed with urllib3), requests

import urllib3
import re
#import threading
import time
import requests

requests.packages.urllib3.disable_warnings()
http = urllib3.PoolManager()
all_past_intermediates = [];
all_intermediate_depths = [];

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

#get_extract returns a dictionary containing any info rest.kegg.jp/get/* returns
#i.e.: get/md:M00377 => { "ENTRY":"M00377" "NAME":"Reductive ... "REACTION":{"rnxxx":[[a,b][c,d]]}}
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
					temp = tokens[0].split(',');
					d['ID'] = temp[len(temp)-1]
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
				line = each.strip();
				tokens = line.split();
				while '' in tokens:
					tokens.remove('')
				for token in tokens:
					ret[key].append(token)
		elif (key == "EQUATION") and ('Reaction' in ret["TYPE"]):
			ret[key] = {'REACTANTS':[], 'PRODUCTS':[], 'RATIOS':[]}
			tokens = block.strip().split();
			while '' in tokens:
				tokens.remove('')
			
			passed_arrow = False;
			for token in tokens:
				if token == "<=>":
					passed_arrow = True;
				elif token.isdigit():
					ret[key]['RATIOS'].append(token);
				elif( token.startswith('C') and (not passed_arrow)):
					ret[key]['REACTANTS'].append( token );
				elif( token.startswith('C') ): #and passed_arrow (implied):
					ret[key]['PRODUCTS'].append( token );
					
		else:
			ret[ key ] = block;

	return ret;

def A2B(compoundA, compoundB, depth_limit = 10, do_gibbs = False, verbose = True):
	#set variable idA, ask if compoundA is correctly found
	idAlist = []
	if re.compile('C\d{5,}').match(compoundA):  #cpd id was provided
		idA = compoundA
	else:
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
		if( not found ):
			print( '{0} could not be found.'.format(compoundA.capitalize()) )
			return( -1 );
		else:
			idAlist.append(idA.split(':')[1])
			extras = get_extract(idA)
			if "COMMENT" in extras:
				for moreidAs in extras["COMMENT"].split('\n'):
					idAlist.append(re.search("(C\d\d\d\d\d)", moreidAs).group())
			
	#set variable idB, ask if compoundB is correctly found
	if re.compile('C\d{5,}').match(compoundB):
		idB = compoundB;
	else:
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
		if( not found ):
			print( '{0} could not be found.'.format( compoundB.capitalize() ) )
			return( -1 );
		else:
			idB = idB.split(':')[1];
		
	return search_modules(idAlist, idB, depth_limit, True, do_gibbs, verbose);

def A2Br(compoundA, compoundB, depth_limit = 20, do_gibbs = False, verbose = True):
	#set variable idA, ask if compoundA is correctly found
	idAlist = []
	if re.compile('C\d{5,}').match(compoundA):  #cpd id was provided
		idA = compoundA
	else:
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
		if( not found ):
			print( '{0} could not be found.'.format(compoundA.capitalize()) )
			return( -1 );
		else:
			idAlist.append(idA.split(':')[1])
			extras = get_extract(idA)
			if "COMMENT" in extras:
				for moreidAs in extras["COMMENT"].split('\n'):
					idAlist.append(re.search("(C\d\d\d\d\d)", moreidAs).group())
	#set variable idB, ask if compoundB is correctly found
	if re.compile('C\d{5,}').match(compoundB):
		idB = compoundB;
	else:
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
		if( not found ):
			print( '{0} could not be found.'.format( compoundB.capitalize() ) )
			return( -1 );
		else:
			idB = idB.split(':')[1];
		
	return search_reactions(idAlist, idB, depth_limit, True, do_gibbs, verbose );


def search_modules(idAlist, idB, depth_limit, fill_solution = True, do_gibbs = False, verbose = True ):

	solution = {'found':False, 'modules':[], 'reactions':[], 'enzymes':[], 'Gibbs':0};
	for idA in idAlist:
		print(idA)
		mdlist = link("module", idA);
		if( mdlist == [] ):
			#print('problem')
			#return solution; 
			continue #no solution for module based search
		#sollist = []
		GFE = 0
		for md in mdlist:
			x = module_helper(idB, md, [], 0, depth_limit)
			print(x)
			n = 0
			if x[ len(x)-1 ]:  #x is solution
				solution['found'] = True;
				print("Solution found!");
				solution['modules'] = x;
				if fill_solution:
					print("Filling in useful information...");
					for md in solution['modules']:
						md_data = get_extract(md);
						print(solution['modules'])
						for i in range(len(md_data['REACTION'])):
							#print(i)
							r = md_data['REACTION'][i]['ID']
							r_data = get_extract(r);
							solution['enzymes'].append( r_data['ENZYME'] )
							solution['reactions'].append(r)
							if do_gibbs:
								print("Hacking several other databases for Gibbs Free Energy ({0})".format(i));
								solution['Gibbs'], n = GIBBS(r,n)
				break; #break out of for md in mdlist

	return solution;  #I do not believe this ever gets called

def search_reactions(cpdA_idlist, cpdB_id, depth_limit, fill_solution = True, do_gibbs = False, verbose = True):
	if (depth_limit < 0):
		depth_limit = 9999;
	all_past_intermediates.clear();
	all_intermediate_depths.clear();
	for cpdA_id in cpdA_idlist:
		solution = {"found":False, "reactions":[], "enzymes":[], "Gibbs":0}
		#past_reactions = []
		reactions = link("reaction", cpdA_id);
		if len(reactions)==0:
			continue; #no solutions	
		for rn in reactions:
			solution["reactions"] = reaction_helper(cpdB_id, rn, [], cpdA_id, 0, depth_limit, verbose)
			if solution["reactions"][ len(solution["reactions"])-1 ]: #if last reaction is not false:
				solution['found'] = True;
				#fill out solution here!!!!
				return solution;	
	if fill_solution:
		solution['reactions'] = [];
		solution['enzymes'] = [];
	return(solution);
		
def module_helper(cpdB, module, past_modules, depth, limit):
	print(depth)
	if depth > limit:
		return [False]
	elif module in past_modules:
		return [False]
	else:
		print( "Trying " + str(past_modules + [module]) );
		md_data = get_extract(module);
		rxns = [];
		#print(md_data['REACTION'])
		for i in range(len(md_data['REACTION'])):
			rxns = rxns + [ md_data['REACTION'][i]['ID'] ]
			print("\tis {0} in products of".format(cpdB) + str(md_data['REACTION'][i]) + "?")
			if cpdB in md_data['REACTION'][i]['PRODUCTS']:
				return [module];

		rxns.reverse(); #optimizes for assimilatory pathways
		for r in rxns:
			next_md_list = link('module', r);
			for next_module in next_md_list:
				x = [module] + module_helper(cpdB, next_module, past_modules + [module], (depth+1), limit); #recurse
				if x[ len(x)-1 ]: #if last element is not False
					#found!
					return x; #returns array of modules

		return [False]; #no solutions

#The following compounds are blacklisted becuase they are too common
#water, oxygen
blacklisted_compounds = ['C00001', 'C00007'] #water and Oxygen because they are not likely products of efficient reaction pathways
def reaction_helper(cpdB, 
					reaction,  
					past_reactions,
					intermediate, 
					rdepth, 
					limit,
					verbose = True):
	#uses global called all_past_intermediates and all_intermediate_depths (list)

	if verbose:
		print( "D{0} | Trying ".format(rdepth) + str(past_reactions + [reaction]) );

	if ( rdepth > limit) :
		if verbose:
			print('Too phat')
		return [False];

	if reaction in past_reactions:
		return [False];

	if ( intermediate in all_past_intermediates ):
		if rdepth < all_intermediate_depths[ all_past_intermediates.index(intermediate) ]:
			all_intermediate_depths[ all_past_intermediates.index(intermediate) ] = rdepth;
			if verbose:
				print("Refound intermediate in possible pathway");
		else:
			return [False];
	
	rxn_data = get_extract(reaction);
	if (cpdB in rxn_data['EQUATION']['REACTANTS']) and (intermediate in rxn_data['EQUATION']['REACTANTS']):
		if verbose:
			print('\tBoth in reactants')
		return [False];
	elif (cpdB in rxn_data['EQUATION']['PRODUCTS']) and (intermediate in rxn_data['EQUATION']['PRODUCTS']):
		if verbose:
			print('\tBoth in products')
		return [False];
	elif (cpdB in rxn_data['EQUATION']['PRODUCTS']) and (intermediate in rxn_data['EQUATION']['REACTANTS']):
		if verbose:
			print("\tFound!")
		return [reaction];
	elif (cpdB in rxn_data['EQUATION']['REACTANTS']) and (intermediate in rxn_data['EQUATION']['PRODUCTS']):
		if verbose:
			print("\tFound! (in a reverse reaction)")
		return [reaction];
	
	if( intermediate in rxn_data['EQUATION']['PRODUCTS'] ):
		otherside = rxn_data['EQUATION']['REACTANTS'];
	else:
		otherside = rxn_data['EQUATION']['PRODUCTS'];
		if cpdB in otherside:
			if verbose:
				print("\tFound 2, electric boogaloo!")
			return [reaction];
	
	if intermediate not in blacklisted_compounds:
		all_past_intermediates.append( intermediate );
		all_intermediate_depths.append( rdepth );

	for p in otherside:
		#p is next_intermediate
		if p in blacklisted_compounds:
			continue;
		if p in all_past_intermediates: 
			if rdepth >= all_intermediate_depths[ all_past_intermediates.index(p) ]:
				continue; #start next loop/iteration
		next_rxn_list = link('reaction', p);
		for next_reaction in next_rxn_list:
			#print("\trecurse")
			x = [reaction] + reaction_helper(cpdB, next_reaction, past_reactions + [reaction], p, (rdepth+1), limit, verbose);
			if x[ len(x)-1 ]: #if last element not False
				return x;

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
	if( not found ):
		print( '{0} could not be found.'.format(compoundA.capitalize()) )
		return( -1 );

def GIBBS(RN,unknownreactions = 0): #Finds the Gibbs free energy for any kegg reaction via the reaction number
    try:
    	GFE = 0
    	newstr = http.request( 'GET', 'http://rest.kegg.jp/get/rn:{0}'.format(RN)).data.decode() 
    	EClist = newstr.split("ENZYME")[1].split("\n")[0].strip().split()
    	for EC in EClist:
    		if(not re.search("\d[.]\d[.]\d[.]\d", EC) and EC) : 
    			EC = re.search("\d[.]\d[.]\d[.]\d", http.request('GET', 'http://rest.kegg.jp/get/rn:{0}'.format(RN)).data.decode()).group()
    		elif (not re.search("\d[.]\d[.]\d[.]\d", EC) and not (EC)):
    			print('No Gibbs can be found')
    			GFE = 0
    			unknownreactions += 1
    			continue
    		bcdat = http.request( 'GET', 'https://biocyc.org/META/NEW-IMAGE?type=EC-NUMBER&object=EC-{0}'.format(EC)).data.decode("utf-8", "ignore");
    		bclink = bcdat.split("Reaction:")[1].split("\n <br> <a href=\"")[1].split("\" class=\"REACTION\"")[0].strip();
    		brstr = http.request( 'GET', 'https://biocyc.org{0}'.format(bclink)).data.decode("utf-8", "ignore")
    		if "Standard Gibbs Free Energy" in brstr:
    			GFE += float(brstr.split("kcal/mol")[0].split("Standard Gibbs Free Energy")[1].split("\n")[1].strip()) 
    		else: 
    			unknownreactions += 1
    	return(GFE,unknownreactions)
    except:
    	unknownreactions += 1
    	return(GFE,unknownreactions)

