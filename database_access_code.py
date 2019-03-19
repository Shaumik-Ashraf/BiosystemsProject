#BEE3600
#requires urllib3 to be installed

def kegglist(datatype):
    import urllib3
    http=urllib3.PoolManager()
    newlist=str(http.request('GET', 'http://rest.kegg.jp/list/{datatype}/'.format(datatype=datatype)).data).split('\\n')
    return(newlist)
    
def keggfind(datatype):
    import urllib3
    http=urllib3.PoolManager()
    newlist=str(http.request('GET', 'http://rest.kegg.jp/find/{datatype}/'.format(datatype=datatype)).data).split('\\n')
    return(newlist)

#creating comprehensive list of relevant data categories

compoundlist=kegglist('compound')
enzymelist=kegglist('enzyme')
reactionlist=kegglist('reaction')

#you can specifiy a particular reaction, compound, or enzyme by replicating the following examples

formatereactionlist=keggfind('reaction/formate')
