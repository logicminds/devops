from puppetapi import puppetclient


# Create Test of functions
def test_facts():
    hostlist = ['puppetagent1.logicminds.corp', 'cobbler.logicminds.corp', 'puppet.logicminds.corp']
    for i in hostlist:
        puppet.setkey(i)
        myoutput = puppet.decode()
        myoutput = myoutput['values']
        print "host %s has %s of swapspace" % (i,myoutput['swapsize'])        


# You can pass in all the connection info via connect and other set commands
cert="/etc/puppetlabs/puppet/ssl/certs/cobbler.logicminds.corp.pem"
key="/etc/puppetlabs/puppet/ssl/private_keys/cobbler.logicminds.corp.pem"

# Create Object
puppet = puppetclient()

# where production = environment
# where facts = resource
# where cobbler.logicminds.corp = key

# Set the certificates
puppet.setcerts(cert,key)

# Set the connection options
puppet.setconnection('puppet.logicminds.corp', '8140', 'production', 'facts', 'puppet.logicminds.corp')

puppet.connect()

# Decode the output from puppet into a python object
#output = puppet.decode()
#print output

test_facts()
#puppet.setresource('resource_types')
#puppet.setkey('*')
#output = puppet.decode()
#print output
#print puppet.rawyaml.getvalue()


