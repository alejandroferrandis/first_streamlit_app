import streamlit as st
import pandas as pd

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

st.title('My parents New Healthy Diner')

st.header('Breakfast Menu')
st.text('🥣Omega 3 & Blueberry Oatmeal')
st.text('🥗Kale, Spinach & Rocket Smoothie')
st.text('🐔Hard-Boiled Free-Range Egg')
st.text('🥑🍞Avocado toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
st.dataframe(my_fruit_list)