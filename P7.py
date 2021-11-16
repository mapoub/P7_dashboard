import numpy as np
import streamlit as st
import pandas as pd 
import time
import matplotlib.pyplot as plt
import matplotlib
import json
import plotly.graph_objects as go

from urllib.request import urlopen
import requests


URL = "http://51.158.147.66"
API = "http://51.158.147.66:4567"



st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 600px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 600px;
        margin-left: -600px;
    }

    /*
    .reportview-container .main .block-container{{
        max-width: 100%;
    */
 
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
 
    .css-12oz5g7 {
        flex: 1 1 0%;
        width: 100%;
        padding: 6rem 1rem 10rem;
        max-width: 100%;
    }

    .css-1d391kg {
        background-color: rgb(240, 242, 246);
        background-attachment: fixed;
        flex-shrink: 0;
        height: 100vh;
        overflow: auto;
        padding: 2rem 1rem;
        position: relative;
        transition: margin-left 300ms ease 0s, box-shadow 300ms ease 0s;
        width: 21rem;
        z-index: 100;
        /* margin-left: 0px; */
    }

    </style>
    """,
    unsafe_allow_html=True,
)

#st.title("New Sidebar")
#st.sidebar.text("I'm here now.")




sb = st.sidebar 
sb.image(URL+'/P7/home.png')

# list des clients 
response = urlopen(API+"/api/clients")

list_id = response.read().decode('utf-8')
    
list_id = list_id.split(',')
#st.write('You selected:', a)

from streamlit.report_thread import get_report_ctx
#import st.ReportThread as ReportThread
#from streamlit.server.Server import Server


#from streamlit.server.Server import Server

#from streamlit.report_thread import get_report_ctx
#ctx = get_report_ctx()
#ctx.
#st.text(ctx.session_id)

#numclient = st.selectbox('Select a client ?',('',103625, 105091, 105134, 104584, 102887, 104691, 104381, 103575, 105973, 101041, 105630, 100591, 104417, 106735, 106438, 106216, 101903, 106087, 105248, 102174, 103830, 101259, 102506, 103658, 101398)) 
numclient = sb.selectbox('Select a client ? (103625: non solvable/105091: solvable)', (list_id)) 

#st.sidebar.text("(103625: non solvable/105091: solvable)")


#numclient = col2.selectbox('Select a client ?', (list_id)) 



sb.image(URL+'/P7/feature_importance.png')
#st.write('You selected:', option)

# data_load_state.text("")

# defining containers of the app
#header = st.container()
#dataset = st.container()
#eda = st.container()
#model_training = st.container()
#model_predict = st.container()





#grid = st.grid()
#for image, scores in images:
#row1 = grid.row()
#row1.write("1")
#row2 = grid.row()
#row2.write("1")


################################ 


# data_load_state = sb.text('Loading data...')



#st.image(URL+'/P7/home.png')

def newindictor(p_key):
    
    indicator_ = st.selectbox('Select a variable  ?',
                             ('','NAME_CONTRACT_TYPE', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'CNT_CHILDREN',
                            'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE',
                            'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH'), key=p_key) 
    
    if (indicator_):

        response = urlopen(API+"/api/indicator?id="+str(numclient)+"&indic="+ str(indicator_))
        id = response.read().decode('utf-8')
        st.image(URL+'/P7/'+id+'.png')
        
        newindictor(p_key+"1")
        
    return indicator_

#time.sleep(2)
#df = pd.read_json("http://51.158.147.66/comet/json.php")

#data_load_state.text("")

#st.dataframe(df)  # Same as st.write(df)
indicators = []


if (numclient !=""):


    col1, col2 = st.columns(2) 
    col3, col4 = st.columns(2) 

#df = pd.read_json("http://51.158.147.66/comet/predict.php?option="+ option)
#    st.write("http://51.158.147.66:7777/api/person/"+ option)
    #df = pd.read_json("http://51.158.147.66:7777/api/person/"+ option)
    #st.dataframe(df)  # Same as st.write(df)
    #response = urlopen("http://51.158.147.66:7777/api/person/"+ option)
   

    #response = urlopen("http://51.158.147.66:7878/api/person/client1")
    response = urlopen(API+"/api/client/"+ str(numclient) )

    data_json = json.loads(response.read())
    #st.write(data_json["score"])
    score = float(data_json["score"])
    proba0 = float(data_json["proba0"])
    seuil = float(data_json["seuil"])
    json = data_json["json"]
    
    # st.write(str(score) + ' '+ str(proba0))
    mondf = pd.read_json(json)
    #st.write(mondf.shape)
    #st.dataframe(mondf) 
    #st.table(mondf)
    sb.dataframe(mondf.T, 1000, 500)

    #response = urlopen("http://51.158.147.66:4567/api/client/"+ str(numclient))
    #data_load_state = st.text(response.read()) 
    
    #data_json = json.loads(response.read())
    #st.write(data_json["score"])

    ##################################
    
    score = int(round(proba0,0))
    
    
    
    if score < seuil:
        color = "red"
        message = "Avis défavorable"
    else:
        color = "green"
        message = "Avis favorable"
        
    fig4 = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = score,
        mode = "gauge+number",
        
        title = {'text': message},
        delta = {'reference': 100},
        gauge = {'axis': {'range': [None, 100]},
             'steps' : [
                 {'range': [0, seuil], 'color': "red"},
                 {'range': [seuil, 100], 'color': "green"}],
             'bar': {'color': "lime"},
             'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 1, 'value': seuil}}))

    fig4.update_layout(font = {'color': color, 'family': "Arial"})
    fig4.show()
    col1.plotly_chart(fig4, use_container_width=True)
    
#   st.write(message)
    
    #fig4.write_image("fig1.png")

    ##################################


    #score = data_json["score"]

#    ## if (option =="dsqdqsdqs"):
#    ##y = np.array([df.batterie[0], 100 - df.batterie[0]])
#    y = np.array([int(round(proba0,0)), 100 - int(round(proba0,0))])    
#    ## labels = 'plein', 'vide'
#    fig1, ax1 = plt.subplots()
#    ##ax1.pie(y, labels=labels, autopct='%1.1f%%', startangle=90)
#    ax1.pie(y,  autopct='%1.1f%%', startangle=90 , colors=['green','red'])

#    st.pyplot(fig1)


    col2.image(URL+'/P7/feature_importance_'+str(numclient)+'.png')
    
    #indicator = newindictor("key")
    #indicators.append(indicator)
    
    #json = data_json["variables2"]
    json = data_json["variables2"]
    bbbb = data_json["variables_princ"]
    # st.write(str(score) + ' '+ str(proba0))
    mondf = pd.read_json(json)
    
    #st.write(mondf.shape)
    #st.dataframe(mondf) 
    #st.table(mondf)
    
    # st.write(list(mondf[0]))
    aaaa=  list(mondf[0])
    #list_id = list_id.split(',')
#st.write('You selected:', a)


#numclient = st.selectbox('Select a client ?',('',103625, 105091, 105134, 104584, 102887, 104691, 104381, 103575, 105973, 101041, 105630, 100591, 104417, 106735, 106438, 106216, 101903, 106087, 105248, 102174, 103830, 101259, 102506, 103658, 101398)) 
    
    indicator = col3.selectbox(' Variables explicatives', (aaaa), key="1111") 
    
    
#    indicator = st.selectbox('Select a variable ?',
#                             ('','NAME_CONTRACT_TYPE', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'CNT_CHILDREN',
#                            'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE',
#                            'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH'), key="1") 
    
    #st.write('You selected:', indicator)
    
    if (indicator):
        
        response = urlopen(API+"/api/indicator?id="+str(numclient)+"&indic="+ str(indicator))
        id = response.read().decode('utf-8')
        col3.image(URL+'/P7/'+id+'.png')

#        newindictor("key")

    col3.write("[nomenclature]("+ URL + "/P7/nomenclature.html)")
   
    indicator2 = col4.selectbox(' Variables importantes', (bbbb), key="2222") 
    
    
#    indicator = st.selectbox('Select a variable ?',
#                             ('','NAME_CONTRACT_TYPE', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'CNT_CHILDREN',
#                            'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE',
#                            'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH'), key="1") 
    
    #st.write('You selected:', indicator)
    
    if (indicator2):
        
        response = urlopen(API+"/api/indicator?id="+str(numclient)+"&indic="+ str(indicator2))
        id = response.read().decode('utf-8')
        col4.image(URL+'/P7/'+id+'.png')

#        newindictor("key")

