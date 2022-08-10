import requests
import json
import os
import schedule
from module import cmd,initial,web_crawer,get_vessel_list
from NOC import NOC
from account import login
from url import url
from pyfiglet import Figlet

while True:
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
    td_array=[]
    esn_array=[]
    vessel_array=[]
    noc_array=[]
    for td in nmss_data:
        td_clear=str(td.text).strip()
        #print(td_clear)
        td_array.append(td_clear)

    for pv0_esn in range(1,len(td_array)-1,5):
        esn_array.append(td_array[pv0_esn])

    for pv0_vessel in range(2,len(td_array)-1,5):
        vessel_array.append(td_array[pv0_vessel])

    for pv0_noc in range(3,len(td_array)-1,5):
        noc_array.append(td_array[pv0_noc])
    total_vessel_num=len(esn_array)

    print("-----------------------------")
    count=0
    for pv_esn,pv_vessel,pv_noc in zip(esn_array,vessel_array,noc_array):
    
        if str(pv_noc)==str(noc):
            print(f"esn : {pv_esn}")
            print(f"vessel : {pv_vessel}")
            print(f"noc : {pv_noc}")
            print("---------------------------")
            count=count+1
    print(f"total_vessel_num : {total_vessel_num}")
    print(f"in {noc} NOC num : {count}")
