import pycurl
import cStringIO
import yaml
import re

class puppetclient:

    # Setup the connection object with curl
    conn = pycurl.Curl()
    cert = None
    key = None
    cakey = None
    host = None
    port = None
    url = None
    resource = None
    environment = None
    serialization = 'yaml'
    
    
    #def __init__(self):
        
       
    def sethost(self,host, port):
        # set the host if you need to set it after creating the object
        self.host = host
        self.port = port
        self.connect()

    def setenvironment(self,environment):
        self.environment = environment
        self.connect()

    def setresource(self,resource):
        self.resource = resource
        self.connect()

    def setkey(self,key):
        # The key is considered the endpoint or host
        self.key = key
        self.connect()

    def setserialization(self,serialization):
        # This can be used to set the format to something other than yaml such as pson
        self.serialization = serialization

    def setconnection(self,host, port, environment, resource, key):
       # This function is called by many of the set functions in order to re-create the url pattern
       # Build connection string url
      
       self.host = host
       self.port = port
       self.environment = environment
       self.resource = resource
       self.key = key
       values = [self.host, self.port, self.environment, self.resource, self.key]
       for t in values:
           # Check for Null value
           if not t:
               print 'vaule is null please use the set commands'
               # Need to handle this case if any of these are not valid

       self.connect()
    def connect(self):
       # This function is called by many of the set functions in order to re-create the url pattern
       # Build connection string url
      
      
           
       # We will need to test all of these attributes before moving forward
       # create error if any of these are still undefined 
       # Update url and pycurl object 
       self.createurl()
       self.setcurlattrs()
       
    def createurl(self):
       self.url = "https://%s:%s/%s/%s/%s" % (self.host,self.port,self.environment,self.resource,self.key)
       self.conn.setopt(self.conn.URL, self.url)
       
    def decode(self):
        rawyaml = cStringIO.StringIO()
        # Need to check for certs
        tempstring = None
        self.conn.setopt(self.conn.WRITEFUNCTION, rawyaml.write)
        
        self.conn.perform()
        # This fails on subsequent calls if we close it
        # Not sure what the ramifications are by keeping it open
        #self.conn.close()
        
        contents = rawyaml.getvalue()
        tempstring = contents
        # Below is the yaml encoded output from puppet
        # Puppet isn't outputting well formatted yaml code that
        # this parser can parse so we need a regex to remove those paticular lines
         # We will need a smart regex pattern to remove all the ruby object code tags
         # in the yaml output from puppet
         # examples of what is removed by regex
         #!ruby/object:Puppet::Node::Facts
        tempstring = re.sub('.*\!ruby\/.*','',tempstring)
        #load the contents and Return the contents in a python object
        return yaml.load(tempstring)

    def setcerts(self,cert, cakey):
        # Include the path to the cert and path to the private key
        # If these Certs are not set we cannot get any data out of puppet
        self.cert = cert
        self.cakey = cakey
        # Lets put some cert verfication here
        self.conn.setopt(self.conn.SSL_VERIFYPEER, 0)
        self.conn.setopt(self.conn.SSL_VERIFYHOST, 0)
        self.conn.setopt(self.conn.SSLCERT,self.cert)
        self.conn.setopt(self.conn.SSLKEY,self.cakey)

    def setcurlattrs(self,format='yaml'):
        # Setup the output to Yaml
        # setopt doesn't seem to like passing in strings
        formatstring = '[\"Accept: %s\"]' % (format)
        self.conn.setopt(self.conn.HTTPHEADER, ["Accept: yaml"])
        #self.conn.setopt(self.conn.VERBOSE,1)
        #c.setopt(conn.ENCODING, 'Accept: yaml')

        # So far this is the only attribute I can think of

