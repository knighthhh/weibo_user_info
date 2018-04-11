import datetime
import json
import threading
from time import sleep

import config
import re
from download import Download
from db import MongoClient

class Scheduler(object):
    def __init__(self):
        self.download = Download()
        self.db = MongoClient()
        self.user_url_list = []
        self.threads = []

    def run(self,user_id = config.START_ID):
        self.user_start(user_id)


    def user_start(self,user_id):
        user_id = int(user_id)
        results = self.db.find(user_id)
        if (results and results['flag'] == False) or not results:
            index_data = self.get_user_index(user_id)
            if index_data:
                self.get_user_info(user_id)
                self.get_fans(user_id,index_data['user'])
                self.get_followers(user_id,index_data['user'])
            else:
                data = {
                    'user_id':user_id,
                    'flag':'Error'
                }
                self.db.save(data)
        else:
            print(results['user']," 该用户已经爬取过")



    def get_user_index(self,user_id):
        user_index = 'https://m.weibo.cn/api/container/getIndex?containerid=100505{user_id}'
        url = user_index.format(user_id=user_id)
        response = self.download.get_html(url)
        if response:
            try:
                res_json = json.loads(response)
                if 'userInfo' in res_json.keys():
                    user = res_json['userInfo']['screen_name']
                    user_id = res_json['userInfo']['id']
                    user_url = res_json['userInfo']['profile_url']
                    fans = res_json['userInfo']['followers_count']
                    followers = res_json['userInfo']['follow_count']
                    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data = {
                        'user':user,
                        'user_id':user_id,
                        'user_url':user_url,
                        'fans':fans,
                        'followers':followers,
                        'time':time,
                        'flag':True
                    }
                    print('正在抓取 ' + user +' ID为：' + str(user_id))
                    self.db.save(data)
                    return data
            except:
                print('json解析出错')
                return None

    def get_user_info(self,user_id):
        user_info = 'https://m.weibo.cn/api/container/getIndex?containerid=230283{user_id}_-_INFO'
        url = user_info.format(user_id = user_id)
        response = self.download.get_html(url)
        if response:
            # pattern = re.compile( r'{"card_type":41,"item_name":"\u6027\u522b","item_content":"(.*?)"}.*?{"card_type":41,"item_name":"\u6240\u5728\u5730","item_content":"(.*?)"}.*?{"card_type":41,"item_name":"\u7b80\u4ecb","item_content":"(.*?)"}.*?{"card_type":41,"item_name":"\u7b49\u7ea7".*?"item_content":"(.*?)".*?{"card_type":41,"item_name":"\u9633\u5149\u4fe1\u7528","item_content":"(.*?)".*?{"card_type":41,"item_name":"\u6ce8\u518c\u65f6\u95f4","item_content":"(.*?)"}',re.S)
            # results = re.search(pattern,response)
            # if results:
            #     sex = results.group(1)
            #     location = results.group(2)
            #     jianjie = results.group(3)
            #     level = results.group(4)
            #     credit = results.group(5)
            #     reg_time = results.group(6)
            sex = ''
            location = ''
            jianjie = ''
            level = ''
            credit = ''
            reg_time = ''

            sex_pattern = re.compile(r'{"card_type":41,"item_name":"\\u6027\\u522b","item_content":"(.*?)"}',re.S)
            location_pattern = re.compile(r'{"card_type":41,"item_name":"\\u6240\\u5728\\u5730","item_content":"(.*?)"}',re.S)
            # jianjie_pattern = re.compile(r'{"card_type":41,"item_name":"\\u7b80\\u4ecb","item_content":"(.*?)"}',re.S)
            level_pattern = re.compile(r'{"card_type":41,"item_name":"\\u7b49\\u7ea7".*?"item_content":"(.*?)"',re.S)
            credit_pattern = re.compile(r'{"card_type":41,"item_name":"\\u9633\\u5149\\u4fe1\\u7528","item_content":"(.*?)"',re.S)
            reg_time_pattern = re.compile(r'{"card_type":41,"item_name":"\\u6ce8\\u518c\\u65f6\\u95f4","item_content":"(.*?)"}',re.S)

            sex_res = re.search(sex_pattern,response)
            if sex_res:
                sex = sex_res.group(1).encode('utf8').decode('unicode_escape')

            location_res = re.search(location_pattern,response)
            if location_res:
                location = location_res.group(1).encode('utf8').decode('unicode_escape')

            # jianjie_res = re.search(jianjie_pattern,response)
            # if jianjie_res:
            #     jianjie = jianjie_res.group(1).encode('utf8').decode('unicode_escape')

            level_res = re.search(level_pattern,response)
            if level_res:
                level = level_res.group(1).encode('utf8').decode('unicode_escape')

            credit_res = re.search(credit_pattern,response)
            if credit_res:
                credit = credit_res.group(1).encode('utf8').decode('unicode_escape')

            reg_time_res = re.search(reg_time_pattern,response)
            if reg_time_res:
                reg_time = reg_time_res.group(1).encode('utf8').decode('unicode_escape')

            data = {
                'user_id':user_id,
                'sex':sex,
                'location':location,
                # 'jianjie':jianjie,
                'level':level,
                'credit':credit,
                'reg_time':reg_time
            }
            self.db.save(data)

    def get_fans(self,user_id,user_name):
        fans = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{user_id}&since_id={since_id}'
        for sid in range(1,251):
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('正在爬 ' + user_name + ' 第' + str(sid) +'页的粉丝')
            sleep(0.5)
            url = fans.format(user_id = user_id,since_id = sid)
            print(url)
            response = self.download.get_html(url)
            if response:
                try:
                    res_json = json.loads(response)
                    if 'cards' in res_json.keys():
                        if res_json['cards']:
                            results = res_json['cards'][0]
                            if 'card_group' in results.keys():
                                for res in results['card_group']:
                                    if 'user' in res.keys():
                                        user = res['user']['screen_name']
                                        fans_user_id = res['user']['id']
                                        data = {
                                            'user':user,
                                            'user_id':fans_user_id,
                                            'flag':False
                                        }
                                        self.db.save_first(data)
                        else:
                            print('爬了' + user_name + ' '+ str(sid) + ' 页粉丝')
                            break
                except:
                    print('json解析出错')

    def get_followers(self,user_id,user_name):
        followers = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{user_id}&page={page}'
        for page in range(1,11):
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('正在爬 ' + user_name + ' 第'+ str(page) + '页的关注')
            sleep(0.5)
            url = followers.format(user_id = user_id,page = page)
            response = self.download.get_html(url)
            if response:
                try:
                    res_json = json.loads(response)
                    if 'cards' in res_json.keys():
                        if res_json['cards']:
                            results = res_json['cards'][0]
                            if 'card_group' in results.keys():
                                for res in results['card_group']:
                                    if 'user' in res.keys():
                                        user = res['user']['screen_name']
                                        follower_user_id = res['user']['id']
                                        data = {
                                            'user': user,
                                            'user_id': follower_user_id,
                                            'flag':False
                                        }
                                        self.db.save_first(data)
                        else:
                            print('爬了' + user_name + ' ' + str(page) + ' 页关注')
                            break
                except:
                    print('json解析出错')
