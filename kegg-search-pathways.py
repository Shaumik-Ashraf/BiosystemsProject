#kegg-search-pathways
#thread optimize!

def search_modules_with_threads(idA, idB, depth_limit, fill_solution, do_gibbs = False ):

	solution = {'found':False, 'modules':[], 'reactions':[], 'enzymes':[], 'Gibbs':0};
	GFE = 0
	max_threads = 4;
	active_threads = 0;
	threads = list(range(max_threads));
	
	mdlist = link("module", idA);
	if( mdlist == [] ):
		return solution; #no solution for module based search
	else:
		threads_to_spawn = min(max_threads, len(mdlist));
		for i in range(threads_to_spawn):
			#threads[i] = Kthread()
			#to be continued

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

			#end if
			break; #break out of for md in mdlist

	return solution;

#===================  main  =============================


