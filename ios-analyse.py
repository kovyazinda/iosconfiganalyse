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

 headerarray=["Hostname","Version","Interfaces","Routes","IP Default-Gateway","NAT Rules","Syslog Host","Syslog Level","NTP host","SSH enabled","Telnet Enabled","SNMP Enabled","SNMP Trap Config", "Weak Password Methods","DHCP Snooping","Dynamic ARP inspection","Banner","AAA","Exec Timeout","Server Groups"]

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
    hostnameresult=hostname.group(0)

   version = re.search("^version\ (.*)",string)
   if version:
    versionresult=version.group(0)

   interfaces = re.search("^interface\ (.*)",string)
   if interfaces:
    interfacesresult=interfacesresult+"\n"+interfaces.group(0)


   if re.search("interface", sectionresult):

    shutdown = re.search(" shutdown",string)
    if shutdown:
     interfacesresult=interfacesresult+" shutdown"

    description = re.search("description\ (.*)",string)
    if description:
     interfacesresult=interfacesresult+description.group(0)

    ipaddr = re.search("^\ ip\ address\ (.*)",string)
    if ipaddr:
     interfacesresult=interfacesresult+"\n"+ipaddr.group(0)+"\n"  

    nat = re.search("^ip\ nat\ (.*)",string)
    if nat:
     interfacesresult=interfacesresult+"\n"+nat.group(0)+"\n"

   route = re.search("ip\ route\ (.*)",string)
   if route:
     routesresult=routesresult+route.group(0)+"\n"

   defaultgateway = re.search("ip\ default-gateway\ (.*)",string)
   if defaultgateway:
     defaultgatewayresult=defaultgatewayresult+defaultgateway.group(0)+"\n"


   ipaddr = re.search("^\ ip\ address\ (.*)",string)
   if ipaddr:
    ipaddrresult=ipaddrresult+sectionresult+ipaddr.group(0)+"\n"

   natglobal = re.search("^ip\ nat\ (.*)",string)
   if natglobal:

    try:
     natresult=natresult+sectionresult+"\n"+nat.group(0)+"\n\n"
    except:
     natresult=natresult+nat.group(0)+"\n"

   loghost = re.search("^logging\ (1.*)|^logging\ host\ (1.*)",string)
   if loghost:
    loghostresult=loghostresult+loghost.group(0)+"\n"

   loglevel = re.search("^logging\ trap\ (.*)", string)
   if loglevel:
    loglevelresult=loglevel.group(0)

   ntphost = re.search("^ntp\ server\ (.*)",string)
   if ntphost:
    ntphostresult=ntphostresult+ntphost.group(0)+"\n"

   sshenabled = re.search("transport\ input.*(ssh)",string)
   if sshenabled:
    sshenabledresult=sshenabledresult+sectionresult+"\n "+sshenabled.group(0)+"\n"

   telnetenabled = re.search("transport\ input\ (telnet)",string)
   if telnetenabled:
    telnetenabledresult=telnetenabledresult+sectionresult+"\n "+telnetenabled.group(0)

   httpenabled = re.search("^(ip\ http\ server)",string)
   if httpenabled:
    httpenabledresult=httpenabled.group(0)

   httpsenabled = re.search("^(ip\ http\ secure\-server)",string)
   if httpsenabled:
    httpsenabledresult=httpsenabled.group(0)
   
   snmpenabled = re.search("snmp\-server\ community\ (.*)",string)
   if snmpenabled:
    snmpenabledresult=snmpenabledresult+snmpenabled.group(0)+"\n"

   snmptrap = re.search("snmp\-server\ (host.*|enable\ trap.*)",string)
   if snmptrap:
    snmptrapresult=snmptrapresult+snmptrap.group(0)+"\n"

   passwordmethods = re.search("(.*password\ .*)",string)
   if passwordmethods:
    passwordmethodsresult=passwordmethodsresult+sectionresult+"\n"+passwordmethods.group(0)+"\n"

   servergroups = re.search("(.*\-server\ host\ .*)",string)
   if servergroups:
    servergroupsresult=servergroupsresult+servergroups.group(0)+"\n"


   dhcpsnooping = re.search("^ip dhcp snooping (.*)",string)
   if dhcpsnooping:
    dhcpsnoopingresult=dhcpsnoopingresult+dhcpsnooping.group(0)+"\n"

   arpinspection = re.search("^ip arp inspection (.*)",string)
   if arpinspection:
    arpinspectionresult=arpinspectionresult+arpinspection.group(0)+"\n"

   banner = re.search("^banner (.*)",string)
   if banner:
    bannerresult=bannerresult+banner.group(0)+"\n"

   aaa = re.search("^aaa (.*)",string)
   if aaa:
    aaaresult=aaaresult+aaa.group(0)+"\n"

   exectimeout = re.search("exec-timeout (.*)",string)
   if exectimeout:
    exectimeoutresult=exectimeoutresult+exectimeout.group(0)+"\n"

  infile.close

  valuearr=[hostnameresult , versionresult, interfacesresult, routesresult, defaultgatewayresult, natresult, loghostresult ,loglevelresult ,ntphostresult ,sshenabledresult ,telnetenabledresult ,snmpenabledresult ,snmptrapresult ,passwordmethodsresult ,dhcpsnoopingresult , arpinspectionresult, bannerresult, aaaresult, exectimeoutresult,servergroupsresult]


  csvrecord.writerow(valuearr)
  

# closing report
 outfile.close

else:
 print "Syntax: ios-analyse.py <input-config-directory> <output-report.csv>"
