import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

######################################################## CONNECTIONS ##########################################################

# my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
# my_cur = my_cnx.cursor()
## my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()") ## test if connection works
# my_cur.execute("select * from fruit_load_list")
## my_data_row = my_cur.fetchone() # to get one row
# my_data_rows = my_cur.fetchall()

########################################################### FUNCTIONS ##########################################################

def get_fruityvice_data(this_fruit_choice):
    # st.write('The user entered ', fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # Setting up response as dataframe
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit * "')")
        return "Thanks for adding " + new_fruit

########################################################### DATA ##########################################################

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# TITLE
st.title('My parents New Healthy Diner')

st.header('Breakfast Favourites')
st.text('🥣Omega 3 & Blueberry Oatmeal')
st.text('🥗Kale, Spinach & Rocket Smoothie')
st.text('🐔Hard-Boiled Free-Range Egg')
st.text('🥑🍞Avocado toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")
# st.text(fruityvice_response.json()) # Writes data to the screen

try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error("Please select a fruit to get the information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        st.dataframe(back_from_function)

except URLError as e:
    st.error()

st.header("The fruit load list contains")

# Add a button to load the fruit
if st.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    st.dataframe(my_data_rows)

# Allow the user to add a fruit to the list

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the List'):
    my_cnx = snowflake.connect(**st.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    st.text(back_from_function)

