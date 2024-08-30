#imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import calendar
import regex

# get chromedriver
PATH = r"C:\Users\juanz\Documents\Python Scripts\chromedriver.exe"
driver = webdriver.Chrome(PATH)
wait = WebDriverWait(driver, 10)
# setup website
gmailCreate = "https://accounts.google.com/lifecycle/steps/signup/name?continue=https://accounts.google.com/ManageAccount?nc%3D1&dsh=S335930166:1703543757284651&flowEntry=SignUp&flowName=GlifWebSignIn&hl=en-GB&theme=glif&TL=AHNYTITTJfpZX7V5obzd_tNLSGYnQP_TB6jsUv5B9LgDPGtyVFoRIGr_GXK1haAM"
facebook = "https://facebook.com"
hotmailCreate = "https://signup.live.com/signup?cobrandid=90015&id=292841&contextid=1F090698DE71C8B7&opid=607E6A28AFF06187&bk=1703614859&sru=https://login.live.com/login.srf%3fcobrandid%3d90015%26id%3d292841%26cobrandid%3d90015%26id%3d292841%26contextid%3d1F090698DE71C8B7%26opid%3d607E6A28AFF06187%26mkt%3dEN-US%26lc%3d1033%26bk%3d1703614859%26uaid%3dbe0627e3fcea43a5b9944b3264917de5&uiflavor=web&lic=1&mkt=EN-US&lc=1033&uaid=be0627e3fcea43a5b9944b3264917de5"
hotmailLogin = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=19&ct=1703618335&rver=7.0.6738.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26nlp%3d1%26deeplink%3dowa%252f%26RpsCsrfState%3dbbfda581-9090-b177-27c0-42b441dab68d&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c"

personinfo = [
    #{
    #'firstname': "David",
    #'lastname': "Scarpelli",
    #'email': "Bestserverglobal@gmail.com",
    #'password': "babaca20",
    ##'picAddress': "C:\Users\juanz\Documents\Python Scripts\images\Juan_Fellipe_Braganca_Tello",
    #'gender': "male",
    #'review': "big text here"
    #},
    #{
    #'firstname': "Gary",
    #'lastname': "Serrano",
    #'email': "GarySerrano441990@outlook.com",
    #'password': "babaca20",
    #'dob': "4/4/1990",
    ##'picAddress': "C:\Users\juanz\Documents\Python Scripts\images\Juan_Fellipe_Braganca_Tello",
    #'gender': "male",
    #'review': "big text here"
    #},
    {
    'firstname': "Sergio",
    'lastname': "Oliveira",
    'email': "SergioOliveira331992@outlook.com",
    'password': "babaca20",
    'dob': "3/3/1992",
    #'picAddress': "C:\Users\juanz\Documents\Python Scripts\images\Juan_Fellipe_Braganca_Tello",
    'gender': "male",
    'review': "big text here"
    },
    
]

original_window = 0

def confirm_facebook(person, website):
    global original_window
    driver.switch_to.window(original_window)
    
    driver.get(hotmailLogin)


    # Wait for the new tab to finish loading content
    wait.until(EC.title_is("Sign in to Outlook"))
    # print title
    print("Connected to ", driver.title, person)
    time.sleep(1)
    
    email = wait.until(
        EC.presence_of_element_located((By.NAME, "loginfmt"))
    )
    email.send_keys(person['email'])
    
    next = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='submit'][@value='Next']"))
    )
    next.click()
    time.sleep(1)
    
    password = wait.until(
        EC.presence_of_element_located((By.NAME, "passwd"))
    )
    password.send_keys(person['password'])
    
    next2 = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='submit'][@value='Sign in']"))
    )
    next2.click()
    time.sleep(1)
    try:
        dontstaysignin = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='button'][@value='No']"))
        )
        dontstaysignin.click()
    except:
        continua = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='button'][@id='unified-consent-continue-button']"))
        )
        continua.click()
    time.sleep(5)
        
    titletext = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='AQAAAAAAAQABAAAAAAARLQAAAAA='][@tabindex='0']"))
    )
    fbtitle = " is your Facebook confirmation code"
    if fbtitle in titletext.text:
        print("true")
        test1 = titletext.text.replace(fbtitle,"")
        print("test1[1]",test1)
        regex_pattern = regex.compile(r"\D(\d{5})\D")
        matching_numbers = regex.findall(regex_pattern, test1)
        print(matching_numbers)
        driver.switch_to.window(original_window)
        fivecode = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text='][@dir='ltr']"))
        )
        fivecode.send_keys(matching_numbers[1])
        nextVerify = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Next='][@role='button']"))
        )
        nextVerify.click()
        time.sleep(1000)
    else:
        print("false")
    
            
def create_gmail_account(person, website):
    driver.get(website)
    # print title
    print("Connected to ", driver.title)
            
    #element = wait.until(
    #    EC.presence_of_element_located((By.LINK_TEXT, "Create new account"))
    #)
    #element.click()
    
    firstName = wait.until(
        EC.presence_of_element_located((By.NAME, "firstName"))
    )
    firstName.send_keys(person['firstname'])

    lastname = wait.until(
        EC.presence_of_element_located((By.NAME, "lastName"))
    )
    lastname.send_keys(person['lastname'])

    next = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button'][@jsname='LgbsSe']"))
    )
    next.click()
    time.sleep(5)
    day = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='tel'][@name='day']"))
    )
    #day = wait.until(
    #    EC.presence_of_element_located((By.ID, "day"))
    #)
    split_dob = person['dob'].split('/')
    day.send_keys(split_dob[0])
    
    month = Select(wait.until(
        EC.presence_of_element_located((By.XPATH, "//select[@id='month'][@jsname='YPqjbf']"))
    ))
    month.select_by_value(split_dob[1])
    
    year = wait.until(
        EC.presence_of_element_located((By.ID, "year"))
    )
    year.send_keys(split_dob[2])
    
    gender = Select(wait.until(
        EC.presence_of_element_located((By.ID, "gender"))
    ))
    
    if person['gender'] == "male":
        gender.select_by_value("2")
    else:
        gender.select_by_value("1")
        
    next2 = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button'][@jsname='LgbsSe']"))
    )
    next2.click()
    time.sleep(5)
    try:
        createOwnEmail = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='radio'][@data-value='custom']"))
        )
        createOwnEmail.click()
    except:
        pass   
    newEmail = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text'][@name='Username']"))
        )
    newEmail.send_keys(f"{person['firstname']}{person['lastname']}{split_dob[0]}{split_dob[1]}{split_dob[2]}")
    
    next3 = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='button'][@jsname='LgbsSe']"))
        )
    next3.click()
    time.sleep(5)
    
    password1 = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password'][@name='Passwd']"))
    )
    password1.send_keys(person['password'])
    
    password2 = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password'][@name='PasswdAgain']"))
    )
    password2.send_keys(person['password'])
    
    next4 = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='button'][@jsname='LgbsSe']"))
        )
    time.sleep(2)
    next4.click()
    time.sleep(5)
    driver.close()
    
def create_hotmail_account(person, website):
    driver.get(website)
    
    # print title
    print("Connected to ", driver.title)
            
    #element = wait.until(
    #    EC.presence_of_element_located((By.LINK_TEXT, "Create new account"))
    #)
    #element.click()
    split_dob = person['dob'].split('/')
    time.sleep(2)
    nextPage = wait.until(
        EC.presence_of_element_located((By.ID, "liveSwitch"))
    )
    nextPage.click()
    email = wait.until(
        EC.presence_of_element_located((By.NAME, "MemberName"))
    )
    email.send_keys(f"{person['firstname']}{person['lastname']}{split_dob[0]}{split_dob[1]}{split_dob[2]}")
    
    next = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='submit'][@id='iSignupAction']"))
    )
    next.click()
    time.sleep(1)
    passw = wait.until(
        EC.presence_of_element_located((By.NAME, "Password"))
    )
    passw.send_keys(person['password'])
   
    next2 = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='submit'][@id='iSignupAction']"))
    )
    next2.click()
    time.sleep(1)
    
    firstName = wait.until(
        EC.presence_of_element_located((By.ID, "FirstName"))
    )
    firstName.send_keys(person['firstname'])
    
    LastName = wait.until(
        EC.presence_of_element_located((By.ID, "LastName"))
    )
    LastName.send_keys(person['lastname'])
    
    next3 = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='submit'][@id='iSignupAction']"))
    )
    next3.click()
    time.sleep(1)
    
    day = wait.until(
        EC.presence_of_element_located((By.XPATH, "//select[@id='BirthDay'][@name='BirthDay']"))
    )
    day.send_keys(split_dob[1])
    
    month = wait.until(
        EC.presence_of_element_located((By.ID, "BirthMonth"))
    )
    month.send_keys(calendar.month_name[int(split_dob[0])])
    
    year = wait.until(
        EC.presence_of_element_located((By.ID, "BirthYear"))
    )
    year.send_keys(split_dob[2])
    next4 = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='submit'][@id='iSignupAction']"))
    )
    next4.click()
    time.sleep(20)
    global original_window
    
    original_window = driver.current_window_handle
    
    driver.execute_script(f"window.open('{facebook}')")
    wait.until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    time.sleep(5)
    
    create_facebook_account(person)
      
def create_facebook_account(person):
    # print title
    print("Connected to ", driver.title)
            
    element = wait.until(
        EC.presence_of_element_located((By.LINK_TEXT, "Create new account"))
    )
    element.click()
        
    firstName = wait.until(
        EC.presence_of_element_located((By.NAME, "firstname"))
    )
    firstName.send_keys(person['firstname'])

    lastname = wait.until(
        EC.presence_of_element_located((By.NAME, "lastname"))
    )
    lastname.send_keys(person['lastname'])


    email = wait.until(
        EC.presence_of_element_located((By.NAME, "reg_email__"))
    )
    email.send_keys(person['email'])
    
    reEnterEmail = wait.until(
        EC.presence_of_element_located((By.NAME, "reg_email_confirmation__"))
    )
    reEnterEmail.send_keys(person['email'])


    password = wait.until(
        EC.presence_of_element_located((By.NAME, "reg_passwd__"))
    )
    password.send_keys('babaca20')
    
    bdayYear = Select(wait.until(
        EC.presence_of_element_located((By.NAME, "birthday_year"))
    ))
    bdayYear.select_by_value("1990")
    
    if i['gender'] == "male":
        sex = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='radio'][@value='2']"))
        )
    else:
        sex = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='radio'][@value='1']"))
        )
    sex.click()
    
    completeForm = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit'][@name='websubmit']"))
    )
    completeForm.click()
    time.sleep(25)
    
    emailToSendCode = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text='][@dir='ltr']"))
        )
    emailToSendCode.send_keys(person['email'])
    time.sleep(5)
    titletext = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='AQAAAAAAAQABAAAAAAARLQAAAAA='][@tabindex='0']"))
    )
    if titletext.text =="Send login code":
        titletext.click()
        confirm_facebook(person, hotmailLogin)
    else:
        print("[ALERT]: confirm email code failed")
    
def createAccounts(person):
    create_hotmail_account(person, hotmailCreate)
    

for i in personinfo:
    #create email function
    createAccounts(i)
    #confirm_facebook(i, hotmailLogin)
    #create facebook account function
    #create_facebook_account(i, facebook)
    #wait until facebook account funtion is complete
    
    #create function to login to email and confirm email
    
    #wait for email verification function to be complete
    
    #sign in to facebook, insert photo, then search for company to review, post review
    
    #done
