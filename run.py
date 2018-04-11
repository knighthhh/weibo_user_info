from time import sleep

from scheduler import Scheduler
from db import MongoClient
import multiprocessing
import threading

def main():
    s = Scheduler()
    print('程序开始运行。。')
    # s.run('1266321801')
    db = MongoClient()
    while True:
        user = db.find_one_flag()
        if user:
            s.run(user['user_id'])
        else:
            print('所有用户已经爬取完')
            break


if __name__ == '__main__':
    for i in range(2):
        p = multiprocessing.Process(target=main)
        p.start()
        sleep(5)

