from puppetapi import puppetclient
from node import Node


#This class is more of a wrapper for the puppetclient class as well as providing an easy way to get and set
# specific items that cannot be done at the node level

class puppetbase:
    puppet = None
    
    def __init__(self, pupclient):
        # This is mandatory that you set the client
        self.puppet = pupclient

    #def signcerts(self,cert,key):
    #    self.puppet.setcerts(cert,key)

    def setcertsigning(self):
        return None

    def getnodes(self):
        # Return a list of nodes that are under puppet control
        return getcertlist()

    def getnode(self,fqdn):
        # Return a node object of the hostname
        # set the key "hostname" then return 
        self.puppet.setkey(fqdn)
        puppetnode = Node(self.puppet.decode())
        return puppetnode

    def getrejectedcerts(self):
        self.puppet.setresource("certificate_revocation_list")
        self.puppet.setkey("ca")
        rejected = self.puppet.decode()
        return rejected

    def getcertlist(self):
        return []

    def getcertreqs(self, key='all'):
        self.puppet.setresource("certificate_requests")
        self.puppet.setkey(key)
        reqs = self.puppet.decode()
        return reqs
    
    def gethostlist(self):
        return []
    


