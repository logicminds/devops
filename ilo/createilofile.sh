#!/bin/bash

# Author: Corey Osman
# Date: 1-26-2010
# This script will create the xml file for each server and set the ilo name, admin
# using the hponcfg utility.  This must be run on each server
# Whats nice about this script is that you don't need the ilo password that is a afixed to the system

# Notes:
# - Different versions of ilo firmware use different RIBCL Versions and cannot parse newer code with older firmware.  If your system
# Is really old you may need to update the ilo firmware first and see what XML config commands are supported.
# The easiest way to start is to export your current ilo config  using "hponfig -w iloconfig.xml"


HOST=`hostname -s`
cat > /root/setupilo.xml << EOF


# You don't need to change the Login info in the tag since its ignored
<RIBCL VERSION="2.0">
  <LOGIN USER_LOGIN="adminname" PASSWORD="password">
    <SERVER_INFO MODE="write">
        <SERVER_NAME value ="${HOST}"/>
    </SERVER_INFO>
  <RIB_INFO MODE="write">
    <MOD_NETWORK_SETTINGS>
      <REG_DDNS_SERVER value="Yes"/>
      <DHCP_DOMAIN_NAME value="Yes"/>
      <DHCP_ENABLE value="Yes"/>
      <DNS_NAME value="ilo-${HOST}"/>
      <DHCP_GATEWAY value="Yes"/>
      <DHCP_DNS_SERVER value="Yes"/>
      <DHCP_WINS_SERVER value="Yes"/>
      <DHCP_STATIC_ROUTE value="Yes"/>
    </MOD_NETWORK_SETTINGS>
  </RIB_INFO>
  <USER_INFO MODE="write">
    <ADD_USER 
      USER_NAME="User" 
      USER_LOGIN="admin" 
      PASSWORD="anypasswordyouwant">
      <ADMIN_PRIV value ="Y"/>
      <REMOTE_CONS_PRIV value ="Y"/>
      <RESET_SERVER_PRIV value ="Y"/>
      <VIRTUAL_MEDIA_PRIV value ="Y"/>
      <CONFIG_ILO_PRIV value="Yes"/>
    </ADD_USER>
  </USER_INFO>
  </LOGIN>
</RIBCL>

EOF
# This is assuming you have installed the hponfig tool from the PSP
hponcfg -f /root/setupilo.xml -l /root/setupilo.log


