import pycurl
import StringIO
import yaml


class pypuppet:

    # Setup the connection object with curl
    conn = pycurl.Curl()
    cert = None
    key = None
    host = None
    port = None
    url = None
    rawyaml = StringIO.StringIO()
    
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
        self.key = key
        self.connect()
                
    def connect(self,host=None, port=None, environment=None, resource=None, key=None):
       # This function is called by many of the set functions in order to re-create the url pattern
       # Build connection string url
      
       self.host = host
       self.port = port
       self.environment = environment
       self.resource = resource
       self.key = key
       # We will need to test all of these attributes before moving forward
       # create error if any of these are still undefined 
       # Update url and pycurl object 
       self.createurl()
       self.setcurlattrs()
       
    def createurl(self):
       self.url = "https://%s:%s/%s/%s/%s" % (self.host,self.port,self.environment,self.resource,self.key)
       print self.url
       self.conn.setopt(self.conn.URL, self.url)
       
    def decode(self):
        # Need to check for certs
        
        self.conn.setopt(self.conn.WRITEFUNCTION, self.rawyaml.write)
        self.conn.perform()
        self.conn.close()
        
        # Below is the yaml encoded output from puppet
        # Puppet isn't outputting well formatted yaml code that
        # this parser can parse so this is disabled for now
#        contents = self.rawyaml.getvalue()
        # Process the contents and Return the contents in a python object
#        return yaml.load(contents)

    def setcerts(self,cert, key):
        # Include the path to the cert and path to the private key
        # If these Certs are not set we cannot get any data out of puppet
        self.cert = cert
        self.key = key
        # Lets put some cert verfication here
        self.conn.setopt(self.conn.SSL_VERIFYPEER, 0)
        self.conn.setopt(self.conn.SSL_VERIFYHOST, 0)
        self.conn.setopt(self.conn.SSLCERT,self.cert)
        self.conn.setopt(self.conn.SSLKEY,self.key)

    def setcurlattrs(self,format='yaml'):
        # Setup the output to Yaml
        # setopt doesn't seem to like passing in strings
        formatstring = '[\"Accept: %s\"]' % (format)
        self.conn.setopt(self.conn.HTTPHEADER, ["Accept: yaml"])
        #self.conn.setopt(self.conn.VERBOSE,1)
        #c.setopt(conn.ENCODING, 'Accept: yaml')

        # So far this is the only attribute I can think of

