# Class: vmware
#
# This module manages vmware tools install and can optionally updated the tools to the latest version
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
class vmware {
   if ($manufacturer == "VMware, Inc."){
    
    yumrepo{"vmware-tools":
        baseurl => 'http://packages.vmware.com/tools/esx/latest/rhel$releasever/$basearch',
        gpgcheck => 1,
        descr => 'VMware Tools for Red Hat Enterprise Linux $releasever $basearch',
        enabled => 1,
        gpgkey => "http://packages.vmware.com/tools/VMWARE-PACKAGING-GPG-KEY.pub",
    }
    package{"vmware-tools":
	# ensure => latest,
        ensure => present,
        provider => yum,
        require => Yumrepo['vmware-tools'],
        
    }

    # run the vmware-config-tools command everytime the tools are updated
    # restart the vmware-tools service everytime the command is run 
#    exec{"/usr/bin/vmware-config-tools.pl -d":
#	require => [Exec["vmware-uninstall-tools.pl"],Package["vmware-tools"]],
#	subscribe => Package["vmware-tools"],
#        notify => Service["vmware-tools"],
#
#
#    }
    exec{"vmware-uninstall-tools.pl":
	onlyif => "test -f /usr/bin/vmware-uninstall-tools.pl",
        path => ["/bin:/usr/bin"],	

    }
    service{"vmware-tools":
        ensure => running,
        enable => true,
        hasrestart => true,
        hasstatus => true,
        pattern => "vmware-tools",
        require => Package['vmware-tools'],
    }
	
   }

}
