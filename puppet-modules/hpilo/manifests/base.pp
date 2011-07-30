# Class: hpilo
#
# This module manages hpilo
#
# Parameters:
#
# Actions:
#
# Requires:
#
# Sample Usage:
#
# [Remember: No empty lines between comments and class definition]
class hpilo::base {

      # You will need to define these parameters for the static templates to work correctly
      
      # this is your dns server
      $dns = '192.168.1.1'
      
      # this is your netmask
      $netmask = '255.255.255.0'

      # this is the default admin username you wish to create
      $ilouser = 'admin'

      # this is the default password for the default admin user
      $ilouserpass = 'password'
      
      # set to true if you want to use the auto ip setting which will determine the ip and gateway automatically
      # based on the current ip address of the system.  If autoip is false you will need to figure out how to automatically
      # assign a static ip.  
      $autoip = "false"

      ###############  Set only if autoip is false  #######################
      # You will need to set this if autoip is false
      $mygateway = '192.168.1.254'

      # You will need to set this if autoip is false
      $myiloip = '192.168.1.2'
      
      ###############  ###########################  #######################
       
      ###############  Set only if autoip is true  #######################
      # if you want to put your ilo card on a separate network  example: 192.168.xxx.22, disregard if autoip is false
      #$ilonet = 'xxx' 
      $ilonet = '27'
      
      # this is the gateway bit if using a 24 bit netmask: example: 192.168.25.xxx, disregard if autoip is false
      $gwbit = '240' 
      
      ###############  ###########################  #######################
      

      
       # Define where you want your settings file and log file to go
      $logfile='/tmp/ilosettings.log'
      $settingsfile='/ilosettings.xml'
      # Don't run these if not an HP machine
      if ( $manufacturer ) and ( $manufacturer == 'HP') {
          # Not all ilos have the same feature set and thus ilo configs are not backwards compatible
	  case $productname {
		/G5/: { $ilogen = 2 }
		/G6/: { $ilogen = 2 }
		/G4/: { $ilogen = 1 }
		/G3/: { $ilogen = 0 }
		/G7/: { $ilogen = 3 }
		default: { $ilogen = 1 }
                
	  }
	  exec{"/sbin/hponcfg -f ${settingsfile} -l ${logfile}":
		onlyif => "test -e /sbin/hponcfg",
		path =>"/bin:/usr/sbin:/usr/bin",
		refreshonly => true,
		subscribe => File["${settingsfile}"],
		timeout => 0,	

	   }

	# since the template accomodates dhcp and static there is no need to change the template file
         $ilotemplate = "hpilo/iloconfig.erb"
         file { "${settingsfile}":
                   content => template("${ilotemplate}"),
                   ensure => present,
                   owner => root,
                   group => root,
                   mode => 644

                }
      }
               
}
