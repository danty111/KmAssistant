from excel import getVrs
import re


# class get_exe():
#     def __init__(self):
#         self.flattened_list = []
#         self.temporarily_list = []
#
#     def flatten_data(self,data):
#         for item in data:
#             if isinstance(item, dict) and 'title' in item:
#                 self.temporarily_list.append(item['title'])
#             if 'topics' in item and isinstance(item['topics'], list):
#                 self.flatten_data(item['topics'])
#             else:
#                 self.flattened_list.append(self.temporarily_list)
#                 self.temporarily_list = []
#         return self.flattened_list
#
# data = [{'title': 'PR微平台v6.1.4.20231031 公众号、H5、小程序不同场景数据修复流程【55804024】', 'topics': [{'title': '关注公众号-正常修复流程', 'topics': [{'title': '关注公众号', 'topics': [{'title': '关注公众号', 'topics': [{'title': '触发修复流程', 'topics': [{'title': '1'}]}]}]}]}, {'title': '未关注公众号-（没有公众号openid）访问小程序', 'topics': [{'title': '无', 'topics': [{'title': '1、访问小程序', 'topics': [{'title': '跳转到公众号', 'topics': [{'title': '2'}]}]}]}]}, {'title': '未关注公众号-（有公众号openid）访问小程序', 'topics': [{'title': '未关注公众号', 'topics': [{'title': '直接触发修复流程', 'topics': [{'title': '2'}]}]}]}, {'title': '不关注公众号直接访问H5(绑定小程序)', 'topics': [{'title': '绑定了小程序', 'topics': [{'title': '跳转到小程序', 'topics': [{'title': '触发修复流程', 'topics': [{'title': '2'}]}]}]}]}, {'title': '不关注公众号直接访问H5(未绑定小程序）', 'topics': [{'title': '未绑定小程序', 'topics': [{'title': '直接访问h5', 'topics': [{'title': '弹出提示语（请先关注公众号）', 'topics': [{'title': '2'}]}]}]}]}, {'title': '不关注公众号，但数据库存在unionid时，访问h5', 'topics': [{'title': '未关注公众号', 'topics': [{'title': '1.访问小程序后解绑小程序\n2.访问h5', 'topics': [{'title': '触发修复流程', 'topics': [{'title': '2'}]}]}]}]}]}]
#
# # flattened_data = get_exe().flatten_data(data)
# a = "222"
# a = a+"111"
# makers = ['priority-1'][0]
# match = int(re.search(r'\d+', makers).group())
# # print(match)
# getVrs().convert_xmind_to_excel('C:/Users/yuanhaibo/Desktop/冒烟/1钱333.xmind', r'C:\Users\yuanhaibo\Desktop\冒烟')

import requests

# 设置蒲公英上应用的 App Key
app_key = 'YOUR_APP_KEY'

# 发送请求获取应用信息
response = requests.get(f'https://www.pgyer.com/apiv2/app/viewGroup?com.kemai.merchantassistant.ceshi', params={'_api_key': 'eff282712bbde4644a5ee6835cfd39d8'})

# 解析响应 JSON 数据获取最新包的下载地址
data = response.json()
print(data)
download_url = data['data']['builds'][0]['buildQRCodeURL']
print(download_url)
# # 发送请求下载最新包
# response = requests.get(download_url)
#
# # 保存下载的包到本地文件
# with open('latest_app.apk', 'wb') as file:
#     file.write(response.content)
#
# print('包下载完成！')