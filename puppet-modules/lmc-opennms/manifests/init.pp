# Class: opennms
#
# This module manages opennms
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
class opennms {
     if $listdistid == "CentOS" {
     	$listdistid = "rhel"
     }
     $oscode = "${listdistid}${lsbmajdistrelease}"
     $oscode = inline_template("<%= $oscode.downcase! %>")

     $opennmssource = "http://yum.opennms.org/repofiles/opennms-repo-unstable-${oscode}.noarch.rpm"
     package{"opennmsrepo":
	ensure => present,
	source => ${opennmssource},
	provider => yum,
     }
     package{"opennms":
	ensure => present,
	provider => yum,
        required => [[Package["opennmsrepo"], Package["iplike"], Package["jdk"], Service["postgresql"]],
     }
     package{ "iplike":
  	ensure => present,
	provider => yum,
        require => [Package["opennmsrepo"], Exec["createdb"]],
     }
     package{ "jdk":
  	ensure => present,
	provider => yum,
        require => [Package["opennmsrepo"]],
     }
    
     package{"postgresql-server":
	ensure => present,
	provider => yum,
	require => Package["opennmsrepo"],
     }
     service{"postgresql":
	enable => true,
	ensure => running,
	hasstatus => true,
	hasrestart => true,
	pattern => "postgresql",
	require => Package["postgresql-server"]
     }
     service{"opennms":
	enable => true,
	ensure => running,
	hasstatus => true,
	hasrestart => true,
	#pattern => "opennms",
     }
     file{"/etc/pg_hba.conf":
	ensure => present,
	source => "puppet:///modules/opennms/pg_hba.conf",
	owner => root,
	group => root,
	mode => 644,
	require => Package["postgresql-server"],
	notify => Service["postgresql"],
     }
     file{"/etc/pg_hba.conf":
	ensure => present,
	source => "puppet:///modules/opennms/pg_hba.conf",
	owner => root,
	group => root,
	mode => 644,
	require => Package["postgresql-server"],
	notify => Service["postgresql"],
     }
     #exec{"initdb":
#	command => "/bin/su -c 'service postgresql initdb'",
#	creates => "/etc/postgresql_initdb_donotremove.txt",
#     }
     exec{"createdb":
	command => "/bin/sudo -u postgres createdb -U postgres -E UNICODE opennms",
	creates => "/etc/opennms_createdb_donotremove.txt",
	require => Service["postgresql"],
     }
     exec{"iplike":
	command => "/bin/su -c /usr/sbin/install_iplike.sh",
	creates => "/etc/opennms_iplike_donotremove.txt",
	require => [Service["postgresql"]Package["iplike"]],
     }
     exec{"setup_opennms":
	command => "/bin/su -c '/opt/opennms/bin/install -dis'",
	creates => "/etc/opennms_installed_donotremove.txt",
	require => Exec["iplike"],
     }
     exec{"findjava":
	command => "/bin/su -c '/opt/opennms/bin/runjava -s'",
	creates => "/etc/opennms_findjava_donotremove.txt",
     }
     # add to bottom of /etc/sysconfig/iptables
     # -A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 8980 -j ACCEPT 
     # -A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp -s 12.34.56.00/24 --dport 8980 -j ACCEPT 
     # su -c '/sbin/service iptables restart' 
// TODO:
     #Additionally you will want to be certain that that the max number of
     # of simultaneous connections is configured to be greater than
     # c3p0.maxPoolSize in $OPENNMS_HOME/etc/c3p0.properties (50 by default) +10.
     #max_connections = 60
     # will probably want to create a template for postgresql.conf
	

}
