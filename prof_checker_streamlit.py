import os
import streamlit as st
import plotly.graph_objects as go
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
        pass


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

s = st.text_area('Type a sentence or sentences in the box below')

s_list = s.strip().split('\n')

profs = {'A1':0, 'A2':0, 'B1':0, 'B2':0, 'C1':0}

#prof, tagged = find_prof(s)

#st.write(f'Prof Level: {prof}')

if st.button('Submit'):

    if len(s_list) == 1:
        prof, tagged = find_prof(s_list[0])
        st.markdown("**Proficiency Level:** {0}".format(prof))
    elif len(s_list) == 0:
        st.markdown("*No entry found!*")
    else:
        with st.spinner('Processing...'):
            my_bar = st.progress(0)
            percent = 100/len(s_list)

            for idx, i in enumerate(s_list):
                if i.strip() == '':
                    continue
                else:
                    prof, tagged = find_prof(i)

                if prof == 'A1':
                    profs['A1'] += 1
                elif prof == 'A2':
                    profs['A2'] += 1
                elif prof == 'B1':
                    profs['B1'] += 1
                elif prof == 'B2':
                    profs['B2'] += 1
                elif prof == 'C1' or prof == 'C2':
                    profs['C1'] += 1
                else:
                    st.markdown("**Not Found:** _{0}_".format(i))

                my_bar.progress((percent/100) * (idx+1))
        #st.write(f'Prof Level: {prof}')
        #st.text(profs)

        labels = []
        values = []

        for k,v in profs.items():
            if v != 0:
                labels.append(k)
                values.append(v)


        fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                     insidetextorientation='radial',
                                     hovertemplate =
                                    '<b>Proficiency:</b>: %{label}'+
                                    '<br><b>Count:</b> %{value}<br>'+
                                    '<b>Percentage:</b> %{percent}'
                                    )])

        st.subheader('Proficiency Distribution')
        st.plotly_chart(fig, use_container_width=True)

#st.image(chart)