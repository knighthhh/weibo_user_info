#mongodb配置
MONGO_URL = 'localhost'
MONGO_DB = 'weibo'
MONGO_TABLE_USER = 'weibo_user'
MONGO_PORT = 27017
MONGO_PASSWORD = None

#当前请求次数
REQUEST_NUM = 0

#请求多少次后换IP配置
CHANGE_IP = 150

#代理IP
IP = ''

#是否开启代理
PROXY_SWITCH = True

#cookies
COOKIES = ''

#是否使用cookies
COOKIES_SWITCH = False

#请求最大出错次数
ERROR_MAX = 5

#初始URL配置
#姚晨的微博主页
START_URL = 'https://m.weibo.cn/u/1266321801?uid=1266321801&featurecode=20000320'
START_ID = '1266321801'

#讯代理配置
IP_URL =''

#请求头配置
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Connection':'keep-alive',
    'Host':'m.weibo.cn',
    'Referer':'https://m.weibo.cn/',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With':'XMLHttpRequest',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8'
}