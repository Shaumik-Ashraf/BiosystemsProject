#kthreads.py
#thread class for kegg cli

import threading
import kegg

class Kthread(threading.Thread):
	FOR_MODULES = 0;
	FOR_REACTIONS = 1;
	count = 0;
	lock = threading.Lock();

	def __init__(self, cpdB, current_node, past_nodes, depth, limit, rn_or_md):
		threading.Thread.__init__(self)
		self.thread_id = count;
		self.cpdB = cpdB;
		self.current_node = current_node
		self.past_nodes = past_nodes
		self.depth = depth;
		self.limit = limit;
		self.rn_or_md = rn_or_md;
		
		if rn_or_md == Kthread.FOR_MODULES:
			self.name = "kthread-{0}-{1}".format(thread_id, "modules");
		else:
			self.name = "kthread-{0}-{1}".format(thread_id, "reactions");
		
		kthread.count += 1;
	
	def run(self):
		if rn_or_md == Kthread.FOR_MODULES:
			print( self.name + " processing:", end="" );
			solution = kegg.module_helper(self.cpdB, self.current_node, self.past_nodes, self.depth, self.limit);
		else:
			print( self.name + " processing:", end="" );
			solution = kegg.reaction_helper(self.cpdB, self.current_node, self.past_nodes, self.depth, self.limit);
