# -*- coding: utf-8 -*-
import os
import json

work_dir = "./result/"
p_module = {}
format = False

def json_format(filepath):
    try:
        f = fopen(filepath, "r", "utf-8")
        j_file = json.load(f)
        dumps_str = json.dumps(j_file, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
        f.close()
        
        f = fopen(filepath, "w", "utf-8")
        f.write(dumps_str)
        f.close()
    except Exception as err:
        print("json format error, %s" % err)

def ip_api(filepath):
    f = fopen(filepath, "r", "utf-8")
    jfile = json.load(f)
    if jfile.get("status") == "success":
        ip = jfile.get("query")
        country = jfile.get("country")
        region = jfile.get("regionName")
        city = jfile.get("city")
        lat = jfile.get("lat")
        lon = jfile.get("lon")
        isp = jfile.get("isp")
        as_org = jfile.get("org")
        asn = jfile.get("as")
        if len(asn) > 2 and (asn[0:2] == "AS" or asn[0:2] == "as"):
            space_index = asn.index(" ")
            asn = asn[0:space_index]
            
        # ip, country, region, city, asn, as_org, isp
        print("ip, country, region, city, asn, as_org, isp")
        print("%s , %s, %s, %s, %s, %s, %s" % (ip , country, region, city, asn, as_org, isp))
    f.close()

def fofa(filepath):
    f = fopen(filepath, "r", "utf-8")
    jfile = json.load(f)
    
    if jfile.get("error"):
        print(jfile.get("errmsg"))
        return
    mode = jfile.get("mode")
    size = jfile.get("size")
    page = jfile.get("page")
    if jfile.get("results") == None:
        jfile["results"] = []
        
    print("get results: %d, size: %s, page: %s, mode: %s" % (len(jfile.get("results")), size, page, mode))
    
    print("ip:port(protocol), country, province, city, as_number, as_organization, isp")
    for obj in jfile.get("results"):
        ip              = obj[0]
        port            = obj[1]
        country         = obj[2].replace("'", "\"")
        host            = obj[3]
        title           = obj[4].replace("'", "\"")
        domain          = obj[5].replace("'", "\"")
        province        = obj[6].replace("'", "\"")
        country_name    = obj[7].replace("'", "\"")
        header          = obj[8].replace("'", "\"")
        server          = obj[9].replace("'", "\"")
        protocol        = obj[10].replace("'", "\"")
        banner          = obj[11].replace("'", "\"")
        as_number       = "AS"+ str(obj[12])
        as_organization = obj[13].replace("'", "\"")
        latitude        = obj[14]
        longitude       = obj[15]
        isp             = obj[16].replace("'", "\"")
        city            = obj[17].replace("'", "\"")
        m_type          = "fofa"
        m_status        = "0"
        
        #ip:port(protocol), country, province, city, as_number, as_organization, isp
        print("%s:%s(%s), %s, %s, %s, %s, %s, %s" % (ip,port, protocol, country, province, city, as_number, as_organization, isp))
    f.close()
    
def censys(filepath):
    f = fopen(filepath, "r", "utf-8")
    jfile = json.load(f)
    if jfile.get("status") != "ok":
        print(jfile.get("error"))
        return
        
    print(jfile.get("metadata"))
    
    print("ip:port/protocols, country, province, city, autonomous_system_asn, autonomous_system_name, autonomous_system_routed_prefix")
    for obj in jfile.get("results"):
        ip = obj.get("ip")
        updated_at = obj.get("updated_at")
        city = obj.get("location.city")
        country = obj.get("location.country")
        province = obj.get("location.province")
        protocols = obj.get("protocols")
        longitude = obj.get("location.longitude")
        latitude = obj.get("location.latitude")
        autonomous_system_routed_prefix = obj.get("autonomous_system.routed_prefix")
        autonomous_system_asn = "AS%d" % obj.get("autonomous_system.asn")
        autonomous_system_name = obj.get("autonomous_system.name")
        if len(protocols)<=0:
            port = "0"
            proto = ""
            host = "%s:%s" % (ip, port)
            print("%s:%s/%s, %s, %s, %s, %s, %s, %s" % (ip, port, proto, country, province, city, autonomous_system_asn, autonomous_system_name, autonomous_system_routed_prefix))
            
        else:
            for i in protocols:
                port = i.split("/")[0]
                proto = i.split("/")[1]
                host = "%s:%s" % (ip, port)
                print("%s:%s/%s, %s, %s, %s, %s, %s, %s" % (ip, port, proto, country, province, city, autonomous_system_asn, autonomous_system_name, autonomous_system_routed_prefix))
        
        #ip:port/protocols, country, province, city, autonomous_system_asn, autonomous_system_name, autonomous_system_routed_prefix
        #print("%s:%s/%s, %s, %s, %s, %s, %s, %s" % (ip, port, protocols, country, province, city, autonomous_system_asn, autonomous_system_name, autonomous_system_routed_prefix))
    f.close()           
                
def shodan(filepath):
    f = fopen(filepath, "r", "utf-8")
    jfile = json.load(f)
    if int(jfile.get("total")) <= 0:
        print("shodan search not found")
        return
        
    for obj in jfile.get("matches"):
        ip = obj.get("ip_str")
        port = obj.get("port")
        host = "%s:%s" % (ip, port)
        asn = obj.get("asn")
        protocol = obj.get("product")
        isp = obj.get("isp")
        asn_org = obj.get("org")
        utime = obj.get("timestamp")
        longitude = obj.get("location.longitude")
        latitude = obj.get("location.latitude")
        city = obj.get("location.city")
        country = obj.get("location.country_name")
        region = obj.get("location.region_code")
        
        #ip, port, protocol, country, region, city, asn, asn_org, isp
        print("ip, port, protocol, country, region, city, asn, asn_org, isp")
        print("%s, %s, %s, %s, %s, %s, %s, %s, %s" % (ip, port, protocol, country, region, city, asn, asn_org, isp))
    f.close()
    
def init():
    p_module["ipinfo-ip-api"] = ip_api
    p_module["censys"] = censys
    p_module["fofa"] = fofa
    p_module["shodan-search"] = shodan

def fopen(filepath, mode, encoding):
    import sys
    if sys.version_info < (3, 0):
        return open(filepath, mode)
    else:
        return open(filepath, mode, encoding=encoding)
    
if __name__ == "__main__":
    init()
    for fpathe, dirs, fs in os.walk(work_dir):
        for finfo in fs:
            path = os.path.join(fpathe,finfo)
            
            if format:
                json_format(path)
            
            for name in p_module:
                if name in path:
                    try:
                        print("%s%s%s" % ('*' * 20, path, '*' * 20))
                        pfunc = p_module[name]
                        pfunc(path)
                    except Exception as err:
                        print("execute func error, %s" % err)
                