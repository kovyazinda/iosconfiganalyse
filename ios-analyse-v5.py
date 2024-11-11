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
  print ("Debug: ",filenames)
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
 worksheet.write (0,1,"Version",cell_format_header)
 worksheet.write (0,2,"Interfaces",cell_format_header)
 worksheet.write (0,3,"Routes",cell_format_header)
 worksheet.write (0,4,"IP Default-Gateway",cell_format_header)
 worksheet.write (0,5,"NAT Rules",cell_format_header)
 worksheet.write (0,6,"Syslog Host",cell_format_header)
 worksheet.write (0,7,"Syslog Level",cell_format_header)
 worksheet.write (0,8,"NTP host",cell_format_header)
 worksheet.write (0,9,"SSH enabled",cell_format_header)
 worksheet.write (0,10,"Telnet Enabled",cell_format_header)
 worksheet.write (0,11,"SNMP Enabled",cell_format_header)
 worksheet.write (0,12,"SNMP Trap Config",cell_format_header)
 worksheet.write (0,13,"Weak Password Methods",cell_format_header)
 worksheet.write (0,14,"DHCP Snooping",cell_format_header)
 worksheet.write (0,15,"Dynamic ARP inspection",cell_format_header)
 worksheet.write (0,16,"Banner",cell_format_header)
 worksheet.write (0,17,"AAA",cell_format_header)
 worksheet.write (0,18,"Exec Timeout",cell_format_header)
 worksheet.write (0,19,"Server Groups",cell_format_header)
 worksheet.write (0,20,"Boot system",cell_format_header)

#setting column properties
#width
# Hostname
 worksheet.set_column(0, 0, 30)
# Version
 worksheet.set_column(1, 1, 15)
# Long columns - interfaces, routes, default gateway, nat
 worksheet.set_column(2, 6, 50)
# Long columns - boot system
 worksheet.set_column(20, 20, 50)


# Other columns - set default to 30
 worksheet.set_column(7, 19, 30)


# to start writing to next rown
 rownum=1

#old version
# headerarray=["Hostname","Version","Interfaces","Interface Shutdown","IP Addresses","Routes","NAT Rules","Syslog Host","Syslog Level","NTP host","SSH enabled","Telnet Enabled","SNMP Enabled","SNMP Trap Config", "Weak Password Methods","DHCP Snooping","Dynamic ARP inspection","Banner","AAA","Exec Timeout","Server Groups"]

 headerarray=["Hostname","Version","Interfaces","Routes","IP Default-Gateway","NAT Rules","Syslog Host","Syslog Level","NTP host","SSH enabled","Telnet Enabled","SNMP Enabled","SNMP Trap Config", "Weak Password Methods","DHCP Snooping","Dynamic ARP inspection","Banner","AAA","Exec Timeout","Server Groups"]

# Uncomment to display interfaces in shutdown 
# headerarray=["Hostname","Version","Interfaces","Interfaces in shutdown","Routes","IP Default-Gateway","NAT Rules","Syslog Host","Syslog Level","NTP host","SSH enabled","Telnet Enabled","SNMP Enabled","SNMP Trap Config", "Weak Password Methods","DHCP Snooping","Dynamic ARP inspection","Banner","AAA","Exec Timeout","Server Groups"]


# old csv record
# csvrecord.writerow(headerarray)


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
  bootsystemresult=""

  print ("Reading "+inputfile+":")
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

   version = re.search("^version\ (.*)",string)
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
     interfacesresult=interfacesresult+" "+description.group(0)

    vlan = re.search("switchport\ access\ vlan\ (.*)",string)
    if vlan:
     interfacesresult=interfacesresult+" "+vlan.group(0)


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

   route = re.search("ip\ route\ (.*)",string)
   if route:
     routesresult=routesresult+route.group(0)+"\n"

   defaultgateway = re.search("ip\ default-gateway\ (.*)",string)
   if defaultgateway:
     defaultgatewayresult=defaultgatewayresult+defaultgateway.group(0)+"\n"


   ipaddr = re.search("^\ ip\ address\ (.*)",string)
   if ipaddr:
#    print "Log Host:"+loghost.group(0)
    ipaddrresult=ipaddrresult+sectionresult+ipaddr.group(0)+"\n"

   natglobal = re.search("^ip\ nat\ (.*)",string)
   if natglobal:

    try:
     natresult=natresult+sectionresult+"\n"+natglobal.group(0)+"\n\n"
    except:
     natresult=natresult+natglobal.group(0)+"\n"

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
    sshenabledresult=sshenabledresult+sectionresult+"\n "+sshenabled.group(0)+"\n"

   telnetenabled = re.search("transport\ input\ (telnet)",string)
   if telnetenabled:
#    print "telnet enabled:"+telnetenabled.group(0)
#    telnetenabledresult=section.group(0)+telnetenabledresult+telnetenabled.group(0)
    telnetenabledresult=telnetenabledresult+sectionresult+"\n "+telnetenabled.group(0)

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

   passwordmethods = re.search("(.*password\ 7)",string)
   if passwordmethods:
    if ("ftp" in sectionresult):    
#     print ("passwordmethods:"+passwordmethods.group(0))
     passwordmethodsresult=passwordmethodsresult+passwordmethods.group(0)+"\n"
    else:
#     print ("passwordmethods:"+sectionresult+passwordmethods.group(0))
     passwordmethodsresult=passwordmethodsresult+passwordmethods.group(0)+"\n"

#+passwordmethods.group(0)+"\n"

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

   bootsystem = re.search("boot system (.*)",string)
   if bootsystem:
    bootsystemresult = bootsystemresult+bootsystem.group(0)+"\n"

  infile.close

#old version
#  valuearr=[hostnameresult , versionresult, interfacesresult, shutdownresult, ipaddrresult, routesresult, natresult, loghostresult ,loglevelresult ,ntphostresult ,sshenabledresult ,telnetenabledresult ,snmpenabledresult ,snmptrapresult ,passwordmethodsresult ,dhcpsnoopingresult , arpinspectionresult, bannerresult, aaaresult, exectimeoutresult,servergroupsresult]

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
#  valuearr=[hostnameresult , versionresult, interfacesbriefresult, interfacesshutdownresult, routesresult, defaultgatewayresult, natresult, loghostresult ,loglevelresult ,ntphostresult ,sshenabledresult ,telnetenabledresult ,snmpenabledresult ,snmptrapresult ,passwordmethodsresult ,dhcpsnoopingresult , arpinspectionresult, bannerresult, aaaresult, exectimeoutresult,servergroupsresult]

# output only information about interfaces not in shutdown
  valuearr=[hostnameresult , versionresult, interfacesbriefresult, routesresult, defaultgatewayresult, natresult, loghostresult ,loglevelresult ,ntphostresult ,sshenabledresult ,telnetenabledresult ,snmpenabledresult ,snmptrapresult ,passwordmethodsresult ,dhcpsnoopingresult , arpinspectionresult, bannerresult, aaaresult, exectimeoutresult,servergroupsresult,bootsystemresult]

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
