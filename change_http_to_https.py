def change_http_to_https_func(path_to_file,email,password):
    import os
    import pandas as pd
    from drop_duplicates_in_xlsx import drop_duplicates_and_prune_to_200
    import time
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver import ActionChains

    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options

    import pyautogui
    #commentary
    # #i added this commentary to github. me kinda plain9
    #another push another commit. How do i figure this thing out
    #path_to_file = "/media/alex/新加卷/OBS_Recordings_T/Data_science/Python/My_python_programs/IOYU/http_to_https"
    dirname = os.path.dirname ( path_to_file )
    os.chdir ( dirname )
    path_to_google_extension = os.path.join(path_to_file,"efcnkaeocmkpckkenjinmdgkbjhajoca.crx")


    chrome_options=Options()
    #chrome_options.add_argument( f"--load-extension={path_to_google_extension}")
    chrome_options.add_extension (path_to_google_extension  )


    pd.set_option ( "display.max_columns" , 10 )
    pd.set_option ( "display.width" , 1500 )
    pd.set_option ( "max_colwidth" , 500 )
    pd.set_option ( "display.colheader_justify" , "left" )


    results_df=pd.read_excel(os.path.join(path_to_file, 'https_with_dropped_duplicates.xlsx'))
    print(results_df)

    #time.sleep(10000)
    list_of_all_urls=drop_duplicates_and_prune_to_200()
    for url_of_the_course in list_of_all_urls:
        print('I am replacing buggy http and com at the following url:',url_of_the_course)
        driver = webdriver.Chrome (options = chrome_options, executable_path =  '/usr/local/bin/chromedriver')
        driver.get ( f'{url_of_the_course}' )
        driver.maximize_window ()
        print ( driver.title )

        driver.implicitly_wait ( 5 )
        driver.find_element_by_xpath ( "(//a[ text()='Вход' or text()='Log in'])[1]" ).click ()
        driver.find_element_by_id ( 'username' ).send_keys ( f'{email}' )
        driver.find_element_by_id ( 'password' ).send_keys ( f'{password}' )
        driver.find_element_by_id ( 'loginbtn' ).click ()
        driver.find_element_by_xpath ( "//a[@class='d-inline-block  dropdown-toggle icon-no-margin' and @id='action-menu-toggle-3']" ).click ()
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Редактировать настройки']"))).click()

        #path_to_file = "/media/alex/新加卷/OBS_Recordings_T/Data_science/Python/My_python_programs/IOYU/http_to_https"
        html_button1 = driver.find_element_by_xpath ( "(//button[@title='HTML'])[1]" )
        html_button1.click ()
        html_button2 = driver.find_element_by_xpath ( "(//button[@title='HTML'])[2]" )
        html_button2.click ()

        actions=ActionChains(driver)

        #We click on the link to be changed


        #driver.get ( f'{url_of_the_extension}' )
        #pyautogui.hotkey('ctrl','f')
        driver.execute_script('window.open("");')
        driver.switch_to.window(driver.window_handles[1])
        driver.get("chrome://extensions/shortcuts")
        driver.find_element_by_xpath("//body").click()

        actions.move_by_offset(0, 0).click().send_keys(Keys.TAB*4).perform()
        time.sleep(2)
        actions.key_down(Keys.CONTROL).send_keys("b").key_up(Keys.CONTROL).perform()
        driver.close()
        driver.switch_to.window ( driver.window_handles[0] )

        pyautogui.keyDown("ctrl")
        pyautogui.press("b")
        pyautogui.keyUp("ctrl")
        time.sleep(19)
        pyautogui.press(["tab","tab","tab","tab","space"])
        pyautogui.press("tab")
        pyautogui.write("http://173904.selcdn.com", interval = 0.01)
        pyautogui.press ( "tab" )
        pyautogui.write ( "https://173904.selcdn.ru", interval = 0.01 )
        pyautogui.press ( "tab",presses=6 )
        pyautogui.press ( "tab" )
        pyautogui.press("enter")

        WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,"//input[@type='submit' and @value='Сохранить и показать']"))).click()
        time.sleep(3)
        pyautogui.press ( "enter" )
        p = driver.page_source
        currentURL = driver.current_url
        if 'http://173904.selcdn.com' in p:
            print(f'I could not change the string at {currentURL}. Check it manually' )
        else:
            print (f'at {currentURL} everything is okey-dockey. We can move on')

        #time.sleep(10000)

        driver.quit()
