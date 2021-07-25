from collections import namedtuple
import altair as alt
import math
import geopandas as gpd
import pandas as pd
import numpy as np
import streamlit as st
import random
import time
import os
import SessionState
from PIL import Image
import pydeck as pdk

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
    main_txt = """🏙 Manhattan City Layout Analysis"""
    manhattan_clusters = pd.read_csv('data/manhattan_city_layouts.csv',index_col=0)
    
    ### SIDEBAR CONTENT ###
    display_side_panel_header("Menu")
    session_state.pages = st.sidebar.radio("Navigate Webapp", options=['Introduction','Clustering City Layouts','Blending City Layouts'])
    
    ### Introduction ###
    if session_state.pages == 'Introduction':
        sub_txt = "2021 NYU CUSP Capstone Project"
        display_app_header(main_txt,sub_txt,is_sidebar = False)

    ### Clustering City Layouts ###
    if session_state.pages == 'Clustering City Layouts':
        sub_txt = "Clustering City Layouts"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        NTA_GMM = gpd.read_file('https://raw.githubusercontent.com/lazfishing/streamlit-example/master/data/manhattan_nta.geojson')
        col1, col2 = st.beta_columns(2)
        
        with col1:
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=40.7701,
                    longitude=-73.9812,
                    zoom=10.5,
                    pitch=35,
                ),
                layers=[
                    pdk.Layer(
                        "GeoJsonLayer",
                        NTA_GMM,
                        opacity=0.6,
                        stroked=True,
                        filled=True,
                        get_fill_color='[gmm_pca_color * 0.9, gmm_pca_color * 0.9, 255]',
                        auto_highlight=True,
                        pickable=True,
                    ),
                ],
                tooltip={
                    "html": 
                        "<b>{ntaname}</b> </br>PCA Component Score: {gmm_pca} </br>Normalized Deviation from Mean Score: {deviation}", 
                    "style": {
                        "backgroundColor": "black", 
                        "color": "white", 
                        "font-size": "12px"
                    } 
                },
            ))
            
        with col2:
            neighborhood = st.selectbox('Select a neighborhood to view', options=manhattan_clusters.nta.unique())

    ### Blending City Layouts ###
    if session_state.pages == 'Blending City Layouts':
        sub_txt = "Blending City Layouts"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        display_side_panel_header("Configuration")
        session_state.interpolate_setting = st.sidebar.radio("Settings for latent interpolation", options=['Overview','Individual transitions'])
        list1 = ['SoHo-TriBeCa-Civic Center-Little Italy','East Harlem North','Clinton','Upper West Side']
        list2 = ['Chinatown','Battery Park City-Lower Manhattan','Manhattanville','Stuyvesant Town-Cooper Village']
        nta_A = st.sidebar.selectbox('Neighborhood A', options=list1)
        nta_B = st.sidebar.selectbox('Neighborhood B', options=list2)

#         col1, col2 = st.beta_columns(2)
#         with col1:
#             nta_A = st.selectbox('Neighborhood A', options=list1)
#         with col2:
#             nta_B = st.selectbox('Neighborhood B', options=list2)
        A = [1,4,5,6][list1.index(nta_A)]
        B = 28 - [19,21,25,28][list2.index(nta_B)]
        
        if session_state.interpolate_setting == 'Overview':
            image = Image.open('set_interpolate/{}_{}.png'.format(A,B))
            st.image(image, caption='Blending of {} and {} city layouts'.format(nta_A,nta_B))
            
        else:
            latent_num = st.slider('Drag the slider to see blending! Please be patient while the layouts load...',1,12)
            image = Image.open('interpolation/{}_{}_{}.png'.format(A,B,latent_num-1))
            st.image(image, caption='Blending of {} and {} city layouts'.format(nta_A,nta_B))

if __name__ == "__main__":
    main()
