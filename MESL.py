import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from config import HEAD_BARK, LOGO_MESL, ACCOUNT, PASSWORD


# 点击
def click(driver, path):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
    element.click()

# 输入
def send(driver, path, key):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path)))
    element.send_keys(key)

# 识别
def text(driver, path):
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, path)))
    result = element.text
    return result

# 登陆
def login(driver):
    driver.get('https://in.mesl.cloud/#/login')
    send(driver, '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[2]/input', ACCOUNT)
    send(driver, '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[3]/input', PASSWORD)
    click(driver, '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[4]/button')
    sleep(2)


# 进入控制面板
def goto_dashboard(driver):
    driver.get('https://in.mesl.cloud/#/dashboard')
    lasttime = text(driver, '//*[@id="main-container"]/div/div[2]/div/div/div[2]/div/div/div/div[1]/p/span')
    flow = driver.find_element(By.CLASS_NAME, 'font-w700').text
    return lasttime, flow

# 数据提取
def extract_data(lasttime, flow):
    time_left = str(lasttime).split(" ")[3] #距离到期时间
    time = str(lasttime).split(" ")[1] #提取时间
    time_reset = str(lasttime).split(" ")[5] #提取重置时间
    time_y, time_m, time_d = str(time).split("/")

    flow_used = float(str(flow).split(' ')[1])  # 已用流量
    flow_used_unit = str(flow).split(' ')[2]  # 已用流量单位
    print(flow_used)
    flow_all = float(str(flow).split(' ')[5])  # 总流量
    flow_all_unit = str(flow).split(' ')[6]  # 已用流量单位
    print(flow_all)
    flow_used_fixed = flow_used/1024 if flow_used_unit == 'MB' else flow_used # 转换单位
    flow_left = flow_all - flow_used_fixed #剩余流量
    flow_per = int(flow_used_fixed/flow_all*20) #使用占比
    flow_percent = '{:.0%}'.format(flow_used_fixed/flow_all) #使用量百分比
    print(flow_percent)

    #转Bark字符串
    flow_daily = flow_left/float(time_reset)
    print(flow_daily)
    flow_daily = f"剩余日均: {flow_left/float(time_reset):.2f} {flow_all_unit}"
    flow_left = f"已用流量: {flow_used:.2f} {flow_used_unit}·{flow_all} GB"
    time_left = f"剩余天数: {time_left}天·{time_reset}天"
    #进度条
    s_jd = "流量进度: ["
    for number in range(1, flow_per):
        s_jd = s_jd + ">"
    for number in range(1, 20 - flow_per):
        s_jd = s_jd + "-"
    s_jd = s_jd + "]" + "·" + flow_percent

    deadline = "截止日期: " + time_y + "年" + time_m+ "月" + time_d + "日"
    ret = requests.get(f'{HEAD_BARK}/Mesl/{flow_daily}\n{flow_left}\n{s_jd}\n{time_left}\n{deadline}?icon={LOGO_MESL}&group=Mesl')

chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
login(driver)
lasttime, flow = goto_dashboard(driver)
extract_data(lasttime, flow)

driver.close()
driver.quit()