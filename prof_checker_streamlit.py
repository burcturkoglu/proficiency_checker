import os, io
import streamlit as st
import plotly.graph_objects as go
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageChops

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

    driver.set_window_size(1400, 600)

    nodes = driver.find_element_by_xpath("""//*[@id="piechart"]/div/div[1]/div/*[name()='svg']/*[name()='g'][1]""")
    
    result = nodes.text

    text = driver.find_elements_by_xpath("//*[@id=\"demo\"]")

    try:
        text_image = text[0].screenshot_as_png

    except:
        text_image = None
    
    driver.close()
    
    if 'C2' in result:
        #print('C2')
        proficiency = 'C2'
    elif 'C1' in result:
        #print('C1')
        proficiency = 'C1'
    elif 'B2' in result:
        #print('B2')
        proficiency = 'B2'
    elif 'B1' in result:
        #print('B1')
        proficiency = 'B1'
    elif 'A2' in result:
        #print('A2')
        proficiency = 'A2'
    elif 'A1' in result:
        #print('A1')
        proficiency = 'A1'
    else:
        proficiency = None

    return proficiency, text_image


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
    prof, text = prof_checker(tagged)

    return prof, text

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("style.css")

st.title('Sentence Proficiency Level Checker')

s = st.text_area('Type a sentence or sentences in the box below')

s_list = s.strip().split('\n')

profs = {'A1':0, 'A2':0, 'B1':0, 'B2':0, 'C1':0, 'C2':0}

if st.button('Submit'):

    if len(s_list) == 1:
        prof, text = find_prof(s_list[0])
        st.markdown("**Proficiency Level:** {0}".format(prof))
        
        st.image('./proficiency_legend.png', use_column_width=True)
        st.image(text, use_column_width=True)


    elif len(s_list) == 0:
        st.markdown("*No entry found!*")

    else:
        text_images = []

        with st.spinner('Processing...'):
            my_bar = st.progress(0)
            percent = 100/len(s_list)

            for idx, i in enumerate(s_list):
                if i.strip() == '':
                    continue
                else:
                    prof, text = find_prof(i)

                if prof == 'A1':
                    profs['A1'] += 1
                    text_images.append(text)
                elif prof == 'A2':
                    profs['A2'] += 1
                    text_images.append(text)
                elif prof == 'B1':
                    profs['B1'] += 1
                    text_images.append(text)
                elif prof == 'B2':
                    profs['B2'] += 1
                    text_images.append(text)
                elif prof == 'C1':
                    profs['C1'] += 1
                    text_images.append(text)
                elif prof == 'C2':
                    profs['C2'] += 1
                    text_images.append(text)
                else:
                    st.markdown("**Not Found:** _{0}_".format(i))

                my_bar.progress(round((percent/100) * (idx+1), 2))

        labels = []
        values = []

        for k,v in profs.items():
            if v != 0:
                labels.append(k)
                values.append(v)

        with st.beta_expander("See the proficiency level of each sentence"):
            st.image("./proficiency_legend.png", use_column_width=True)
            for m in text_images:
                st.markdown('<hr>', unsafe_allow_html=True)
                st.image(m, use_column_width=True)
                

        st.text("\n")

        st.markdown("**Proficiency Levels and Distribution**")
        col1, col2 = st.beta_columns([1, 4])

        for g, h in zip(labels, values):
            col1.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**{0}**: {1}%".format(g, round(100*h/sum(profs.values()), 2)))


        colors = {'A1':'#d9be99', 'A2':'#a7d9d9', 'B1':'#d48181', 'B2':'#78dc7e', 'C1':'#7378fa', 'C2':'#ff60fa'}

        layout = go.Layout(
                  margin=go.layout.Margin(
                        t=0  #top margin
                    )
                )

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                     insidetextorientation='radial',
                                     marker_colors=[colors[i] for i in labels],
                                     hovertemplate =
                                    '<b>Proficiency:</b>: %{label}'+
                                    '<br><b>Count:</b> %{value}<br>'+
                                    '<b>Percentage:</b> %{percent}'
                                    )], layout=layout)

        col2.plotly_chart(fig, use_container_width=True)