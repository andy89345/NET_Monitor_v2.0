from NOC import NOC
from account import login
from url import url
from pyfiglet import Figlet
import datetime
import time
import urllib.request as req
import json
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import threading
import requests
class cmd:
    def Cmd(ip):
        cmdstr1="ping -n 5 "
        cmdstr2=cmdstr1+ip
        result = os.popen(cmdstr2)
        context = result.read()
        print(context)  
        if ("Min" in context) and ("specified" in context) and ("specified" in name):
            online=1
        else:
            online=0
        return online

class initial:
    def Initial():
        f=Figlet(width=2000)
        print(f.renderText("Ping-Monitor-System"))
        print("-----------------------")
        print("Author : Andy Lin     |")
        print("Version : 2.0         |")
        print("-----------------------\n\n\n")
        result=[]
        print("Initial.........")
        print("=================================================================================================")
        #=================================================================================================
        print("Get NOC")
        NOC_dict=json.dumps(NOC.noc)
        NOC_json=json.loads(NOC_dict)
        GET_NOC=NOC_json["TW"]  #Get the NOC
        #print(f"NOC : {GET_NOC}")
        #=================================================================================================
        print("Get total url")
        URL_dict=json.dumps(url.url_array)
        URL_json=json.loads(URL_dict)
        GET_NMS_URL=URL_json["SE_NMS_url"] #Get NMS_URL from se
        GET_DNCC_URL=URL_json["SE_DNCC_url"] #Get DNCC_URL from se
        GET_VIDEOSOFT_URL=URL_json["Videosoft_Bridge_url"] #Get VIDEOSOFT_URL from videosoft bridge
        #print(f"NMS URL : {GET_NMS_URL}")
        #print(f"DNCC URL : {GET_DNCC_URL}")
        #print(f"VIDEOSOFT URL : {GET_VIDEOSOFT_URL}")
        print("=================================================================================================")
        #=================================================================================================
        videosoft_login=login("videosoft","Lung@hwa123")
        videosoft_login_data=[videosoft_login.account,videosoft_login.password]
        result=[GET_NOC,GET_NMS_URL,GET_DNCC_URL,GET_VIDEOSOFT_URL,videosoft_login_data]
        return result
    

class web_crawer:
    def beautiful_soup(url):
        url_html=req.Request(url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"})
        with req.urlopen(url_html) as get_url_html:
            url_html_read=get_url_html.read()
            url_beautiful_data=BeautifulSoup(url_html_read,"html.parser")
        return url_beautiful_data

class get_json:
    def get_json_data(url):
       json_full=requests.get(url)
       json_dump=json.dumps(json_full.text)
       json_load=json.loads(json_dump)
       return json_load


class get_vessel_list:
    def NMSS(url):
        nmss_beautiful=web_crawer.beautiful_soup(url)
        #print(nmss_beautiful)
        get_list=nmss_beautiful.find_all("td")
        return get_list

    def DNCC(noc):
        if noc=="TW":
            input_url_noc="tw"
        elif noc=="US":
            input_url_noc="usa"
        elif noc=="AU":
            input_url_noc="au"
        elif noc=="JP":
            input_url_noc="jp"
        
        url_json=json.dumps(url.url_array)
        real_url_json=json.loads(url_json)
        normal_url=real_url_json["get_dncc_url"]
        full_url=normal_url+input_url_noc
        get_dncc_json=get_json.get_json_data(full_url)


        return get_dncc_json
class Multithread_gogo:
    def __init__(self,esn_array,vessel_array,lan2_ip_array,mng_ip_array):
        self.esn_array=esn_array
        self.vessel_array=vessel_array
        self.lan2_ip_array=lan2_ip_array
        self.mng_ip_array=mng_ip_array
        