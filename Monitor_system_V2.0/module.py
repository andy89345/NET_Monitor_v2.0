from NOC import NOC
from account import login
from url import url,hx200_url
from pyfiglet import Figlet
import datetime
import time
import urllib.request as req
import json
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import threading
import requests
import os
import pyodbc
def split_list(array,n):
    for i in range(0,len(array),n):
        yield(array[i:i+n])

class cmd:
    def Cmd(ip):
        cmdstr1="ping -n 5 "
        cmdstr2=cmdstr1+ip
        result = os.popen(cmdstr2)
        context = result.read()
        print(context)  
        if (("Min" in context) or ("最小值" in context)) and (("Average" in context) or ("平均" in context)):
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
        GET_NOC=NOC_json["AU"]  #Get the NOC
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
        print(url_html)
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
        vessel_name_array=[]
        vessel_esn_array=[]
        vessel_beam_array=[]
        vessel_lan2_array=[]
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
        get_dncc_json=get_dncc_json[2:len(get_dncc_json)-2]
        split_get_dncc_json=str(get_dncc_json).split("},{")
        for x in split_get_dncc_json:
            #print(x)
            spl_x=str(x).split(",")
            #print(spl_x)
            vessel_name_in_list=str(spl_x[0]).replace('"',"")
            vessel_esn_in_list=str(spl_x[1])
            vessel_beam_in_list=str(spl_x[2]).replace('"',"")
            vessel_lan2_in_list=str(spl_x[3]).replace('"',"")

            vessel_name_real=vessel_name_in_list.split(":")
            vessel_name_final=vessel_name_real[1]
            vessel_name_array.append(vessel_name_final)

            vessel_esn_real=vessel_esn_in_list.split(":")
            vessel_esn_final=vessel_esn_real[1]
            vessel_esn_array.append(vessel_esn_final)

            vessel_beam_real=vessel_beam_in_list.split(":")
            vessel_beam_final=vessel_beam_real[1]
            vessel_beam_array.append(vessel_beam_final)

            vessel_lan2_real=vessel_lan2_in_list.split(":")
            vessel_lan2_final=vessel_lan2_real[1]
            vessel_lan2_array.append(vessel_lan2_final)

        result_array=[vessel_name_array,vessel_esn_array,vessel_beam_array,vessel_lan2_array]
        return result_array

class hx200:
    
    def GetHx200_info(lan2ip,vessel,esn,beam):
        print("-----------------------------------------------")
        online_status=cmd.Cmd(lan2ip)
        print(f"vessel : {vessel}")
        if online_status==1:
            try:
                hx200_gps_url=hx200_url.hx200_gps_url(lan2ip)
                hx200_sql_url=hx200_url.hx200_spf_url(lan2ip)
                gps=requests.get(hx200_gps_url)
                sqf=requests.get(hx200_sql_url)
                if(gps.status_code==requests.codes.ok):
                    gps_soup=BeautifulSoup(gps.text,"html.parser")
                    total_data_gps=gps_soup.pre.text
                    latitude="GPS latitude in radians"
                    gps_data=total_data_gps[total_data_gps.index(latitude):]
                    print("The GPS latitude in radians is:")
                    print(gps_data[24:33])
                    gps_lat=gps_data[24:33]
                    gps_lat=str(gps_lat).strip()
                    if "G" in str(gps_lat):
                        spl_lat=gps_lat.split("G")
                        gps_lat=spl_lat[0]
                            
                    longitude="GPS longitude in radians"
                    gps_data2=total_data_gps[total_data_gps.index(longitude):]
                    print("The GPS longitude in radians is:")
                    print(gps_data2[25:35])
                    gps_lon=gps_data2[25:35]
                    gps_lon=str(gps_lon).strip()
                    if "G" in str(gps_lon):
                        spl_lon=gps_lon.split("G")
                        gps_lon=spl_lon[0]
                else:
                    print("HX200 GPS connection lost")
                    gps_lat="0.00"
                    gps_lon="0.00"

                if(sqf.status_code==requests.codes.ok):
                    sqf_soup=BeautifulSoup(sqf.text,"html.parser")
                    total_data_sqf=sqf_soup.find_all("pre")
                    #print(total_data_sqf[1])
                    total_data_sqf_x=total_data_sqf[1].text


                    SQF="Signal Strength"
                    sqf_data=total_data_sqf_x[total_data_sqf_x.index(SQF):]
                    print("The SQF is:")
                    print(sqf_data[30:32])
                    sql_sqf=sqf_data[30:32]
                    sql_sqf=str(sql_sqf)
                    CAR="Carrier Info"
                    car_data=total_data_sqf_x[total_data_sqf_x.index(CAR):]
                    print("The carrier Info is")
                    print(car_data[18:35])
                    sql_car=car_data[18:35]
                    sql_car=str(sql_car)


                else:
                    print("HX200 SQF connection lost")
                    sql_sqf="0"
                    sql_car="000.0:0:00000"
                time_current=datetime.datetime.utcnow()
                #time_current=str(time_current)
                server = 'vesselstatusdb.database.windows.net' 
                database = 'VesselStatusDB' 
                username = 'lunghwa' 
                password = 'LHE@debug' 
                cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
                cursor = cnxn.cursor()
                cursor.execute("INSERT INTO dbo.Andy_test3 (ship_name,esn,gps_lat,gps_lon,sqf,carrierInfo,beam,time) VALUES(?,?,?,?,?,?,?,?)",vessel,esn,gps_lat,gps_lon,sql_sqf,sql_car,beam,time_current)
                cursor.commit()
            except Exception as e:
                print(e)
        print("--------------------------------------------------")