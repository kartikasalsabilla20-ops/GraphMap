import streamlit as st
import folium
from streamlit_folium import st_folium
import networkx as nx
from haversine import haversine
import os
from PIL import Image
import matplotlib.pyplot as plt

# ===========================
# PAGE CONFIG
# ===========================
st.set_page_config(page_title="Java Graph Visualizer", layout="wide")

# ===========================
# SIDEBAR MENU
# ===========================
st.sidebar.title("Menu")
menu = st.sidebar.radio("Choose Menu", ["Profile", "Graph", "City Connection Map"])


# ===========================
# PAGE 1 – TEAM PROFILE 
# ===========================
if menu == "Profile":
    st.title("Team Profile")
    col1, col2, col3 = st.columns(3)

    def load_square_image(filename, width=250):
        here = os.path.dirname(__file__)
        path = os.path.join(here, filename)

        if os.path.exists(path):
            st.image(path, width=width)  # tidak gepeng!
        else:
            st.write("Image not found")

    # --- Member 1 ---
    with col1:
        load_square_image("kartika.jpg", width=250)
        st.write("**Name:** Kartika Putri Salsabila")
        st.write("**Program:** Actuarial Science")
        st.write("**Role:** Programmer")

    # --- Member 2 ---
    with col2:
        load_square_image("keisha.jpg", width=250)
        st.write("**Name:** Keisha Alisha Nara Rikin")
        st.write("**Program:** Actuarial Science")
        st.write("**Role:** Programmer")

    # --- Member 3 ---
    with col3:
        load_square_image("velove.jpg", width=250)
        st.write("**Name:** Velove Jennifer Suoth")
        st.write("**Program:** Actuarial Science")
        st.write("**Role:** Programmer")

    st.stop()
# ===========================
# PAGE 2 – GRAPH (Degree + Adjacency Matrix)
# ===========================
if menu == "Graph":
    import pandas as pd
    st.title("Graph Visualization – Degree & Adjacency Matrix")

    # input sederhana tanpa teks panjang
    col_a, col_b = st.columns([1,1])
    with col_a:
        n_nodes = st.number_input("", min_value=1, max_value=200, value=5, step=1, key="n_nodes")
    with col_b:
        n_edges = st.number_input("", min_value=0, max_value=1000, value=4, step=1, key="n_edges")

    # validasi maksimum edges untuk simple undirected graph
    max_edges = int(n_nodes * (n_nodes - 1) / 2)
    if n_edges > max_edges:
        n_edges = max_edges
        st.session_state["n_edges"] = n_edges  # sinkronkan UI value jika melebihi

    # build / rebuild graph otomatis saat salah satu input berubah
    import random
    G = nx.Graph()
    G.add_nodes_from(range(n_nodes))
    possible_edges = [(i, j) for i in range(n_nodes) for j in range(i+1, n_nodes)]
    random.shuffle(possible_edges)
    chosen_edges = possible_edges[:n_edges]
    G.add_edges_from(chosen_edges)

    # Visualisasi graph
    st.subheader("📌 Graph Visualization")
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(6,6))
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700, ax=ax)
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_labels(G, pos, font_color='white', ax=ax)
    ax.set_axis_off()
    st.pyplot(fig)

    # Degree
    st.subheader("📌 Degree of Each Node")
    degrees = dict(G.degree())
    deg_df = pd.DataFrame.from_dict(degrees, orient='index', columns=["degree"]).sort_index()
    deg_df.index.name = "node"
    st.dataframe(deg_df, use_container_width=True)

    # Adjacency Matrix
    st.subheader("📌 Adjacency Matrix")
    adj_matrix = nx.to_numpy_array(G, dtype=int)
    adj_df = pd.DataFrame(adj_matrix, index=range(n_nodes), columns=range(n_nodes))
    st.dataframe(adj_df, use_container_width=True)

    # Download adjacency matrix as CSV
    csv = adj_df.to_csv(index=True)
    st.download_button("Download adjacency matrix (CSV)", data=csv, file_name="adjacency_matrix.csv", mime="text/csv")

    st.stop()
