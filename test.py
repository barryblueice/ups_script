import platform
import time
from ping3 import ping
from dotenv import load_dotenv

import os
from loguru import logger

from datetime import datetime

today = (datetime.today()).strftime("%Y-%m-%d")
logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log", rotation="500 MB", retention="10 days", compression="zip")

def shutdown():
    try:
        reason="停电自动关机"
        if platform.system() == "Windows":
            if reason:
                os.system(f"shutdown /s /t 1 /c \"{reason}\"")
            else:
                os.system("shutdown /s /t 1")
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            os.system("shutdown now")
        logger.success('无法Ping到host，判定为关机状态，执行关机操作……')
    except Exception as e:
        logger.error(f'错误：{e}')

def ping_process(host):
    ping_result = []
    for i in range(1,6,1):
        result = ping(dest_addr=host,timeout=5)
        time.sleep(1)
        ping_result.append(result)
        
    if False in ping_result:
        logger.warning(f'无法Ping到host: {host}')
        return False
    
    logger.success('Ping事件已结束')
    
    return True

def initial_env():
    env_variables = {
        'power_off_num': '2',
        'host': '192.168.100.1'
    }

    with open(os.path.join(os.getcwd(),'.env'), 'w') as file:
        for key, value in env_variables.items():
            file.write(f'{key}={value}\n')

def get_env():
    load_dotenv()
    target_num = int(os.getenv('power_off_num'))
    logger.info(f'目标关机次数：{target_num}')
    host = os.getenv('host')
    logger.info(f'host地址：{host}')
    return target_num,host

if __name__ == "__main__":
    
    logger.info('开始运行')
    
    initial_env()
    target_num,host = get_env()
    
    num = 0
    
    while True:
        result = ping_process(host)
        if result == False:
            num += 1
            logger.warning(f'Ping事件执行失败（失败次数：{num}），当执行失败等于{target_num}次时将自动执行关机事件')
            
        else:
            num == 0
        if num == target_num:
            shutdown()
            # break
        time.sleep(60)