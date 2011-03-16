from node import Node
from base import pypuppet

# Testing for Node


# First Create the puppet object
puppet = puppetclient()

# Set up all the certs and keys
cert="/etc/puppetlabs/puppet/ssl/certs/cobbler.logicminds.corp.pem"
key="/etc/puppetlabs/puppet/ssl/private_keys/cobbler.logicminds.corp.pem"

# Set the certificates
puppet.setcerts(cert,key)

# Set the connection options
puppet.setconnection('puppet.logicminds.corp', '8140', 'production', 'facts', 'puppet.logicminds.corp')

# Connect to the puppet server
puppet.connect()

# Get the data from puppet
output = puppet.decode()

puppetnode = Node(output)

#print puppetnode.list()
#print puppetnode.getfacts()
print puppetnode.swapsize
print puppetnode.productcame
