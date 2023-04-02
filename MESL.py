import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

head_bark = 'https://api.day.app/HCpomwdmsT2cNj7zkGmTvn'
logo_mesl = 'https://lsky.pantheon.center/image/2023/04/02/642940f3a50c1.png'

chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 登录
def login(driver):
    driver.get('https://in.mesl.cloud/#/login')
    sleep(5)
    email_input = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[2]/input')
    email_input.send_keys('13961722760@qq.com')
    password_input = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[3]/input')
    password_input.send_keys('022760Mesl')
    login_btn = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[4]/button')
    login_btn.click()
    sleep(5)

# 获取流量信息
def get_flow_info(driver):
    driver.get('https://in.mesl.cloud/#/dashboard')
    sleep(2)
    lasttime = driver.find_element(By.XPATH, '//*[@id="main-container"]/div/div[2]/div/div/div[2]/div/div/div/div[1]/p/span')
    flow = driver.find_element(By.CLASS_NAME, 'font-w700')
    flow_used = int(float(str(flow.text).split(' ')[1])) # 已用流量
    flow_all = str(int(float(str(flow.text).split(' ')[5]))) # 总流量
    flow_left = float(flow_all) - float(flow_used) # 剩余流量
    flow_per = int(float(flow_used)/float(flow_all)*20) # 使用占比
    flow_percent = '{:.0%}'.format(float(flow_used)/float(flow_all)) # 使用量百分比
    time_left = str(lasttime.text).split(" ")[3] # 距离到期时间
    time = str(lasttime.text).split(" ")[1] # 提取时间
    time_reset = str(lasttime.text).split(" ")[4].split("。")[1] # 提取重置时间
    time_y = str(time).split("/")[0]
    time_m = str(time).split("/")[1]
    time_d = str(time).split("/")[2]

    # 转Bark字符串
    flow_daily = flow_left/float(time_reset)
    flow_daily = "剩余日均: " + str("%.2f" % flow_daily) + ' GB'
    flow_left = "已用流量: " + str("%.2f" % flow_used) + ' GB' + "·" + flow_all + 'GB'
    time_left = "剩余天数: " + time_reset + "天" + "·" + time_left + "天"
    # 进度条
    s_jd = "流量进度: ["
    for number in range(1, flow_per):
        s_jd = s_jd + ">"
    for number in range(1, 20 - flow_per):
        s_jd = s_jd + "-"
    s_jd = s_jd + "]" + "·" + flow_percent
    deadline = "截止日期: " + time_y + "年" + time_m+ "月" + time_d + "日"
    return (flow_daily, flow_left, s_jd, time_left, deadline)

# 发送到Bark
def send_to_bark(flow_daily, flow_left, s_jd, time_left, deadline):
    ret = requests.get('%s/MESL/%s\n%s\n%s\n%s\n%s?icon=%s&group=MESL' % (head_bark, flow_daily, flow_left, s_jd, time_left, deadline, logo_mesl))

driver = webdriver.Chrome(options=chrome_options)
login(driver) # 登录
flow_info = get_flow_info(driver) # 获取流量信息
send_to_bark(*flow_info) # 发送到Bark
driver.quit()
