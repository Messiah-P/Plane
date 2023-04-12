import datetime
import yaml

# 读取YAML文件
with open("./config.yml", "r") as f:
    config = yaml.safe_load(f)

# 获取Paths配置
paths = config["paths"]
LOG_PATH = paths["log_path"]

# 链接配置
links = config["links"]
LOGO_MESL = links["logo_mesl"]
HEAD_BARK = links["head_bark"]
subscribe = links["subscribe"]

# 账号配置
links = config["account"]
ACCOUNT = links["email"]
PASSWORD = links["password"]

#其他信息
log_path = f"{LOG_PATH}/{datetime.datetime.now():%Y-%m-%d}.log"


