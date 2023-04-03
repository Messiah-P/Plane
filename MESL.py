import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

head_bark = 'https://api.day.app/HCpomwdmsT2cNj7zkGmTvn'
logo_yy = 'https://lsky.pantheon.center/image/2023/04/02/642940f3a50c1.png'

chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

#点击
def click(path):
    driver.find_element(By.XPATH, path).click()

#输入
def send(path,key):
    driver.find_element(By.XPATH, path).send_keys(key)

#识别
def text(path):
    result = driver.find_element(By.XPATH, path).text
    return result

#登陆
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://in.mesl.cloud/#/login')
driver.implicitly_wait(5)
send('//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[2]/input','1661862073@qq.com')
send('//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[3]/input','022760Mesl')
click('//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[4]/button')
#driver.implicitly_wait(2)
sleep(2)

#进入控制面板
driver.get('https://in.mesl.cloud/#/dashboard')
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
time_reset = str(lasttime).split(" ")[5] #提取重置时间
time_y = str(time).split("/")[0]
time_m = str(time).split("/")[1]
time_d = str(time).split("/")[2]

flow_used = float(str(flow).split(' ')[1]) #已用流量
flow_used_unit = str(flow).split(' ')[2] # 已用流量单位
print(flow_used)
flow_all = float(str(flow).split(' ')[5]) #总流量
flow_all_unit = str(flow).split(' ')[6] # 已用流量单位
print(flow_all)
if flow_used_unit == 'MB':
    flow_used_fixed = flow_used/1024
flow_left = flow_all - flow_used_fixed #剩余流量
flow_per = int(flow_used_fixed/flow_all*20) #使用占比
flow_percent = '{:.0%}'.format(flow_used_fixed/flow_all) #使用量百分比
print(flow_percent)

#转Bark字符串
flow_daily = flow_left/float(time_reset)
print(flow_daily)
flow_daily = "剩余日均: " + str("%.2f" % flow_daily) + ' ' + flow_all_unit
flow_left = "已用流量: " + str("%.2f" % flow_used) + ' ' + flow_used_unit + "·" + str(flow_all) + 'GB'
time_left = "剩余天数: " + time_left + "天" + "·" + time_reset + "天"
#进度条
s_jd = "流量进度: ["
for number in range(1, flow_per):
    s_jd = s_jd + ">"
for number in range(1, 20 - flow_per):
    s_jd = s_jd + "-"
s_jd = s_jd + "]" + "·" + flow_percent


deadline = "截止日期: " + time_y + "年" + time_m+ "月" + time_d + "日"
ret = requests.get('%s/Mesl/%s\n%s\n%s\n%s\n%s?icon=%s&group=Mesl'% (head_bark,flow_daily,flow_left,s_jd,time_left,deadline,logo_yy))

driver.close()
driver.quit()
