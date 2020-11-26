import os
import sys
import re

#import csv

from os import walk
import xlsxwriter

inputdir = sys.argv[1]
outputfile = sys.argv[2]

print (inputdir)
print (outputfile)

if inputdir and outputfile:   
# old csv export
# outfile=open(outputfile,"w+")
 filelist = []
 for (dirpath, dirnames, filenames) in walk(inputdir):
  filelist.extend(filenames)
  break
# old csv export
# csvrecord = csv.writer(outfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)

# Writing to excel
 workbook = xlsxwriter.Workbook(outputfile)
 worksheet = workbook.add_worksheet()

#apply default row height
 worksheet.set_default_row(70)

#applying cell format
 cell_format_header = workbook.add_format({'bold': True, 'font_color': 'black'})
 cell_format_normal = workbook.add_format({'bold': False, 'font_color': 'black', 'text_wrap' : True})
 cell_format_bad = workbook.add_format({'bold': False, 'font_color': 'black', 'bg_color': 'red','text_wrap' : True})

# writing column headers
 worksheet.write (0,0,"Hostname",cell_format_header)
 worksheet.write (0,1,"Model",cell_format_header)
 worksheet.write (0,2,"Interfaces",cell_format_header)
 worksheet.write (0,3,"IP Address",cell_format_header)
 worksheet.write (0,4,"IP Default-Gateway",cell_format_header)
 worksheet.write (0,5,"TFTP Server",cell_format_header)
 worksheet.write (0,6,"Syslog Host",cell_format_header)

 worksheet.write (0,7,"NTP host",cell_format_header)

 worksheet.write (0,8,"Telnet Enabled",cell_format_header)
 worksheet.write (0,9,"HTTP enabled",cell_format_header)
 worksheet.write (0,10,"SNMP Enabled",cell_format_header)
 worksheet.write (0,11,"SNMP Trap Config",cell_format_header)
 worksheet.write (0,12,"VLAN",cell_format_header)
 worksheet.write (0,13,"Exec Timeout",cell_format_header)
 worksheet.write (0,14,"ACL",cell_format_header)


#setting column properties
#width
# Hostname
 worksheet.set_column(0, 0, 30)
# Model
 worksheet.set_column(1, 1, 30)
# Long columns - interfaces, ip address, default gateway, nat
 worksheet.set_column(2, 4, 50)

# Other columns - set default to 30
 worksheet.set_column(5, 17, 30)


# to start writing to next rown
 rownum=1



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
  vlanresult=""
  arpinspectionresult=""
  aclresult=""
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
  tftpresult=""
  defaultgatewayresult=""
  bootsystemresult=""

  print ("Reading "+inputfile+":")
  infile=open(inputdir+"/"+inputfile,"rU")
  for string in infile:
   
   try:
    section=re.search("^([a-z].*)",string)
    sectionresult=section.group(0)
   except:
    pass

   hostname = re.search("^SwitchName\t\t(.*)",string)
   if hostname:
# debug
    print ("Hostname:"+hostname.group(0))
    hostnameresult=hostname.group(0)

   version = re.search("^ModelName(.*)",string)
   if version:
    versionresult=version.group(0)

   interfaces = re.search("^Port_._(.*)",string)
   if interfaces:
#    print ("Interfaces:"+interfaces.group(0))

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
     interfacesresult=interfacesresult+" "+description.group(0)

    
   ipaddr = re.search("^IPAddress(.*)|^Netmask(.*)",string)
   if ipaddr:
    ipaddrresult=ipaddrresult+"\n"+ipaddr.group(0)+"\n"  



#Reworking interfaces, shutdown, ip addresses, nat

#   shutdown = re.search("shutdown",string)
#   if shutdown:
#     shutdownresult=shutdownresult+sectionresult+"\n"+"shutdown\n"

   route = re.search("ip\ route\ (.*)",string)
   if route:
     routesresult=routesresult+route.group(0)+"\n"

   defaultgateway = re.search("^Gateway(.*)",string)
   if defaultgateway:
     defaultgatewayresult=defaultgatewayresult+defaultgateway.group(0)+"\n"


   ipaddr = re.search("^\ ip\ address\ (.*)",string)
   if ipaddr:
#    print "Log Host:"+loghost.group(0)
    ipaddrresult=ipaddrresult+sectionresult+ipaddr.group(0)+"\n"

   tftp = re.search("^Tftp(.*)",string)
   if tftp:
    tftpresult=tftpresult+tftp.group(0)+"\n"


   loghost = re.search("^SYSLOG(.*)",string)
   if loghost:
#    print "Log Host:"+loghost.group(0)
    loghostresult=loghostresult+loghost.group(0)+"\n"

   loglevel = re.search("^logging\ trap\ (.*)", string)
   if loglevel:
#    print "Log Level:"+loglevel.group(0)
    loglevelresult=loglevel.group(0)

   ntphost = re.search("^1stTimeSrv(.*)|^2ndTimeSrv(.*)",string)
   if ntphost:
#    print "Ntp Host:"+ntphost.group(0)
    ntphostresult=ntphostresult+ntphost.group(0)+"\n"

   sshenabled = re.search("transport\ input.*(ssh)",string)
   if sshenabled:
#    print "ssh enabled:"+sshenabled.group(0)
#    sshenabledresult=section.group(0)+sshenabledresult+sshenabled.group(0)+"\n"
    sshenabledresult=sshenabledresult+sectionresult+"\n "+sshenabled.group(0)+"\n"

   telnetenabled = re.search("^TelnetConsole\t(.*)",string)
   if telnetenabled:
#    print "telnet enabled:"+telnetenabled.group(0)
#    telnetenabledresult=section.group(0)+telnetenabledresult+telnetenabled.group(0)
    telnetenabledresult=telnetenabledresult+sectionresult+"\n "+telnetenabled.group(0)

   httpenabled = re.search("^WebConfig\t(.*)",string)
   if httpenabled:
#    print "http enabled:"+httpenabled.group(0)
    httpenabledresult=httpenabled.group(0)

   httpsenabled = re.search("^(ip\ http\ secure\-server)",string)
   if httpsenabled:
#    print "https enabled:"+httpsenabled.group(0)
    httpsenabledresult=httpsenabled.group(0)
   
   snmpenabled = re.search("^SNMPVERSION(.*)|V1_V2c_RCommunity(.*)|V1_V2c_RWCommunity(.*)",string)
   if snmpenabled:
#    print "snmpenabled:"+snmpenabled.group(0)
    snmpenabledresult=snmpenabledresult+snmpenabled.group(0)+"\n"

   snmptrap = re.search("^TRAP_(.*)",string)
   if snmptrap:
#    print "snmptrap:"+snmptrap.group(0)
    snmptrapresult=snmptrapresult+snmptrap.group(0)+"\n"

   passwordmethods = re.search("(.*password\ .*)",string)
   if passwordmethods:
#    print "passwordmethods:"+passwordmethods.group(0)
    passwordmethodsresult=passwordmethodsresult+sectionresult+"\n"+passwordmethods.group(0)+"\n"

   servergroups = re.search("(.*\-server\ host\ .*)",string)
   if servergroups:
#    print "servergroupsresult:"+servergroups.group(0)
    servergroupsresult=servergroupsresult+servergroups.group(0)+"\n"


   vlan = re.search("^VLAN(.*)|^GVRP(.*)",string)
   if vlan:
#    print "dhcp snooping:"+vlan.group(0)
    vlanresult=vlanresult+vlan.group(0)+"\n"

   arpinspection = re.search("^ip arp inspection (.*)",string)
   if arpinspection:
#    print "arp inspection:"+arpinspection.group(0)
    arpinspectionresult=arpinspectionresult+arpinspection.group(0)+"\n"

   acl = re.search("^AccessIp(.*)",string)
   if acl:
#    print "acl:"+acl.group(0)
    aclresult=aclresult+acl.group(0)+"\n"

   aaa = re.search("^aaa (.*)",string)
   if aaa:
#    print "aaa:"+aaa.group(0)
    aaaresult=aaaresult+aaa.group(0)+"\n"

   exectimeout = re.search("^AgeTime\t(.*)|^WebTimeout(.*)",string)
   if exectimeout:
#    print "exec-timeout:"+exectimeout.group(0)
#    exectimeoutresult=section.group(0)+exectimeoutresult+exectimeout.group(0)+"\n"
    exectimeoutresult=exectimeoutresult+exectimeout.group(0)+"\n"

   bootsystem = re.search("boot system (.*)",string)
   if bootsystem:
    bootsystemresult = bootsystemresult+bootsystem.group(0)+"\n"

  infile.close

#old version
#  valuearr=[hostnameresult , versionresult, interfacesresult, shutdownresult, ipaddrresult, routesresult, natresult, loghostresult ,loglevelresult ,ntphostresult ,sshenabledresult ,telnetenabledresult ,snmpenabledresult ,snmptrapresult ,passwordmethodsresult ,vlanresult , arpinspectionresult, aclresult, aaaresult, exectimeoutresult,servergroupsresult]

  interfacesbriefresult=""
  interfacesshutdownresult=""

#remove records for interfaces in shutdown:
  interfacelist=interfacesresult.split("\n")
  for interfaceline in interfacelist:
   if "shutdown" not in interfaceline:
#    print (interfaceline)
    interfacesbriefresult=interfacesbriefresult+interfaceline+"\n"
   else: 
    interfacesshutdownresult=interfacesshutdownresult+interfaceline+"\n"

# full interfaces information output 
#  valuearr=[hostnameresult , versionresult, interfacesbriefresult, interfacesshutdownresult, routesresult, defaultgatewayresult, natresult, loghostresult ,loglevelresult ,ntphostresult ,sshenabledresult ,telnetenabledresult ,snmpenabledresult ,snmptrapresult ,passwordmethodsresult ,vlanresult , arpinspectionresult, aclresult, aaaresult, exectimeoutresult,servergroupsresult]

# output only information about interfaces not in shutdown
  valuearr=[hostnameresult , versionresult, interfacesbriefresult, ipaddrresult, defaultgatewayresult, tftpresult, loghostresult, ntphostresult ,telnetenabledresult ,httpenabledresult,snmpenabledresult ,snmptrapresult ,vlanresult , exectimeoutresult, aclresult]

# old csv record
#  csvrecord.writerow(valuearr)

# setting row optimal height
# not working
#  worksheet.set_default_row(rownum) 
#  worksheet.set_row(rownum,20)
 
  colnum=0
  for colvalue in valuearr:
   worksheet.write (rownum,colnum,colvalue,cell_format_normal)  
   colnum=colnum+1  

# incrementing row
  rownum=rownum+1


 
 workbook.close()

# old csv closing report
# outfile.close

else:
 print ("Syntax: ios-analyse.py <input-config-directory> <output-report.xlsx>")
