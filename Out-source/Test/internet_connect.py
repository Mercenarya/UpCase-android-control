import urllib3
import flet as ft
def check_internet_conn():
    http = urllib3.PoolManager(timeout=3.0)
    r = http.request('GET', 'google.com', preload_content=False)
    code = r.status
    r.release_conn()
    if code == 200:
        return True
    else:
        return False
def main(page: ft.Page):
    page.add(ft.Text("Connected !!!",size=30,color="white"))
    page.add(ft.Icon(name=ft.icons.WIFI,size=50,color="white"))
    page.update()
def Disconnected_notice(page: ft.Page):
    page.add(ft.Text("Wifi Disonnected !!!",size=30,color="white"))
    page.add(ft.Icon(name=ft.icons.SIGNAL_WIFI_CONNECTED_NO_INTERNET_4_SHARP,size=50,color="white"))
    page.update()
    
if __name__ == "__main__":
    try:
        print(check_internet_conn())
        ft.app(target=main)
        print("Connected")
    except:
        ft.app(target=Disconnected_notice)
        print("Disconnected")