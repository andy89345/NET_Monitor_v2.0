from NOC import NOC
from account import login
from url import url,hx200_url,mng_ip
from pyfiglet import Figlet
import datetime
import time
import urllib.request as req
import json
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import threading
import requests
import os
import pyodbc
import math
from math import radians,cos,sin,asin,sqrt,degrees
#from fake_useragent import UserAgent
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


class satellite_count:
    def __init__(self, vessel_lat,vessel_lon,satellite_lat,satellite_lon):
        self.vessel_lat=float(vessel_lat)
        self.vessel_lon=float(vessel_lon)
        self.satellite_lat=float(satellite_lat)
        self.satellite_lon=float(satellite_lon)

    def satellite_el(self):
        up=cos(radians(self.satellite_lon-self.vessel_lon))*cos(radians(self.vessel_lat))-0.15
        down=(1-(((cos(radians(self.satellite_lon-self.vessel_lon)))*cos(radians(self.vessel_lat))))**2)**0.5
        if down!=0:
            data=up/down
        else:
            data=0
        if data!=0:
            ans=degrees(math.atan(data))
        else:
            ans=degrees(math.atan(data))+90
   
        return round(ans,3)

    def satellite_AZ(self):

        up=math.tan(radians(self.satellite_lon-self.vessel_lon))
        down=math.sin(radians(self.vessel_lat))
        if down!=0:
            data=up/down
        else:
            data=0
        if ((self.satellite_lat-self.vessel_lat)>0) and ((self.satellite_lon-self.vessel_lon)>0):
            print("Satellite in I")
            ans=-degrees(math.atan(data))
        elif((self.satellite_lat-self.vessel_lat)>0) and ((self.satellite_lon-self.vessel_lon)<0):
            print("Satellite in II")
            ans=-degrees(math.atan(data))+360
        elif((self.satellite_lat-self.vessel_lat)<0) and ((self.satellite_lon-self.vessel_lon)<0):
            print("Satellite in III")
            ans=-degrees(math.atan(data))+180   
        elif((self.satellite_lat-self.vessel_lat)<0) and ((self.satellite_lon-self.vessel_lon)>0):
            print("Satellite in IV")
            ans=-degrees(math.atan(data))+180
        elif((self.satellite_lat-self.vessel_lat)==0) and ((self.satellite_lon-self.vessel_lon)>0):
            print("Satellite in east")
            ans=degrees(math.atan(data))+270
        elif((self.satellite_lat-self.vessel_lat)==0) and ((self.satellite_lon-self.vessel_lon)<0):
            print("Satellite in west")
            ans=degrees(math.atan(data))+90
        elif((self.satellite_lat-self.vessel_lat)>0) and ((self.satellite_lon-self.vessel_lon)==0):
            print("Satellite in north")
            ans=degrees(math.atan(data))
        elif((self.satellite_lat-self.vessel_lat)<0) and ((self.satellite_lon-self.vessel_lon)==0):
            print("Satellite in south")
            ans=degrees(math.atan(data))+180
        else:
            print("Satellite in Vessel position")
            ans=degrees(math.atan(data))
        return round(ans,3)

    def satellite_PA(self):
        up=sin(radians(self.satellite_lon-self.vessel_lon))
        down=math.tan(radians(self.vessel_lat))
        if down!=0:
            data=up-down
        else:
            data=0
        ans=degrees(math.atan(data))
        return round(ans,3)

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
        open_noc_txt=open("select_noc.txt","r")
        read_noc=open_noc_txt.readline().strip()
        read_noc_upper=read_noc.upper()
        open_noc_txt.close()
        GET_NOC=NOC_json[read_noc_upper]  #Get the NOC
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
#ua = UserAgent()
#user_agent = ua.random
#headers = {'user-agent': user_agent}
class hx200:
    def get_mng_ip_function(mng_url):
        get_hx200_json=requests.get(mng_url)
        if get_hx200_json.status_code == requests.codes.ok:
            print("GET HX200 INFO SUCCESS!!")
            read_url_data=get_hx200_json.text
            json_type_data=json.loads(read_url_data)
            #hx200_info_lan1=json_type_data["lan1"]
            #hx200_info_lan2=json_type_data["lan2"]
            hx200_info_mng_ip=json_type_data["mng_ip"]
            print(f"mng_ip={hx200_info_mng_ip}")
            #url1="http://"+hx200_info_mng_ip+"/cgi/execAdvCom.bin?Command=194&PrintMsg=Info%20Server"
            #url2="http://"+hx200_info_mng_ip+"/stats/summary/summary.html"
        else:
            print("GET HX200 INFO FAIL..")
            hx200_info_mng_ip="ERROR!!"
            #url1=""
            #url2=""
        return hx200_info_mng_ip



    def GetHx200_info(lan2ip,vessel,esn,beam,videosoft_online_status):
        #print("-----------------------------------------------")
        online_status=cmd.Cmd(lan2ip)
        #print(f"vessel : {vessel}")
        if online_status==1:
            try:
                current_path=os.getcwd()
                today_date=str(datetime.datetime.today().strftime('%Y-%m-%d'))
                file_path=str(current_path)+"\\"+today_date
                vessel_log_path=file_path+"\\"+str(vessel)+".txt"
                if not os.path.isdir(file_path):
                    os.mkdir(file_path)
                else:
                    open_log_data=open(vessel_log_path,"a")

                get_mng_ip_url_fromAPI=mng_ip.get_mng_ip(esn)
                real_mng_ip=hx200.get_mng_ip_function(get_mng_ip_url_fromAPI)
                print(f"vessel : {vessel} online!!!!")
                hx200_gps_url=hx200_url.hx200_gps_url(real_mng_ip)
                hx200_sqf_url=hx200_url.hx200_spf_url(real_mng_ip)
                #headers={
                #    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
                #    }
                print(f"---------------------{hx200_gps_url}")
                print(f"---------------------{hx200_sqf_url}")
                gps=requests.get(hx200_gps_url,timeout=(60,60),verify=False)
                gps.close()
                time.sleep(1)
                sqf=requests.get(hx200_sqf_url,timeout=(60,60),verify=False)
                sqf.close()
                time.sleep(1)
                if(gps.status_code==requests.codes.ok):
                    gps_soup=BeautifulSoup(gps.text,"html.parser")
                    #gps.close()
                    #sqf.close()
                    total_data_gps=gps_soup.pre.text
                    latitude="GPS latitude in radians"
                    gps_data=total_data_gps[total_data_gps.index(latitude):]
                    #print("The GPS latitude in radians is:")
                    #print(gps_data[24:33])
                    gps_lat=gps_data[24:33]
                    gps_lat=str(gps_lat).strip()
                    if "G" in str(gps_lat):
                        spl_lat=gps_lat.split("G")
                        gps_lat=spl_lat[0]
                            
                    longitude="GPS longitude in radians"
                    gps_data2=total_data_gps[total_data_gps.index(longitude):]
                    #print("The GPS longitude in radians is:")
                    #print(gps_data2[25:35])
                    gps_lon=gps_data2[25:35]
                    gps_lon=str(gps_lon).strip()
                    if "G" in str(gps_lon):
                        spl_lon=gps_lon.split("G")
                        gps_lon=spl_lon[0]
                else:
                    #gps.close()
                    #sqf.close()
                    #print("HX200 GPS connection lost")
                    gps_lat="0.00"
                    gps_lon="0.00"

                if(sqf.status_code==requests.codes.ok):
                    sqf_soup=BeautifulSoup(sqf.text,"html.parser")
                    #sqf.close()
                    total_data_sqf=sqf_soup.find_all("pre")
                    #print(total_data_sqf[1])
                    total_data_sqf_x=total_data_sqf[1].text


                    SQF="Signal Strength"
                    sqf_data=total_data_sqf_x[total_data_sqf_x.index(SQF):]
                    #print("The SQF is:")
                    #print(sqf_data[30:32])
                    sql_sqf=sqf_data[30:32]
                    sql_sqf=str(sql_sqf).strip()
                    CAR="Carrier Info"
                    car_data=total_data_sqf_x[total_data_sqf_x.index(CAR):]
                    #print("The carrier Info is")
                    #print(car_data[18:35])
                    sql_car=car_data[18:35]
                    sql_car=str(sql_car).strip()


                else:
                    #sqf.close()
                    #print("HX200 SQF connection lost")
                    sql_sqf="0"
                    sql_car="000.0:0:00000"
                if "AU" in beam:
                    time_current=datetime.datetime.utcnow()+datetime.timedelta(hours=2)
                elif "JP" in beam:
                    time_current=datetime.datetime.utcnow()+datetime.timedelta(hours=-8)
                else:
                    time_current=datetime.datetime.utcnow()
                time_current_str=str(time_current)
                time_current_spl=time_current_str.split(".")
                time_current_clear=str(time_current_spl[0])
                time_current_final=datetime.datetime.strptime(time_current_clear, "%Y-%m-%d %H:%M:%S")
                if sql_car!="000.0:0:00000":
                    car_spl=str(sql_car).split(".")
                    sat_lat="0"
                    sat_lon=car_spl[0]
                    satellite_counter=satellite_count(gps_lat,gps_lon,sat_lat,sat_lon)
                    satellite_EL=str(satellite_counter.satellite_el())
                    satellite_AZ=str(satellite_counter.satellite_AZ())
                    satellite_PA=str(satellite_counter.satellite_PA())
                else:
                    satellite_EL="0.0"
                    satellite_AZ="0.0"
                    satellite_PA="0.0"





                
                print(f"{vessel},{esn},{sql_sqf},{gps_lat},{gps_lon},{beam},{sql_car},{time_current_final},{lan2ip},{videosoft_online_status},{satellite_EL},{satellite_AZ},{satellite_PA}")
                log_data=[
                    str(vessel)+",",
                    str(esn)+",",
                    str(sql_sqf)+",",
                    str(gps_lat)+",",
                    str(gps_lon)+",",
                    str(beam)+",",
                    str(sql_car)+",",
                    str(time_current_final)+",",
                    str(lan2ip)+",",
                    str(videosoft_online_status)+",",
                    str(satellite_EL)+",",
                    str(satellite_AZ)+",",
                    str(satellite_PA)+"\n",
                    ]
                error_log_data=[
                    "Data ERROR!!!------",
                    str(time_current_final)+"\n",
                    ]
                try:
                    print("POST")
                    post_reback=requests.post('http://vesselstatus.eastasia.cloudapp.azure.com/ku_result.ashx', data = {'ship_name':vessel,'esn':esn,'sqf':sql_sqf,'gps_lat':gps_lat,'gps_lon':gps_lon,'beam':beam,'carrierInfo':sql_car,'time':time_current_final,'lan2_ip':lan2ip,'CCTV_Active':videosoft_online_status,'AZ':satellite_AZ,'EL':satellite_EL,'PA':satellite_PA})
                    #open_log=open("log.txt","a")
                    open_log_data.writelines(log_data)
                    open_log_data.close()
                    print("POST done..")
                except Exception as e:
                    print("POST ERROR!!!!")
                    print(e)
                    #open_log=open("log.txt","a")
                    open_log_data.writelines(error_log_data)
                    open_log_data.close()
                #time_current=str(time_current)
                #server = 'vesselstatusdb.database.windows.net' 
                #database = 'VesselStatusDB' 
                #username = 'lunghwa' 
                #password = 'LHE@debug' 
                #cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
                #cursor = cnxn.cursor()
                #cursor.execute("INSERT INTO dbo.Andy_test3 (ship_name,esn,gps_lat,gps_lon,sqf,carrierInfo,beam,time) VALUES(?,?,?,?,?,?,?,?)",vessel,esn,gps_lat,gps_lon,sql_sqf,sql_car,beam,time_current)
                #cursor.commit()
                #cursor.close()
                #cnxn.close()
            except Exception as e:
                print(f"{vessel}--------{e}")
        #time.sleep(5)
        print("--------------------------------------------------")

class videosoft:
    def online_status(vessel):
        video_url_dump=json.dumps(url.url_array)
        video_url_load=json.loads(video_url_dump)
        video_url=video_url_load["Videosoft_Bridge_url"]
        video_user = 'videosoft'
        video_password = 'Lung@hwa123'
        user3_test=requests.get(video_url,timeout=(15,20),auth=HTTPBasicAuth(video_user, video_password))
        if (user3_test.status_code == requests.codes.ok):   
        #user3=req.Request(video_url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"})
        #with req.urlopen(user3)  as video_read:
        #    user_read=video_read.read()
            video_soup=BeautifulSoup(user3_test.text,"html.parser")
            find_data=video_soup.find_all("tr")
            find_data2=str(find_data)
            if vessel=="AMETHYST":
                vessel="Amethyst"
            if vessel in find_data2:
                for i in find_data:
                    total_data_video=str(i.text)
                    data_spl=total_data_video.split("\n")
                    if(len(data_spl)>=2):
                        if vessel==data_spl[2]:
                            video_active=data_spl[1]
                            video_active=str(video_active)
                            #print(total_data)
                            #print("---------------------------------------")
                            #print(f"the {vessel} CCTV_Active is : {video_active}")
                            #newTime=(datetime.datetime.utcnow()+datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
                            #newTime2=newTime[:18]
                            #print(data_spl[1])
                            #print(data_spl[2])
                            #print(data_spl[3])
                        
            else:
                video_active="No data"
                #print(f"the {name_read} CCTV_Active is : {video_active}")
        return video_active


class mail:
    def send_mail(noc):
        receivers=["andy89345@gmail.com, andy@lunghwa.com.tw"]
        content = MIMEMultipart() 
        title=str(noc)+" "+"Monitor_system_2.0"+" "+"shutdown"
        content["subject"] = title 
        content["from"] = "info@lhsat.com" 
        content["to"] = ", ".join(receivers) 
        content_a="Please restart now!! "
    
        content.attach(MIMEText(content_a))

        with smtplib.SMTP(host="smtp.hibox.biz", port="587") as smtp: 
            try:
                smtp.ehlo() 
                smtp.starttls()  
                smtp.login("info@lhsat.com", "Lunghwa123")
                smtp.send_message(content) 
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)
