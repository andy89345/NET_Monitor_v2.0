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

   
    

        
    


