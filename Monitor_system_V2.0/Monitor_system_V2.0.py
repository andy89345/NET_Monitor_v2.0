import requests
import json
import os
from module import cmd,initial,web_crawer,get_vessel_list
from NOC import NOC
from account import login
from url import url
from pyfiglet import Figlet


get_initial_data=initial.Initial()
#print(get_initial_data)
#------------------------------------
noc=get_initial_data[0]
nms_url=get_initial_data[1]
dncc_url=get_initial_data[2]
videosoft_url=get_initial_data[3]
#------------------------------------
login_data=get_initial_data[4]
login_account=login_data[0]
login_password=login_data[1]
#------------------------------------
print("Initial done!!")
print("--------->>")
nmss_data=get_vessel_list.NMSS(nms_url)
for td in nmss_data:
    td_clear=str(td.text).strip()
    print(td_clear)
