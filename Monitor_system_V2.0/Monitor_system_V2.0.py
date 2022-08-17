import requests
import json
import os
import schedule
from module import cmd,initial,web_crawer,get_vessel_list,hx200,videosoft
from NOC import NOC
from account import login
from url import url,hx200_url
from pyfiglet import Figlet
import threading
import time
while True:
    get_initial_data=initial.Initial()
    #print(get_initial_data)
    #------------------------------------
    noc=get_initial_data[0]
    nms_url=get_initial_data[1]
    dncc_url=get_initial_data[2]
    videosoft_url=get_initial_data[3]
    #------------------------------------
    videosoft_login_data=get_initial_data[4]
    videosoft_login_account=videosoft_login_data[0]   
    videosoft_login_password=videosoft_login_data[1]
    #------------------------------------
    print("Initial done!!")
    print("--------->>")
    nmss_data=get_vessel_list.NMSS(nms_url)
    td_array=[]
    nms_esn_array=[]
    nms_vessel_array=[]
    nms_noc_array=[]
    for td in nmss_data:
        td_clear=str(td.text).strip()
        #print(td_clear)
        td_array.append(td_clear)

    for pv0_esn in range(1,len(td_array)-1,5):
        nms_esn_array.append(td_array[pv0_esn])

    for pv0_vessel in range(2,len(td_array)-1,5):
        nms_vessel_array.append(td_array[pv0_vessel])

    for pv0_noc in range(3,len(td_array)-1,5):
        nms_noc_array.append(td_array[pv0_noc])
    total_vessel_num=len(nms_esn_array)



    print("-----------------------------")
    count=0
    get_json_from_dncc=get_vessel_list.DNCC(noc)
    print(f"get json : {get_json_from_dncc}")
    
    noc_dncc_vessel_array=get_json_from_dncc[0]
    noc_dncc_esn_array=get_json_from_dncc[1]
    noc_dncc_noc_array=get_json_from_dncc[2]
    noc_dncc_ip_array=get_json_from_dncc[3]

    noc_nms_esn_array=[]
    noc_nms_vessel_array=[]
    noc_nms_noc_array=[]

    for nms_esn,nms_vessel,nms_noc in zip(nms_esn_array,nms_vessel_array,nms_noc_array):
    
        if str(nms_noc)==str(noc):
            #print(f"esn : {nms_esn}")
            #print(f"vessel : {nms_vessel}")
            #print(f"noc : {nms_noc}")
            noc_nms_esn_array.append(nms_esn)
            noc_nms_vessel_array.append(nms_vessel)
            noc_nms_noc_array.append(nms_noc)
            #print("---------------------------")
            count=count+1
    
    final_vessel_array=[]
    final_esn_array=[]
    final_beam_array=[]
    final_ip_array=[]

    for nms_esn,nms_vessel,nms_noc in zip(noc_nms_esn_array,noc_nms_vessel_array,noc_nms_noc_array):
        for dncc_esn,dncc_vessel,dncc_noc,dncc_ip in zip(noc_dncc_esn_array,noc_dncc_vessel_array,noc_dncc_noc_array,noc_dncc_ip_array):
            if (nms_esn==dncc_esn) and (str(nms_noc) in str(dncc_noc)):
                print(f"vessel : {nms_vessel}")
                print(f"esn : {nms_esn}")
                print(f"beam : {dncc_noc}")
                print(f"lan2_ip : {dncc_ip}")
                final_vessel_array.append(nms_vessel)
                final_esn_array.append(nms_esn)
                final_beam_array.append(dncc_noc)
                final_ip_array.append(dncc_ip)
                print("----------------------------")
            elif (nms_esn==dncc_esn) and (str(nms_noc) not in str(dncc_noc)):
                print(f"vessel : {nms_vessel}")
                print(f"esn : {nms_esn}")
                print(f"beam : {nms_noc}")
                print(f"lan2_ip : {dncc_ip}")
                final_vessel_array.append(nms_vessel)
                final_esn_array.append(nms_esn)
                final_beam_array.append(nms_noc)
                final_ip_array.append(dncc_ip)
                print("----------------------------")
    vessel_online_status_array=[]
    for video_vessel_name in final_vessel_array:
        status=videosoft.online_status(video_vessel_name)
        vessel_online_status_array.append(status)
    thread_list=[]
    for final_vessel,final_esn,final_beam,final_ip,videosoft_status in zip(final_vessel_array,final_esn_array,final_beam_array,final_ip_array,vessel_online_status_array):
        #try:
        print(final_ip)
        t=threading.Thread(target=hx200.GetHx200_info, args=(str(final_ip),str(final_vessel),str(final_esn),str(final_beam),str(videosoft_status)))
        thread_list.append(t)
        t.start()
        #t.join()
        time.sleep(1)
        #except Exception as e:
            #print(e)
    #for i in thread_list:
     #   i.join()
    print(f"total_vessel_num : {total_vessel_num}")
    print(f"in {noc} NOC num : {count}")
    print("---------------------------------------------------")
    print("Threading--->")
    time.sleep(550)
    