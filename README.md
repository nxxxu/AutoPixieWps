# AutoPixieWps
Automated pixieWps python script
Do not attempt to gain access to a router that does not belong to you!.

this script is pretty straight forward.

If you do not get any routers on scan, only the press ctrl+c to cancel
il fix it later, but you can change:
line 32=essid.append (line[84:line.find("\n")]) (change 84 to 83)
and
line 36=lock.append (line[66:68]) (change 66 to 65, and 68 to 67)

change those 3 values and it should work. (it is because different versions or wash gives different output.)
