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
import inference

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
    
def latent_interpolation(nta_A,nta_B):
    manhattan_clusters.nta.unique()
    A = int(np.linspace(1,50)[[i for i, val in enumerate(clusters.nta.unique()==nta_A) if val][0]])
    B = int(np.linspace(1,50)[[i for i, val in enumerate(clusters.nta.unique()==nta_B) if val][0]])
    
    latent0 = root_F_sample[A]
    latent1 = root_F_sample[B]

    steps = [latent0]+[latent0 + x*(latent1-latent0) for x in torch.linspace(0.1, 0.8, steps=10)]+[latent1]
    latent_steps = torch.stack(steps, dim=0)

    P0 = torch.reshape(root_P_list[A],(1,5))
    P1 = torch.reshape(root_P_list[B],(1,5))

    p_steps = [P0]+[P0 + x*(P1-P0) for x in torch.linspace(0.1, 0.8, steps=10)]+[P1]
    P_steps = torch.stack(p_steps, dim=0)

    # root_P = torch.Tensor([[0.4, 0.6, 0.8, 0.9, -0.4]])
    Box_Set_List = []
    for i in range(12):
        P_list, I_list, Set_list = inference_final_set(P_steps[i],latent_steps[i:i+1], 20)
        Set_list = Set_list.detach().numpy()
        box_set = get_box_2(Set_list[:,:2],Set_list[:,2:])
        Box_Set_List.append(box_set)
    plot_boxes2(Box_Set_List,2,6)

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
        nta_A = st.selectbox('Neighbourhood A', options=manhattan_clusters.nta.unique()[:29])
        nta_B = st.selectbox('Neighbourhood B', options=manhattan_clusters.nta.unique()[:29])
        latent_interpolation(nta_A,nta_B)
        
if __name__ == "__main__":
    main()
