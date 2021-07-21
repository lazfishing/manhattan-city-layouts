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

@st.cache(suppress_st_warning=True)
def latent_interpolation(A,B,manhattan_clusters,latent_num):
#    image = Image.open('interpolation/{}_{}_{}.png'.format(A,B,latent_num))
    image = Image.open('interpolation/test_{}.png'.format(latent_num))
    return image

def main():
    st.set_page_config(page_title='Manhattan City Layout Analysis') #layout='wide', initial_sidebar_state='auto'
    rando = cacherando()
    session_state = get_session_state(rando)
    sep = '<|endoftext|>'
    main_txt = """🏙 Manhattan City Layout Analysis"""
    manhattan_clusters = pd.read_csv('city_layouts_with_clustering.csv',index_col=0)
    
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
        NTA_GMM = gpd.read_file('data/manhattan_nta.geojson')
        NTA_GMM = NTA_GMM.to_crs('EPSG:4326')
        st.dataframe(NTA_GMM)
        
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=40.7831,
                longitude=-73.9712,
                zoom=10.5,
                pitch=35,
            ),
            layers=[
                pdk.Layer(
                    'GMMLayer',
                    data=NTA_GMM,
                    get_polygon='geometry',
                    get_fill_color="fill_color",
                    auto_highlight=True,
                    pickable=True
                ),
            ],
        ))

    ### Blending City Layouts ###
    if session_state.pages == 'Blending City Layouts':
        sub_txt = "Blending City Layouts"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        nta_A = st.selectbox('Neighbourhood A', options=manhattan_clusters.nta.unique()[:29])
        nta_B = st.selectbox('Neighbourhood B', options=manhattan_clusters.nta.unique()[:29])
        A = [i for i, val in enumerate(manhattan_clusters.nta.unique()==nta_A) if val][0]
        B = [i for i, val in enumerate(manhattan_clusters.nta.unique()==nta_B) if val][0]
        
        latent_num = st.slider('Drag the slider to see blending! Please be patient while the layouts load...',1,12)
        image = latent_interpolation(A,B,manhattan_clusters,latent_num-1)
        st.image(image, caption='Blending of {} and {} city layouts'.format(nta_A,nta_B))
        
if __name__ == "__main__":
    main()
