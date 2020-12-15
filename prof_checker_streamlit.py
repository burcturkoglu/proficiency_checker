import os
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

def prof_checker(sent):
    options = Options()
    #options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.binary_location = os.environ.get("FIREFOX_BIN")
    options.add_argument('--headless')
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--no-sandbox")
    #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    driver = webdriver.Firefox(executable_path=os.environ.get("GECKODRIVER_PATH"), options=options)
    
    driver.get("https://englishgrammar.pro/action.php")
    
    elem = driver.find_element_by_id("MT")
    elem.clear()
    elem.send_keys(sent)
    elem.submit()
    #nodes = driver.find_elements(By.XPATH, """//*[@id="piechart"]/div/div[1]/div/*[name()='svg']/*[name()='g'][1]/*[name()='g']/*[name()='g']/*[name()='text']""")

    nodes = driver.find_elements(By.XPATH, """//*[@id="piechart"]/div/div[1]/div/*[name()='svg']/*[name()='g'][1]""")
    
    result = nodes[0].text
    
    driver.close()
    
    if 'C2 ' in result:
        #print('C2')
        return 'C2'
    elif 'C1 ' in result:
        #print('C1')
        return 'C1'
    elif 'B2 ' in result:
        #print('B2')
        return 'B2'
    elif 'B1 ' in result:
        #print('B1')
        return 'B1'
    elif 'A2 ' in result:
        #print('A2')
        return 'A2'
    elif 'A1 ' in result:
        #print('A1')
        return 'A1'
    else:
        'Not find'


def pos_tagger(sentence):
    options = Options()
    #options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.binary_location = os.environ.get("FIREFOX_BIN")
    options.add_argument('--headless')
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--no-sandbox")
    #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    driver = webdriver.Firefox(executable_path=os.environ.get("GECKODRIVER_PATH"), options=options)
    
    driver.get("http://ucrel-api.lancaster.ac.uk/claws/free.html")

    driver.refresh()
    
    driver.find_element_by_xpath("/html/body/div[2]/form/input[3]").click()

    elem = driver.find_element_by_xpath("/html/body/div[2]/form/textarea")

    elem.clear()

    elem.send_keys(sentence)

    elem.submit()

    nodes = driver.find_element_by_xpath("/html/body/div[2]/pre")
    
    tagged_text = nodes.text

    driver.close()
    
    return tagged_text


def find_prof(sentence):
    tagged = pos_tagger(sentence)
    result = prof_checker(tagged)
    
    return result, tagged


import streamlit as st

st.title('Sentence Proficiency Level Checker')

s = st.text_input('Type a sentence in the box below')

prof, tagged = find_prof(s)

st.write(f'Your Input: {s}')

st.write(f'Prof Level: {prof}')

st.write(tagged)

