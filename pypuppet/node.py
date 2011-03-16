from puppetapi import puppetclient

class Node:
    facts = {}
    # This class will define the node
    def __init__(self,nodefacts):
        # This is a dict of facts given from puppet
        # Since the facts are dynamic it didn't make sense to statically type every fact in this class
        # The facts object is a multi-dimensional dict so lets make it one less dimension
        self.facts = nodefacts['values']

    
    # need a method that takes a parameter and uses the parameter as a key to return the has value
    # example node.swapspace  (this would return facts['swapspace'])
    def __getattr__(self, name):
        # Raise an attribute Error if the fact does not exist
        if not name in self.facts:
            raise AttributeError("That fact does not exist, check your spelling")
        
        else:
            return self.facts[name]

    def list(self):
        return self.facts.keys()

    def getfacts(self):
        return self.facts
    
    # possibly use __setattr__ to set attributes
    # I don't think setting facts will work since they will be overridden by facter on the OS

    def runcatalog(self, catalog):
        # We will need to setup a connection with the client instead of the host
        return None

    def getcatalog(self):
        return []

    def getreport(self):
        return None

    def getstatus(self):
        return None

    
    
