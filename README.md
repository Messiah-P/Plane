# Plane
# 简述
该项目以Mesl网站为实例，实现完整的数据爬取、处理和推送。

代码使用Selenium和ChromeDriver来自动化登录和提取数据，然后使用Bark发送消息到移动设备。

## 具体功能：

1. 导入必要的库和依赖项：requests、selenium、webdriver等。
2. 定义一些辅助函数，如：click()、send()、text()函数等，这些函数主要用于在页面上进行交互、获取文本等操作。
3. 定义一个login()函数，用于自动填充登录表单并登录到指定的网站。在此函数中，使用send()函数填写登录表单中的用户名和密码，然后使用click()函数点击登录按钮来完成登录过程。
4. 定义一个goto_dashboard()函数，用于进入控制面板并提取所需的数据。在此函数中，使用driver.get()方法加载页面，然后使用text()函数获取上次到期时间和已使用流量数据。在这里，使用selenium.webdriver.common.by.By类和driver.find_element()方法来查找所需的元素。
5. 定义一个extract_data()函数，用于解析和提取数据。在这个函数中，将上次到期时间和已使用流量进行解析，并计算出剩余天数、剩余日均、使用占比和使用量百分比等数据。
6. 最后，使用requests库发送HTTP请求，并将数据发送到Bark上，通过该应用程序推送到移动设备上。该请求中包含数据的各个部分，并使用格式化字符串构建完整的URL，然后使用requests.get()方法发送HTTP请求，将数据发送到Bark上。

## 主要的实现过程：

1. 配置ChromeDriver选项，包括加载策略、无头浏览器等。
2. 创建一个ChromeDriver实例。
3. 调用login()函数，自动登录到网站。
4. 调用goto_dashboard()函数，获取控制面板中的数据。
5. 调用extract_data()函数，解析和提取数据。
6. 使用requests库发送HTTP请求，将数据发送到Bark上。
7. 关闭ChromeDriver浏览器实例。
