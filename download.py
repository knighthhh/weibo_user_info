import requests
import json
import config
import cookies
from config import *
from time import sleep
from requests import RequestException
from random import choice

class Download(object):
    def __init__(self,ip_url = IP_URL,change_ip = CHANGE_IP):
        self.ip_url = ip_url
        self.change_ip = change_ip

    def get_ip(self,url = IP_URL):
        print('正在获取IP。。')
        try:
            response = requests.get(url)
            if response.status_code == 200:
                res_json = json.loads(response.text)
                if res_json['ERRORCODE'] == '0':
                    ip = res_json['RESULT'][0]['ip']
                    port = res_json['RESULT'][0]['port']
                    ip_res = ip + ':' + port
                    print('获取IP成功，当前IP为：',str(ip_res))
                    return ip_res
                elif res_json['ERRORCODE'] == '10036' or res_json['ERRORCODE'] == '10038' or res_json['ERRORCODE'] == '10055':
                    print('提前IP过快，5秒后重新请求', res_json)
                    sleep(5)
                    return self.get_ip(url)
                else:
                    print('未知错误，5秒后重新请求',res_json)
                    sleep(5)
                    return self.get_ip(url)
        except RequestException:
            print('请求IP_url出错，正在重新请求',url)
            sleep(5)
            return self.get_ip(url)

    def get_html(self,url):
        #代理,cookies
        if config.REQUEST_NUM % config.CHANGE_IP == 0:
            config.IP = self.get_ip()
            config.COOKIES = choice(cookies.cookies)
        proxies = {
            'http':'http://' + config.IP
        }
        config.REQUEST_NUM +=1
        try:
            if config.COOKIES_SWITCH:
                response = requests.get(url, headers=config.HEADERS, cookies=config.COOKIES,proxies=proxies)
            else:
                response = requests.get(url, headers=config.HEADERS, proxies=proxies)
            if response.status_code == 200:
                return response.text
            return None
        except requests.exceptions.ConnectTimeout:
            print('请求RUL连接超时，正在重试', url)
            return self.get_html(url)
        except requests.exceptions.Timeout:
            print('请求RUL超时，正在重试', url)
            return self.get_html(url)
        except RequestException:
            print('未知错误，正在重试',url)
            return self.get_html(url)


if __name__ == '__main__':
    download = Download()
    res = download.get_html('https://m.weibo.cn')
    print(res)