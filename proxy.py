import requests
import settings as config

# GET PROXY IP FROM WEBSHARE.IO
def getProxies():
    proxies=[]
    try:
        r = requests.get(config.PROXY_URL, headers={"Authorization": config.PROXY_API_KEY}).json()
        for url in r['results']:
            p = "http://" + url['username'] + ":" + url['password'] + "@" + url['proxy_address'] + ":" + str(
                url['ports']['http'])
            proxies.append(p)
    except:
        print("PROXY CONNECTION FAILED!")
    
    return proxies
