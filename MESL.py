import datetime
import re
import requests

#from config import HEAD_BARK, LOGO_MESL, ACCOUNT, PASSWORD, subscribe
subscribe = "https://in.mesl.cloud/api/v1/client/subscribe?token=b1db7f6094c8c529eaa7d923cc1d3429"
headers = {
    'User-Agent': 'Clash'
}
response = requests.get(subscribe, headers=headers)
subscription_userinfo = response.headers['subscription-userinfo']

# 解析 subscription-userinfo
# 定义包含所有关键字和它们的值的正则表达式模式
# (?P<upload>\d+) 表示匹配 "upload=" 后跟一或多个数字，并将这个数字组合成名为 "upload" 的命名捕获组
pattern = r"upload=(?P<upload>\d+).*download=(?P<download>\d+).*total=(?P<total>\d+).*expire=(?P<expire>\d+)"

# 使用re模块中的match()方法在字符串中查找模式的匹配项
match = re.match(pattern, subscription_userinfo)

# 检查是否找到了匹配项
if match:
    # 使用group()方法获取每个命名捕获组的值
    upload_value = int(match.group('upload'))
    download_value = int(match.group('download'))
    total_value = int(match.group('total'))
    expire_value = int(match.group('expire'))
    # 计算实际的值
    upload_gb = round(upload_value / 1024 ** 3 , 2)
    download_gb = round(download_value / 1024 ** 3 , 2)
    used = round(upload_gb + download_gb , 2)
    total_gb = round(total_value / 1024 ** 3 , 2)
    expire_timestamp = expire_value
    expire_date = datetime.datetime.fromtimestamp(expire_timestamp)
    remaining_days = (expire_date - datetime.datetime.now()).days

    print("上传:" + str(upload_gb))
    print("下载:" + str(download_gb))
    print("已用流量:" + str(used))
    print("总流量:" + str(total_gb))
    print("剩余时间:" + str(remaining_days))

