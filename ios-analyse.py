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

 headerarray=["Hostname","Version","IP Addresses","Syslog Host","Syslog Level","NTP host","SSH enabled","Telnet Enabled","SNMP Enabled","SNMP Trap Config", "Password Methods","DHCP Snooping","Dynamic ARP inspection","Banner","AAA","Exec Timeout"]

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
  valuearr=[]
  prevstring=""

  print "Reading "+inputfile+":"
  infile=open(inputdir+"/"+inputfile,"rU")
  for string in infile:

   section=re.search("^([a-z].*)",string)

   hostname = re.search("^hostname\ (.*)",string)
   if hostname:
#    print "Hostname:"+hostname.group(0)
    hostnameresult=hostname.group(0)

   version = re.search("^version\ (.*)",string)
   if version:
#    print "Version:"+version.group(0)
    versionresult=version.group(0)

   ipaddr = re.search("^\ ip\ address\ (.*)",string)
   if ipaddr:
#    print "Log Host:"+loghost.group(0)
    ipaddrresult=ipaddrresult+ipaddr.group(0)+"\n"

   loghost = re.search("^logging\ (1.*)|^logging\ host\ (1.*)",string)
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

   sshenabled = re.search("transport\ input.*(ssh)",string)
   if sshenabled:
#    print "ssh enabled:"+sshenabled.group(0)
#    sshenabledresult=section.group(0)+sshenabledresult+sshenabled.group(0)+"\n"
    sshenabledresult=sshenabledresult+sshenabled.group(0)+"\n"

   telnetenabled = re.search("transport\ input\ (telnet)",string)
   if telnetenabled:
#    print "telnet enabled:"+telnetenabled.group(0)
#    telnetenabledresult=section.group(0)+telnetenabledresult+telnetenabled.group(0)
    telnetenabledresult=telnetenabledresult+telnetenabled.group(0)

   httpenabled = re.search("^(ip\ http\ server)",string)
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

   passwordmethods = re.search("(.*password\ .)",string)
   if passwordmethods:
#    print "passwordmethods:"+passwordmethods.group(0)
    passwordmethodsresult=passwordmethodsresult+passwordmethods.group(0)+"\n"

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

  valuearr=[hostnameresult , versionresult, ipaddrresult,  loghostresult ,loglevelresult ,ntphostresult ,sshenabledresult ,telnetenabledresult ,snmpenabledresult ,snmptrapresult ,passwordmethodsresult ,dhcpsnoopingresult , arpinspectionresult, bannerresult, aaaresult, exectimeoutresult]

  csvrecord.writerow(valuearr)
  

# closing report
 outfile.close

else:
 print "Syntax: ios-analyse.py <input-config-directory> <output-report.csv>"
