import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np

url = "http://127.0.0.1:7860"

class SqQueue(object):
    def __init__(self, maxsize):
        self.queue = np.zeros(maxsize)
        self.maxsize = maxsize
        self.front = 0

    # 如果队列未满，则在队尾插入元素，时间复杂度O(1)
    def EnQueue(self, data):
        self.queue[(self.front+1)%self.maxsize] = data
        self.front = (self.front+1)%self.maxsize
    
    def sum(self):
        sum = 0
        for i in range(self.maxsize):
            sum += self.queue[i]
            
        return sum

def autoGenerateImags(driver, prompt):

    print("new generation task: "+str(prompt))

    generateBotton = driver.find_element(by=By.ID, value="txt2img_generate")
    generatePromptBotton = driver.find_element(by=By.ID, value="paste")
    clearPromptBotton = driver.find_element(by=By.ID, value="txt2img_clear_prompt")
    saveBotton = driver.find_element(by=By.ID, value="save_txt2img")
    
    promptTop = driver.find_element(by=By.ID, value="txt2img_prompt")
    promptArea = promptTop.find_element(By.TAG_NAME,"textarea")
    
    clearPromptBotton.click()
    driver.switch_to.alert.accept()  # 捕获弹窗，点击取消
    driver.implicitly_wait(1)
    
    promptArea.send_keys(prompt)
    driver.implicitly_wait(1)
    generatePromptBotton.click()
    driver.implicitly_wait(1)
    generateBotton.click()
    driver.implicitly_wait(1)
    
    queue = SqQueue(10)
    flag = True
    while flag:

        response = requests.get(url=f'{url}/sdapi/v1/progress')
        r = response.json()
        ret = r.get("progress")
        queue.EnQueue(float(ret))
        driver.implicitly_wait(1)
        
        # # runing detected
        if queue.sum() > 0.1:
            
            while True:
                
                response = requests.get(url=f'{url}/sdapi/v1/progress')
                r = response.json()
                ret = r.get("progress")
                queue.EnQueue(float(ret))
                driver.implicitly_wait(3)
                
                print(queue.sum())
                
                # finish detected
                if abs(queue.sum() - 0) < 0.01: 
                    
                    driver.implicitly_wait(5)
                    saveBotton.click()
                    driver.implicitly_wait(5)
                    flag = False
                    break
    return

import os
path = os.path.join("./","prompts")
filenames=os.listdir(path)

# web driver
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
    
for file in filenames:
    filePath = os.path.join(path, file)
    
    f = open(filePath, "r")
    prompt = f.readlines()

    autoGenerateImags(driver, prompt)
    
    f.close()

driver.close()
        

