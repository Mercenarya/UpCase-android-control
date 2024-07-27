import urllib3
def Connection_Detect():
    resp = urllib3.request("GET",'https://www.google.com',timeout=1.0)
    status = resp.status
    return status
try:
    if Connection_Detect() == 200:
        print('Connected')
except:
    print("Connection Interrupted")