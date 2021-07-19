from collections import namedtuple
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st
import random
import time
import os
import SessionState

def get_session_state(rando):
    session_state = SessionState.get(random_number=random.random(), nsamples='', 
                                     generated=pd.DataFrame(columns=['Competitor','Similarity','Channels','Target Keywords']))
    return session_state

def cacherando():
    rando = random_number=random.random()
    return rando

def display_app_header(main_txt,sub_txt,is_sidebar = False):
    html_temp = f"""
    <h1 style = "color:black; text_align:left;"> {main_txt} </h2>
    <h2 style = "color:black; text_align:left;"> {sub_txt} </p>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(html_temp, unsafe_allow_html = True)
    else: 
        st.markdown(html_temp, unsafe_allow_html = True)
        
def display_side_panel_header(txt):
    st.sidebar.markdown(f'## {txt}')

def main():
    st.set_page_config(page_title='Manhattan City Layout Analysis') #layout='wide', initial_sidebar_state='auto'
    rando = cacherando()
    session_state = get_session_state(rando)
    sep = '<|endoftext|>'
    main_txt = """Manhattan City Layout Analysis"""
    sub_txt = "2021 NYU CUSP Capstone Project"
    display_app_header(main_txt,sub_txt,is_sidebar = False)
    manhattan_clusters = pd.read_csv('city_layouts_with_clustering.csv',index_col=0)
    
    ### SIDEBAR CONTENT ###
    display_side_panel_header("Menu")
    session_state.pages = st.sidebar.radio("Navigate Webapp", options=['Introduction','Clustering City Layouts','Blending City Layouts'])
#     display_side_panel_header("Configuration")
#     session_state.nsamples = st.sidebar.slider("Number of Competitors to Analyse: ", 1, v_nsamples, 1)
#     display_side_panel_header("Audience Profile")
#     session_state.audience_age = st.sidebar.slider("Audience Age Range: ", 16, 65, (26, 30))
#     session_state.audience_awareness = st.sidebar.selectbox("Audience Awareness: ", options=awareness_stages)
    
    ### Introduction ###
    if session_state.pages == 'Introduction':
        st.text("Introduction")

    ### Clustering City Layouts ###
    if session_state.pages == 'Clustering City Layouts':
        st.text("Clustering City Layouts")

    ### Blending City Layouts ###
    if session_state.pages == 'Blending City Layouts':
        st.text("Blending City Layouts")
        st.selectbox('Neighbourhood A', options=[i if i!=0 for i in manhattan_clusters.nta.unique()])
        
if __name__ == "__main__":
    main()
