#!/usr/bin/env python
# coding: utf-8

import time
start_time=time.time()
import getpass
import re
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import os
import put_list_into_xl
import check_status_code_of_https
from selenium.webdriver.chrome.options import Options
from change_http_to_https import change_http_to_https_func

chrome_options=Options()
chrome_options.add_argument('--headless')
from empty_result_xlsx_files import empty_result_xlsx_files

email=input ('what is your email with which to login onto itempuniversity.com? ')


password=getpass.getpass (prompt='what is your password? ' )


url_of_the_course=input ('what is the url of the course on itemuniversity.com with which you want to work? ')

driver=webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)

driver.get(f'{url_of_the_course}')
driver.maximize_window()
#check if the course you want to work with is really the course the program has found
print ('The title of the course is ', driver.title)
driver.implicitly_wait(2)

driver.find_element_by_xpath("(//a[ text()='Вход' or text()='Log in'])[1]").click()
driver.find_element_by_id('username').send_keys(f'{email}')
driver.find_element_by_id('password').send_keys(f'{password}')
driver.find_element_by_id('loginbtn').click()
button_text=driver.find_element_by_xpath("//button[@type='submit' and @class='btn btn-primary']").get_attribute('innerHTML')
if button_text=='Режим редактирования':
    driver.find_element_by_xpath("//button[@type='submit' and @class='btn btn-primary']").click()
links_with_http=driver.find_elements_by_xpath("//a[@href[contains(., 'http:')]]")
path_to_file="/media/alex/新加卷/OBS_Recordings_T/Data_science/Python/My_python_programs/IOYU/http_to_https"

#here is a list of all elements on a chosen course like pages, tests,
different_elements=driver.find_elements_by_xpath("//a[@class='aalink' or @class='aalink dimmed']")
len(different_elements)
print(f'I found {len(different_elements)} elements in the course which I will check')

#first_element_in_a_course=driver.find_element_by_xpath("//li[contains(@class,'activity')]")
first_element_in_a_course=driver.find_element_by_xpath("(//a[@class='aalink' or @class='aalink dimmed'])[1]").get_attribute('href')
print(first_element_in_a_course)

first_element_in_a_course_plus_forceview=first_element_in_a_course+"&forceview=1"
driver.get(f"{first_element_in_a_course_plus_forceview}")


dirname=os.path.dirname(path_to_file)
#I am changing the working directory into which where this file is located
os.chdir(dirname)

#----------------------------------------------------

print ('now I will go every page in the course and find buggy http link. Then I will list them. ')

u=0
list_of_tuple_of_link_and_code=[]
try:
    for i in range (0, len(different_elements)):
        print ( f'There are {len(different_elements)} elements on the course you provided')
        print ('I am at element', i)
        try:
            #We find all buggy http in attribute that match the criteria
            #for i in range (0, len(different_elements)):
            p=driver.page_source
            l=driver.find_element(By.XPATH, "(//a[ancestor::div[@id='page-navbar']])[last()]").get_attribute('href')
            currentURL=driver.current_url
            if 'http://173904.selcdn.com' in p:
                print('\nI found some buggy http addresses at ', l)
                print ('I found some buggy http addresses at the current URL', currentURL, '************\n')
                list_of_regex_strings_http=re.findall(r'http://173904\.selcdn\.com.*?\.(?:mp[34]|doc|rar|docx|pdf|zip)',p)

                print('list of reg ex strings is\n\n')
                print(*list_of_regex_strings_http, sep='\n')

                print ("Now I am going to check if the status_code is 200\n")
                for n in list_of_regex_strings_http:
                    print ("I am checking the following url:\n", n)
                    print ("Current Page Title is :" ,driver.title)

                    response=requests.head(n)
                    code=response.status_code
                    print("code=", code)
                    print('Now I am writing the buggy http and the status code to a worksheet')

                    tuple_of_link_and_code=(currentURL,n,code)
                    print('tuple_of_link_and_code=',tuple_of_link_and_code)
                    list_of_tuple_of_link_and_code.append(tuple_of_link_and_code)

                    print('list_of_tuple_of_link_and_code[u]', list_of_tuple_of_link_and_code[u],'\n')
                    print('the whole list_of_tuple_of_link_and_code[u]', *list_of_tuple_of_link_and_code, sep='\n')
                    #print (f"list_of_tuple_of_link_and_code[{u}]=", list_of_tuple_of_link_and_code[u])

                    u=u+1
                    print ( 'number of buggy http strings at this step in course=' , u )
                    #ws.cell(row=list_of_regex_strings_http.index(n)+1,column=1).value=n
                    #ws.cell(row=list_of_regex_strings_http.index(n) + 1, column=2).value = code

                    time.sleep(0.5)


                print('\n')
                print (u)
            else:
                pass
                #print ("I could not find the string at", l)

        except Exception as e:
            #buggy_element=driver.find_element(By.XPATH, "//*[contains(@href,'http:') and contains(@href,'.mp3')]")
            print ('There was some error', Exception.__str__)
            print(e)
            #time.sleep(0.5)

        finally:
            next_element=driver.find_element(By.XPATH,"//a[@id='next-activity-link']")
            next_element.click()

except NoSuchElementException:
    driver.find_element_by_xpath("//ol[@class='breadcrumb']/li[3]/a").click()

empty_result_xlsx_files(path_to_file)
put_list_into_xl.put_list_into_xl_func(list_of_tuple_of_link_and_code,path_to_file)
check_status_code_of_https.check_status_code_of_https(path_to_file)


driver.quit()
print('execution time in seconds=', time.time()-start_time)
print('\nPlease check http_to_https_results_with_https_sheet.xlsx file in the same directory.'
      'If you agree with the links there, then run change_http_to_https.py file\n')
answer=input (f'Do you want me to execute changing of http into https and com into ru at the course {url_of_the_course} ? Type y or n=')
if answer=='y':
    change_http_to_https_func(path_to_file,email,password)
elif answer=='n':
    print ('Well suit yourself. ')
else:
    print ('You typed neither "y" nor "n", so what am I supposed to do? ')
#with open("/media/alex/新加卷/OBS_Recordings_T/Data_science/Python/My_python_programs/IOYU/list_of_all_http.docx", 'w') as f:
#    f.write(cap.stdout)
# In[ ]:




