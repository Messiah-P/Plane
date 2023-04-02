import requests
import re
import sys
import io
from retrying import retry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

head_bark = 'https://api.day.app/HCpomwdmsT2cNj7zkGmTvn'
logo_yy = 'https://lsky.pantheon.center/image/2022/11/28/6384d1dfa33d9.jpg'

chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

#driver.implicitly_wait(5) #隐式等待
#print(driver.page_source) #打印页面
#ActionChains(driver).move_by_offset(10, 10).click().perform() #鼠标左键点击，200为x坐标，100为y坐标
#flow = driver.find_element(By.CLASS_NAME,'font-w700').text #通过class查询

#点击
#@retry(wait_fixed=10, stop_max_attempt_number=1)
def click(path):
    driver.find_element(By.XPATH, path).click()

#输入
#@retry(wait_fixed=10, stop_max_attempt_number=1)
def send(path,key):
    driver.find_element(By.XPATH, path).send_keys(key)

#识别
#@retry(wait_fixed=1, stop_max_attempt_number=2)
def text(path):
    result = driver.find_element(By.XPATH, path).text
    return result

#登陆
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://xn--4gq62f52gdss.com/#/login')
driver.implicitly_wait(5)
send('//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[2]/input','2090757601@qq.com')
send('//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[3]/input','022760Yy')
click('//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[4]/button')
#driver.implicitly_wait(2)
sleep(2)

#进入控制面板
driver.get('https://xn--4gq62f52gdss.com/#/dashboard')
driver.implicitly_wait(2)
#ActionChains(driver).move_by_offset(100, 100).click().perform() #鼠标左键点击，200为x坐标，100为y坐标
#click('/html/body/div[2]/div/div[2]/div/div[2]/button')
print("查询结果")
driver.implicitly_wait(10)
lasttime = text('//*[@id="main-container"]/div/div[2]/div/div/div[2]/div/div/div/div[1]/p/span')
flow = driver.find_element(By.CLASS_NAME,'font-w700').text
print(lasttime)
print(flow)

#数据提取
time_left = str(lasttime).split(" ")[3] #距离到期时间
time = str(lasttime).split(" ")[1] #提取时间
time_reset = str(lasttime).split(" ")[4].split("。")[1] #提取重置时间
time_y = str(time).split("/")[0]
time_m = str(time).split("/")[1]
time_d = str(time).split("/")[2]

flow_used = int(float(str(flow).split(' ')[1])) #已用流量
flow_all = str(int(float(str(flow).split(' ')[5]))) #总流量
flow_left = float(flow_all) - float(flow_used) #剩余流量
flow_per = int(float(flow_used)/float(flow_all)*20) #使用占比
flow_percent = '{:.0%}'.format(float(flow_used)/float(flow_all)) #使用量百分比

#转Bark字符串
flow_daily = flow_left/float(time_reset)
flow_daily = "剩余日均: " + str("%.2f" % flow_daily) + ' GB'
flow_left = "已用流量: " + str("%.2f" % flow_used) + ' GB' + "·" + flow_all + 'GB'
time_left = "剩余天数: " + time_reset + "天" + "·" + time_left + "天"
#进度条
s_jd = "流量进度: ["
for number in range(1, flow_per):
    s_jd = s_jd + ">"
for number in range(1, 20 - flow_per):
    s_jd = s_jd + "-"
s_jd = s_jd + "]" + "·" + flow_percent
#s_jd = "[>>>>-----------------------]·10%·100 GB"
#s5 = "已使用: " + flow_used + ' GB'
#s6 = "总流量: " + flow_all + ' GB'
deadline = "截止日期: " + time_y + "年" + time_m+ "月" + time_d + "日"
ret = requests.get('%s/一元机场/%s\n%s\n%s\n%s\n%s?icon=%s&group=一元机场'% (head_bark,flow_daily,flow_left,s_jd,time_left,deadline,logo_yy))

driver.close()
driver.quit()
