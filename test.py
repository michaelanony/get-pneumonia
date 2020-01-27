import json
import re

with open("te.json","r",encoding="utf-8") as fp:
    ret = json.loads(fp.read())
city_details_lists = eval(ret["forum"]["extra"]["ncov_string_list"])
handle_list=[]

for city_details in city_details_lists:
    city_details = city_details.split(" ")
    city = {}
    city_data = {}
    for index,city_detail in enumerate(city_details):
        if index == 0:
            city["city_name"] = city_detail
        if "确诊" in city_detail:
            city_data["确诊数量"] = re.search(r"\d+",city_detail).group()

        if "死亡" in city_detail:
            city_data["死亡数量"] = re.search(r"\d+",city_detail).group()

        if "治愈" in city_detail:
            city_data["治愈数量"] = re.search(r"\d+",city_detail).group()

    city['data']=city_data
    handle_list.append(city)


print(handle_list)

# import redis
#
# rc = redis.Redis(host="192.168.11.31", port="30002",db=1)
# # rc.set("shanghai","{'确诊数量': '1423', '死亡数量': '76', '治愈数量': '44'}")
# # print(type(eval(str(rc.hget("city","shanghai"),encoding='utf-8'))))
#
# ret = str(rc.get("shanghai"),encoding='utf-8')
# if ret == "{'确诊数量': '1423', '死亡数量': '76', '治愈数量': '44'}":
#     print(
#         1
#     )
#
# te=[1,4,"4"]
#
# te.remove(4)
# print(te)
#
# st = "[{'city_name': '湖北', 'data': {'confirm_num': '1423', 'death_num': '76', 'cure_num': '44'}}, {'city_name': '广东', 'data': {'confirm_num': '151', 'cure_num': '2'}}, {'city_name': '河南', 'data': {'confirm_num': '128', 'death_num': '1'}}, {'city_name': '浙江', 'data': {'confirm_num': '128', 'cure_num': '1'}}, {'city_name': '重庆', 'data': {'confirm_num': '110'}}, {'city_name': '湖南', 'data': {'confirm_num': '100'}}, {'city_name': '山东', 'data': {'confirm_num': '75'}}, {'city_name': '北京', 'data': {'confirm_num': '72', 'cure_num': '2'}}, {'city_name': '安徽', 'data': {'confirm_num': '70'}}, {'city_name': '四川', 'data': {'confirm_num': '69'}}, {'city_name': '福建', 'data': {'confirm_num': '56'}}, {'city_name': '上海', 'data': {'confirm_num': '53', 'death_num': '1', 'cure_num': '3'}}, {'city_name': '江西', 'data': {'confirm_num': '48', 'cure_num': '2'}}, {'city_name': '江苏', 'data': {'confirm_num': '47', 'cure_num': '1'}}, {'city_name': '广西', 'data': {'confirm_num': '46'}}, {'city_name': '陕西', 'data': {'confirm_num': '35'}}, {'city_name': '海南', 'data': {'confirm_num': '33', 'death_num': '1'}}, {'city_name': '辽宁', 'data': {'confirm_num': '27'}}, {'city_name': '云南', 'data': {'confirm_num': '26'}}, {'city_name': '黑龙江', 'data': {'confirm_num': '21', 'death_num': '1'}}, {'city_name': '河北', 'data': {'confirm_num': '18', 'death_num': '1'}}, {'city_name': '天津', 'data': {'confirm_num': '18'}}, {'city_name': '甘肃', 'data': {'confirm_num': '14'}}, {'city_name': '山西', 'data': {'confirm_num': '13'}}, {'city_name': '内蒙古', 'data': {'confirm_num': '11'}}, {'city_name': '香港', 'data': {'confirm_num': '8'}}, {'city_name': '贵州', 'data': {'confirm_num': '7'}}, {'city_name': '宁夏', 'data': {'confirm_num': '7'}}, {'city_name': '吉林', 'data': {'confirm_num': '6'}}, {'city_name': '澳门', 'data': {'confirm_num': '6'}}, {'city_name': '新疆', 'data': {'confirm_num': '5'}}, {'city_name': '台湾', 'data': {'confirm_num': '5'}}, {'city_name': '青海', 'data': {'confirm_num': '4'}}]"
# for s in st :
#     print(s)
s1 = "{'confirm_num': '7', 'death_num': 0, 'cure_num': 0}"
s2 = "{'confirm_num': '7', 'death_num': 0, 'cure_num': 0}"
if s1 ==s2:
    print(1)