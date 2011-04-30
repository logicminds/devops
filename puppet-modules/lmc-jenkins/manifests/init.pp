# Class: jenkins
#
# This module manages jenkins and installs the jenkins yum repo for future updates
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
class jenkins{
    yumrepo{"jenkinsrepo":
	baseurl => "http://pkg.jenkins-ci.org/redhat/",
	gpgcheck => '1',
	descr => "jenkins",
	enabled => '1',
	gpgkey => "http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key",
    }
    package{"jenkins":
	ensure => present,
	provider => yum,
        require => Yumrepo['jenkinsrepo'],
	
    }
    service{"jenkinsservice":
	ensure => running,
	enable => true,
	hasrestart => true,
	hasstatus => true,
	name => "jenkins",
	require => Package['jenkins'],
    }
}


