from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import json
import pandas as pd
import shutil
from selenium.webdriver.firefox.options import Options
import datetime


options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'geckodriver.exe') #start headless firefox instance


driver.get("http://www.dce.com.cn/webquote/futures_quote_ajax?varietyid=JM") #go to website


wait = WebDriverWait(driver, timeout=20)
wait.until(lambda d : driver.find_element(By.CSS_SELECTOR, "body").text != "") #wait until text of website body is not empty

body = driver.find_element(By.CSS_SELECTOR, "body").text #store text from body

driver.quit() #close Firefox instance

dictionary = json.loads(body) #convert body text to dictionary


df = pd.DataFrame(dictionary) #create dataframe of dictionary

df2 = pd.DataFrame()
for value in df['contractQuote']: # filter out unneccessary info and add capture date
    if (str(value) == "nan"): break
    subDF = pd.DataFrame(value, index=[0])
    df2 = pd.concat([df2, subDF])
df = df2
df["captureTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open("LastCapture.html", "w", encoding="utf-8") as file: #create html file
    file.write(df2.to_html())

shutil.copy("LastCapture.html", "Archive\\Capture" + str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')) +".html")



