# -*- coding: utf-8 -*-
import os, re
import json

work_dir = "./result/"
p_module = {}

def format(file):
    j_file = json.load(file)
    print(json.dumps(j_file, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

def ip_api(file):
    jfile = json.load(file)
    if jfile.get("status") == "success":
        ip = jfile.get("query")
        country_cn = jfile.get("country")
        country_code = jfile.get("countryCode")
        city = jfile.get("city")
        lat = jfile.get("lat")
        lon = jfile.get("lon")
        isp = jfile.get("isp")
        org = jfile.get("org")
        asn = jfile.get("as")
        searchObj = re.search( r'AS.*?\ ', asn, re.M)
        if not searchObj:
            asn = ""
        print("%s, %s, %s" % (jfile.get("query"), isp, searchObj.group()))
    
    
def init():
    p_module["qianxin-ti-ip"] = format
    p_module["qianxin-ti-hash"] = format
    p_module["virustotal-ip"] = format
    p_module["censys"] = format
    p_module["ipinfo-ip-api"] = ip_api
    p_module["qianxin-pdns-client"] = format
    p_module["qianxin-pdns-domain"] = format
    p_module["virustotal-domain"] = format
    p_module["qianxin-nd"] = format
    p_module["virustotal-file"] = format
    p_module["aliyun-domain-whois"] = format
    p_module["qianxin-rrset"] = format
    p_module["qianxin-rrdata"] = format
    p_module["qianxin-ti-domain"] = format
    p_module["site-title"] = format

if __name__ == "__main__":
    init()
    for fpathe, dirs, fs in os.walk(work_dir):
        for finfo in fs:
            path = os.path.join(fpathe,finfo)
            
            f = open(path, "r", encoding="utf-8")
            for name in p_module:
                if name in path:
                    pfunc = p_module[name]
                    pfunc(f)
            f.close()