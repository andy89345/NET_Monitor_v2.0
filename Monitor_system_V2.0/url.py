import requests
class url:
    url_array={
        "SE_NMS_url":"http://vesselstatus.eastasia.cloudapp.azure.com/nms_ship_status.aspx",
        "SE_DNCC_url":"http://vesselstatus.eastasia.cloudapp.azure.com/dnnc_ship_status.aspx",
        "Videosoft_Bridge_url":"http://surveillance.lhsatellite.com:8080/status",
        "get_dncc_url":"http://vesselstatus.eastasia.cloudapp.azure.com/get_dncc_ship.ashx?beam="
        
       
        }

class hx200_url:
    def hx200_gps_url(lan2ip):
        result="http://"+lan2ip+"/cgi/execAdvCom.bin?Command=194&PrintMsg=Info%20Server"
        return result

    def hx200_spf_url(lan2ip):
        result="http://"+lan2ip+"/stats/summary/summary.html"
        return result

   
class mng_ip:
    def get_mng_ip(esn):
        get_ip_data_url="http://vesselstatus.eastasia.cloudapp.azure.com:8089/hx200_info/"+esn
        return get_ip_data_url
        #get_hx200_json=requests.get(get_ip_data_url)
        #if get_hx200_json.status_code == requests.codes.ok:
        #    print("GET HX200 INFO SUCCESS!!")
        #    read_url_data=get_hx200_json.text
        #    json_type_data=json.loads(read_url_data)
        #    #hx200_info_lan1=json_type_data["lan1"]
        #    #hx200_info_lan2=json_type_data["lan2"]
        #    hx200_info_mng_ip=json_type_data["mng_ip"]
        #    print(f"mng_ip={hx200_info_mng_ip}")
        #    #url1="http://"+hx200_info_mng_ip+"/cgi/execAdvCom.bin?Command=194&PrintMsg=Info%20Server"
        #    #url2="http://"+hx200_info_mng_ip+"/stats/summary/summary.html"
        #else:
        #    print("GET HX200 INFO FAIL..")
        #    #url1=""
        #    #url2=""
        #    hx200_info_mng_ip="ERROR"
        #return hx200_info_mng_ip

        
    


