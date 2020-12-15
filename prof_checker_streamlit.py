import os
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def prof_checker(sent):
    options = Options()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    

    driver.get("https://englishgrammar.pro/action.php")
    
    elem = driver.find_element_by_id("MT")
    elem.clear()
    elem.send_keys(sent)
    elem.submit()

    #driver.set_window_size(1400, 600)

    nodes = driver.find_element_by_xpath("""//*[@id="piechart"]/div/div[1]/div/*[name()='svg']/*[name()='g'][1]""")
    
    #chart = driver.find_elements_by_xpath("/html/body/div")

    result = nodes.text

    #chart_image = chart[0].screenshot_as_png
    
    driver.close()
    
    if 'C2' in result:
        #print('C2')
        return 'C1'
    elif 'C1' in result:
        #print('C1')
        return 'C1'
    elif 'B2' in result:
        #print('B2')
        return 'B2'
    elif 'B1' in result:
        #print('B1')
        return 'B1'
    elif 'A2' in result:
        #print('A2')
        return 'A2'
    elif 'A1' in result:
        #print('A1')
        return 'A1'
    else:
        return 'Not find'


def pos_tagger(sentence):
    options = Options()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    driver.get("http://ucrel-api.lancaster.ac.uk/claws/free.html")

    driver.refresh()
    
    driver.find_element_by_xpath("/html/body/div[2]/form/input[3]").click()

    elem = driver.find_element_by_xpath("/html/body/div[2]/form/textarea")

    elem.clear()

    elem.send_keys(sentence)

    elem.submit()

    nodes = driver.find_element_by_xpath("/html/body/div[2]/pre")
    
    tagged_text = nodes.text.replace("\n", "")

    driver.close()
    
    return tagged_text


def find_prof(sentence):
    tagged = pos_tagger(sentence)
    result = prof_checker(tagged)

    return result, tagged


st.title('Sentence Proficiency Level Checker')

s = st.text_input('Type a sentence in the box below', value='Hello world!')

prof, tagged = find_prof(s)

st.write(f'Prof Level: {prof}')

#st.image(chart)