import os
import sys
import re
import csv
from os import walk

inputdir = sys.argv[1]
outputfile = sys.argv[2]

print inputdir
print outputfile

if inputdir and outputfile:   
 outfile=open(outputfile,"w+")
 filelist = []
 for (dirpath, dirnames, filenames) in walk(inputdir):
  filelist.extend(filenames)
  break

 csvrecord = csv.writer(outfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)

#old version
# headerarray=["Hostname","Version","Interfaces","Interface Shutdown","IP Addresses","Routes","NAT Rules","Syslog Host","Syslog Level","NTP host","SSH enabled","Telnet Enabled","SNMP Enabled","SNMP Trap Config", "Weak Password Methods","DHCP Snooping","Dynamic ARP inspection","Banner","AAA","Exec Timeout","Server Groups"]

 headerarray=["Hostname","Version","Interfaces","Routes","NAT Rules","Syslog Host","Syslog Level","NTP host","SSH enabled","Telnet Enabled","SNMP Enabled","SNMP Trap Config", "Weak Password Methods","Banner","AAA","Exec Timeout","Server Groups"]

 csvrecord.writerow(headerarray)


 for inputfile in filelist:
  hostnameresult=""
  loghostresult=""
  loglevelresult=""
  ntphostresult=""
  sshenabledresult=""
  telnetenabledresult=""
  httpenabledresult=""
  httpsenabledresult=""
  snmpenabledresult=""
  snmptrapresult=""
  passwordmethodsresult=""
  dhcpsnoopingresult=""
  arpinspectionresult=""
  bannerresult=""
  aaaresult=""
  exectimeoutresult=""
  versionresult=""
  ipaddrresult=""
  interfacesresult=""
  servergroupsresult=""
  valuearr=[]
  prevstring=""
  sectionresult=""
  shutdownresult=""
  routesresult=""
  natresult=""
  defaultgatewayresult=""

  print "Reading "+inputfile+":"
  infile=open(inputdir+"/"+inputfile,"rU")
  for string in infile:

   try:
    section=re.search("^([a-z].*)",string)
    sectionresult=section.group(0)
   except:
    pass

   hostname = re.search("^hostname\ (.*)",string)
   if hostname:
#    print "Hostname:"+hostname.group(0)
    hostnameresult=hostname.group(0)

   version = re.search("^ASA Version\ (.*)",string)
   if version:
#    print "Version:"+version.group(0)
    versionresult=version.group(0)

   interfaces = re.search("^interface\ (.*)",string)
   if interfaces:
#    print "Log Host:"+loghost.group(0)

# old version
#    interfacesresult=interfacesresult+interfaces.group(0)+"\n"

# to make shutdown and interface id in single line 
    interfacesresult=interfacesresult+"\n"+interfaces.group(0)


   if re.search("interface", sectionresult):

    shutdown = re.search(" shutdown",string)
    if shutdown:
     interfacesresult=interfacesresult+" shutdown"

# Can be extracted, but makes extraction not readable
    description = re.search("description\ (.*)",string)
    if description:
     interfacesresult=interfacesresult+description.group(0)

    ipaddr = re.search("^\ ip\ address\ (.*)",string)
    if ipaddr:
     interfacesresult=interfacesresult+"\n"+ipaddr.group(0)+"\n"  

    nat = re.search("^ip\ nat\ (.*)",string)
    if nat:
     interfacesresult=interfacesresult+"\n"+nat.group(0)+"\n"


#Reworking interfaces, shutdown, ip addresses, nat

#   shutdown = re.search("shutdown",string)
#   if shutdown:
#     shutdownresult=shutdownresult+sectionresult+"\n"+"shutdown\n"

   route = re.search("^route\ (.*)",string)
   if route:
     routesresult=routesresult+route.group(0)+"\n"

   defaultgateway = re.search("ip\ default-gateway\ (.*)",string)
   if defaultgateway:
     defaultgatewayresult=defaultgatewayresult+defaultgateway.group(0)+"\n"


   ipaddr = re.search("^\ ip\ address\ (.*)",string)
   if ipaddr:
#    print "Log Host:"+loghost.group(0)
    ipaddrresult=ipaddrresult+sectionresult+ipaddr.group(0)+"\n"

   natglobal = re.search("^(nat\ .*)",string)
   if natglobal:
    natresult=natresult+natglobal.group(0)+"\n"

   loghost = re.search("^logging\ host\ (.*)",string)
   if loghost:
#    print "Log Host:"+loghost.group(0)
    loghostresult=loghostresult+loghost.group(0)+"\n"

   loglevel = re.search("^logging\ trap\ (.*)", string)
   if loglevel:
#    print "Log Level:"+loglevel.group(0)
    loglevelresult=loglevel.group(0)

   ntphost = re.search("^ntp\ server\ (.*)",string)
   if ntphost:
#    print "Ntp Host:"+ntphost.group(0)
    ntphostresult=ntphostresult+ntphost.group(0)+"\n"

   sshenabled = re.search("^(ssh.*)",string)
   if sshenabled:
#    print "ssh enabled:"+sshenabled.group(0)
#    sshenabledresult=section.group(0)+sshenabledresult+sshenabled.group(0)+"\n"
    sshenabledresult=sshenabledresult+sshenabled.group(0)+"\n"

   telnetenabled = re.search("^(telnet.*)",string)
   if telnetenabled:
#    print "telnet enabled:"+telnetenabled.group(0)
#    telnetenabledresult=section.group(0)+telnetenabledresult+telnetenabled.group(0)
    telnetenabledresult=telnetenabledresult+telnetenabled.group(0)+"\n"

   httpenabled = re.search("^(http\ server.*)",string)
   if httpenabled:
#    print "http enabled:"+httpenabled.group(0)
    httpenabledresult=httpenabled.group(0)

   httpsenabled = re.search("^(ip\ http\ secure\-server)",string)
   if httpsenabled:
#    print "https enabled:"+httpsenabled.group(0)
    httpsenabledresult=httpsenabled.group(0)
   
   snmpenabled = re.search("snmp\-server\ community\ (.*)",string)
   if snmpenabled:
#    print "snmpenabled:"+snmpenabled.group(0)
    snmpenabledresult=snmpenabledresult+snmpenabled.group(0)+"\n"

   snmptrap = re.search("snmp\-server\ (host.*|enable\ trap.*)",string)
   if snmptrap:
#    print "snmptrap:"+snmptrap.group(0)
    snmptrapresult=snmptrapresult+snmptrap.group(0)+"\n"

   passwordmethods = re.search("(.*password\ .*)",string)
   if passwordmethods:
    try:
     if re.search("encrypted",passwordmethods):
      pass
     else:
      passwordmethodsresult=passwordmethodsresult+passwordmethods.group(0)+"\n"     
    except:
     pass
    

   servergroups = re.search("(.*\-server\ host\ .*)",string)
   if servergroups:
#    print "servergroupsresult:"+servergroups.group(0)
    servergroupsresult=servergroupsresult+servergroups.group(0)+"\n"


   dhcpsnooping = re.search("^ip dhcp snooping (.*)",string)
   if dhcpsnooping:
#    print "dhcp snooping:"+dhcpsnooping.group(0)
    dhcpsnoopingresult=dhcpsnoopingresult+dhcpsnooping.group(0)+"\n"

   arpinspection = re.search("^ip arp inspection (.*)",string)
   if arpinspection:
#    print "arp inspection:"+arpinspection.group(0)
    arpinspectionresult=arpinspectionresult+arpinspection.group(0)+"\n"

   banner = re.search("^banner (.*)",string)
   if banner:
#    print "banner:"+banner.group(0)
    bannerresult=bannerresult+banner.group(0)+"\n"

   aaa = re.search("^aaa (.*)",string)
   if aaa:
#    print "aaa:"+aaa.group(0)
    aaaresult=aaaresult+aaa.group(0)+"\n"

   exectimeout = re.search("exec-timeout (.*)",string)
   if exectimeout:
#    print "exec-timeout:"+exectimeout.group(0)
#    exectimeoutresult=section.group(0)+exectimeoutresult+exectimeout.group(0)+"\n"
    exectimeoutresult=exectimeoutresult+exectimeout.group(0)+"\n"

  infile.close

#old version
#  valuearr=[hostnameresult , versionresult, interfacesresult, shutdownresult, ipaddrresult, routesresult, natresult, loghostresult ,loglevelresult ,ntphostresult ,sshenabledresult ,telnetenabledresult ,snmpenabledresult ,snmptrapresult ,passwordmethodsresult ,dhcpsnoopingresult , arpinspectionresult, bannerresult, aaaresult, exectimeoutresult,servergroupsresult]

  valuearr=[hostnameresult , versionresult, interfacesresult, routesresult, natresult, loghostresult ,loglevelresult ,ntphostresult ,sshenabledresult ,telnetenabledresult ,snmpenabledresult ,snmptrapresult ,passwordmethodsresult ,bannerresult, aaaresult, exectimeoutresult,servergroupsresult]


  csvrecord.writerow(valuearr)
  

# closing report
 outfile.close

else:
 print "Syntax: ios-analyse.py <input-config-directory> <output-report.csv>"
