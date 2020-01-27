import requests
import json
import pymysql
import redis
import time
import re
from threading import Thread

city_py_map = {'湖北': 'hu_bei', '广东': 'guang_dong', '河南': 'he_nan', '浙江': 'zhe_jiang', '重庆': 'chong_qin', '湖南': 'hu_nan',
               '山东': 'shan_dong', '北京': 'bei_jing', '安徽': 'an_hui', '四川': 'si_chuan', '福建': 'fu_jian', '江西': 'jiang_xi',
               '江苏': 'jiang_su', '广西': 'guang_xi', '陕西': 'shan1_xi', '海南': 'hai_nan', '辽宁': 'liao_ning',
               '黑龙江': 'hei_long_jiang', '云南': 'yun_nan', '河北': 'he_bei', '天津': 'tian_jing', '甘肃': 'gan_su',
               '山西': 'shan_xi', '内蒙古': 'nei_meng_gu', '香港': 'xiang_gang', '贵州': 'gui_zhou', '宁夏': 'ning_xia',
               '吉林': 'ji_lin', '澳门': 'ao_men', '新疆': 'xin_jiang', '台湾': 'tai_wan', '青海': 'qing_hai', '上海': 'shang_hai'}


class PneumoniaSpider:
    def __init__(self):
        self.iota = 1
        import urllib3
        self.rc = redis.Redis(host="192.168.11.31", port="30002", db=1)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.db = pymysql.connect(host="192.168.11.31", password="cccbbb", user="michael", port=30001,
                                  database="pneumonia_record")
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 NewsArticle/7.5.7.32 JsSdk/2.0 NetType/WIFI (News 7.5.7 13.300000)",
            "Accept": "application/json, text/javascript"
        }
        sess = requests.session()
        sess.headers = headers
        sess.verify = False
        self.sess = sess
        self.programme_flag = True

    def start(self):

        self.programme_flag = str(self.rc.get("isRunProgramme"), encoding='utf-8')
        spider_flag = str(self.rc.get("isRunSpider"), encoding='utf-8')
        url = str(self.rc.get("captcha_url"), encoding='utf-8')
        print("Now programme_flag is {},spider_flag is {}, url is {}".format(self.programme_flag, spider_flag, url))
        print("Init success!")
        while spider_flag:
            self.run_spider(url)
            print("This is " + str(self.iota) + " run success!")
            self.iota += 1
            time.sleep(10)

    def run_spider(self, url):
        print("=========Now get data============")
        ret = json.loads(self.sess.get(url).text)

        self.all_city = ret["forum"]["rich_content"]
        self.city_details_lists = eval(ret["forum"]["extra"]["ncov_string_list"])
        city_map = self.handle_city_details_lists()
        data_list = self.check_redis_update(city_map)
        self.db_insert_handle(data_list)

    def handle_city_details_lists(self):
        handle_list = []
        for city_details in self.city_details_lists:
            city_details = city_details.split(" ")
            city = {}
            city_data = {
                "confirm_num": 0,
                "death_num": 0,
                "cure_num": 0
            }
            for index, city_detail in enumerate(city_details):
                if index == 0:
                    city["city_name"] = city_detail
                if "确诊" in city_detail:
                    city_data["confirm_num"] = re.search(r"\d+", city_detail).group()
                if "死亡" in city_detail:
                    city_data["death_num"] = re.search(r"\d+", city_detail).group()

                if "治愈" in city_detail:
                    city_data["cure_num"] = re.search(r"\d+", city_detail).group()

            city['data'] = city_data
            handle_list.append(city)
        return handle_list

    def check_redis_update(self, city_map: list):
        for i in city_map[:]:
            ret = self.rc.get(i['city_name'])
            if ret and str(ret, encoding='utf-8') == str(i['data']):
                city_map.remove(i)
            else:
                print(i['city_name'] + "changed")
                print("redis ret=", ret)
                print("data is ", i['data'])
                self.rc.set(i['city_name'], str(i['data']))
        return city_map

    def db_insert_handle(self, data_list):
        with self.db.cursor()as cursor:
            for data in data_list:
                try:
                    table_name = city_py_map[data['city_name']]
                    sql_str = "INSERT INTO pneumonia_record.{}(city_name,confirm_num,death_num,cure_num) values('{}',{},{},{})".format(
                        table_name, data['city_name'], data['data']['confirm_num'], data['data']['death_num'],
                        data['data']['cure_num'])
                    print(sql_str)
                    cursor.execute(sql_str)
                    sql_str2 = "UPDATE pneumonia_record.all_city_new SET confirm_num={},death_num={},cure_num={} WHERE city_name='{}'".format(
                        data['data']['confirm_num'], data['data']['death_num'], data['data']['cure_num'],
                        data['city_name'])
                    cursor.execute(sql_str2)
                except Exception as e:
                    print("db_insert_handle err is ", e)
            self.db.commit()

    def db_create_table(self, table_name: dict):

        with self.db.cursor()as cursor:

            for city, city_py in table_name.items():
                try:
                    sql_str = "create table pneumonia_record.{}\
                    (\
                        city_name   varchar(255) default '{}'           null comment '城市',\
                        confirm_num  int          default 0                 null comment '确诊数量',\
                        cure_num    int          default 0                 null comment '治愈数量',\
                        death_num   int          default 0                 null comment '死亡数量',\
                        update_time timestamp    default CURRENT_TIMESTAMP null comment '更新时间'\
                    )comment '{}';".format(city_py, city_py, city)
                    print(sql_str)
                    cursor.execute(sql_str)
                except Exception as e:
                    print(e)
            self.db.commit()


if __name__ == '__main__':
    sp = PneumoniaSpider()
    sp.start()
