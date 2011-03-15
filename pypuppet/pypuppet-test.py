from base import pypuppet


# Create Test of functions

# You can pass in all the connection info via connect and other set commands
cert="/etc/puppetlabs/puppet/ssl/certs/cobbler.logicminds.corp.pem"
key="/etc/puppetlabs/puppet/ssl/private_keys/cobbler.logicminds.corp.pem"

# Create Object
puppet = pypuppet()

# Set the connection options
puppet.connect('puppet.logicminds.corp', '8140', 'production', 'facts', 'puppetagent1.logicminds.corp')

# Set the certificates
puppet.setcerts(cert,key)

# Decode the output from puppet into a python object
output = puppet.decode()

print output
print puppet.rawyaml.getvalue()
