#imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# get chromedriver
PATH = r"C:\Users\juanz\Documents\Python Scripts\chromedriver.exe"
driver = webdriver.Chrome(PATH)
# USER DATA
accountName = "Juan1608"
accountPassword = "rionovo420"

# setup website
website = "https://bestserverglobal.com"
driver.get(website)
# print title
print("Connected to ", driver.title)

fecharButton = driver.find_element_by_name("fechar")
if fecharButton:
    fecharButton.send_keys(Keys.RETURN)

print("closed double tc ad")

playNow = driver.find_element_by_name("Play Now")
if playNow:
    playNow.send_keys(Keys.RETURN)
print("went to login screen")

insertAccountName = driver.find_element_by_name("account_login")
insertAccountPassword = driver.find_element_by_name("password_login")
if insertAccountName:
    insertAccountName.send_keys(accountName)
    insertAccountPassword.send_keys(accountPassword)
    insertAccountPassword.send_keys(Keys.RETURN)
print("input credentials")
#driver.close()