# kegg.py
# database_access_code.py consolodated into a module
# requires: urllib3

import urllib3;

http = urllib3.PoolManager();

def list(datatype):
        newstr = str(http.request('GET', 'http://rest.kegg.jp/list/{datatype}/'.format(datatype=datatype)).data)
        newstr = newstr.replace("\\t", "\t");
        newlist = newstr.split('\\n');
        newlist[0] = newlist[0][2:]; #shave off trash at beggining of first element
        del newlist[len(newlist)-1]; #shave off last element (trash)
        return(newlist);
    
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

