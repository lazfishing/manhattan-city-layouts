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
    df_tsne = pd.read_csv('data/city_tsne.csv',index_col=0)
    df_tsne.cluster = [str(int(c)) for c in df_tsne.cluster]
    
    ### SIDEBAR CONTENT ###
    display_side_panel_header("Menu")
    session_state.pages = st.sidebar.radio("Navigate Webapp", options=['Introduction','Clustering City Layouts','Neighborhood Analysis','Blending City Layouts'])
    
    ### Introduction ###
    if session_state.pages == 'Introduction':
        sub_txt = "2021 NYU CUSP Capstone Project"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        
    ### Clustering City Layouts ###
    if session_state.pages == 'Clustering City Layouts':
        sub_txt = "Clustering City Layouts"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        clusterSelect = st.multiselect('Select cluster(s) to view:',options=[str(c) for c in range(11)],default=[str(c) for c in range(11)])
        c = alt.Chart(df_tsne, height=600).mark_circle(size=10).encode(x='Dim1', y='Dim2',
                                                                color='cluster', 
                                                                tooltip=['cluster']).transform_filter(
            alt.FieldOneOfPredicate(field='cluster', oneOf=clusterSelect))
        st.altair_chart(c, use_container_width=True)


    ### Neighborhood Analysis ###
    if session_state.pages == 'Neighborhood Analysis':
        sub_txt = "Neighborhood Analysis"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        NTA_GMM = gpd.read_file('https://raw.githubusercontent.com/lazfishing/streamlit-example/master/data/manhattan_nta.geojson')
        display_side_panel_header("Configuration")
        session_state.viz_setting = st.sidebar.radio("Settings for visualization", options=['Top PCA component','Deviation from Manhattan style'])
        neighborhood = st.sidebar.selectbox('Select a neighborhood to view', options=manhattan_clusters.nta.unique())
        nhood = list(manhattan_clusters.nta.unique()).index(neighborhood)

        PCALayer =  pdk.Layer(
            "GeoJsonLayer",
            NTA_GMM,
            opacity=0.6,
            stroked=True,
            filled=True,
            get_fill_color='[gmm_pca_color * 0.9, 150, 255]',
            auto_highlight=True,
            pickable=True)
        
        DeviationLayer =  pdk.Layer(
            "GeoJsonLayer",
            NTA_GMM,
            opacity=0.6,
            stroked=True,
            filled=True,
            get_fill_color='[150, deviation * 255, 255]',
            auto_highlight=True,
            pickable=True)
        
        tooltip = {
            "html": "<b>{ntaname}</b> </br>PCA Component Score: {gmm_pca} </br>Normalized Deviation from Mean Score: {deviation}", 
            "style": {
                "backgroundColor": "black", 
                "color": "white", 
                "font-size": "12px"
            }}
        
        if session_state.viz_setting == 'Top PCA component':
            layers = [PCALayer]
        else:
            layers = [DeviationLayer]
        
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=40.7701,
                longitude=-73.9812,
                zoom=10,
                pitch=25,
                height=300,
                bearing=-20,
            ),
            layers=layers,
            tooltip=tooltip
        ))
        
        col1, col2, col3 = st.beta_columns(3)
            
        with col1:
            image = Image.open('indiv_layouts/{}.png'.format(nhood))
            st.image(image, caption='City layout extracted from {}'.format(neighborhood))
        
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
