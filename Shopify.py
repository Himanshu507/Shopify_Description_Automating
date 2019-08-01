import sys
import io
import os
import pyperclip
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException
import time


#Description Text here
startfile = open("start.txt","r")
startdes =  startfile.read()
startfile.close()
endfile = open("end.txt")
enddesc = endfile.read()
endfile.close()

driver = webdriver.Chrome(executable_path="C:\Users\Himanshu\Documents\Drivers\chromedriver.exe")
driver.get("https://accounts.shopify.com/store-login")
driver.find_element_by_xpath("//*[@id='shop_domain']").send_keys("casesdock.myshopify.com")
driver.find_element_by_xpath("//*[@id='body-content']/div[1]/div/form/button").click()
driver.find_element_by_xpath("//*[@id='account_email']").send_keys("store@gmail.com")
driver.find_element_by_xpath("//*[@id='js-login-form']/form/button").click()
driver.find_element_by_xpath("//*[@id='account_password']").send_keys("lamepassword")
driver.find_element_by_xpath("//*[@id='login_form']/button").click()
time.sleep(3)
driver.find_element_by_xpath("//*[@id='AppFrameNav']/nav/div[3]/ul[1]/li[3]/a/span").click()
wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Collections']"))).click()
time.sleep(5)
Collections = driver.find_elements(By.TAG_NAME, 'a')
# collection links start from 28 to number of collections
counter = 0
arr = list()
for i in range(42, len(Collections)):
    if i % 2 != 0:
        try:
            print i, "In ", Collections[i].text, " number of products are "
            inputprint = "Enter collection text = "
            with open("descriptions.txt",'r+') as des:
                for line in des:
                    if line.strip()=='startdescription':
                        break
                for line in des:
                    if line.strip()=='enddescription':
                        break
                    description = line
                des.close()
            n = 3
            nfirstlines = []
            with open("descriptions.txt") as f, open("descriptiontmp.txt", "w") as out:
                for x in xrange(n):
                    nfirstlines.append(next(f))
                for line in f:
                    out.write(line)
                    # NB : it seems that `os.rename()` complains on some systems
                    # if the destination file already exists.
                f.close()
                out.close()
                os.remove("descriptions.txt")
                os.rename("descriptiontmp.txt", "descriptions.txt")
            time.sleep(5)
            Collections[i].click()
            time.sleep(2)
            try:
                Show_More_Button = driver.find_element_by_xpath(
                    "//*[@id='AppFrameMain']/div/div/div[2]/form/div/div[1]/div[3]/div[4]/button")
                if Show_More_Button.is_displayed():
                    Show_More_Button.click()
                    time.sleep(2)
                    No_Of_Products = driver.find_elements_by_class_name("p_1Bu1z")
                    print len(No_Of_Products) 
                    for j in range(len(No_Of_Products)):
                        if j>9:
                            driver.find_element_by_xpath("//*[@id='AppFrameMain']/div/div/div[2]/form/div/div[1]/div[3]/div[4]/button").click()
                            time.sleep(5)
                            No_Of_Products = driver.find_elements_by_class_name("p_1Bu1z")
                            time.sleep(5)
                        No_Of_Products[j].click()
                        time.sleep(5)
                        driver.find_element_by_xpath(
                            "//*[@id='product-description_parent']/div[2]/div/div/div/button").click()
                        driver.find_element_by_xpath("//*[@id='product-description']").clear()
                        finaldescription = startdes+description+enddesc
                        pyperclip.copy(finaldescription)
                        driver.find_element_by_xpath("//*[@id='product-description']").send_keys(Keys.CONTROL+"v")
                        time.sleep(2)
                        driver.find_element_by_xpath(
                            "//*[@id='app']/div/div/div/div[4]/div/div[2]/div/div[2]/button").click()
                        time.sleep(8)
                        driver.back()
                        time.sleep(5)
                        No_Of_Products = driver.find_elements_by_class_name("p_1Bu1z")
                    #break


            except NoSuchElementException as nosuchelementexception:
                No_Of_Products = driver.find_elements_by_class_name("p_1Bu1z")
                print len(No_Of_Products)
                for j in range(len(No_Of_Products)):
                    if j > 9:
                        driver.find_element_by_xpath("//*[@id='AppFrameMain']/div/div/div[2]/form/div/div[1]/div[3]/div[4]/button").click()
                        time.sleep(5)
                        No_Of_Products = driver.find_elements_by_class_name("p_1Bu1z")
                    No_Of_Products[j].click()
                    time.sleep(5)
                    driver.find_element_by_xpath("//*[@id='product-description_parent']/div[2]/div/div/div/button").click()
                    driver.find_element_by_xpath("//*[@id='product-description']").clear()
                    finaldescription = startdes+description+enddesc
                    pyperclip.copy(finaldescription)
                    driver.find_element_by_xpath("//*[@id='product-description']").send_keys(Keys.CONTROL+"v")
                    time.sleep(2)
                    driver.find_element_by_xpath("//*[@id='app']/div/div/div/div[4]/div/div[2]/div/div[2]/button").click()
                    time.sleep(8)
                    driver.back()
                    time.sleep(5)
                    No_Of_Products = driver.find_elements_by_class_name("p_1Bu1z")

            driver.find_element_by_xpath("//span[text()='Collections']").click()
            time.sleep(5)
            Collections = driver.find_elements(By.TAG_NAME, 'a')
            #break
        except StaleElementReferenceException as s:
            print "Collection page exception", s
    #break
time.sleep(1)
driver.quit()
