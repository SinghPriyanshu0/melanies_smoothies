# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
import pandas as pd 

# Write directly to the app
st.title(":cup_with_straw: Customize your soomthie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie
    """
)

cnx=st.connection('snowflake')

search_on=pd_df.loc[pd_df["FRUIT_NAME"]== fruit_choosen,'SEARCH_ON'].Iloc[0]
st.write('The search value for ',fruit_choosen,'is',search_on,'.')

name_on_order = st.text_input("Name on Smoothie")
st.write("The name of your smoothie is ", name_on_order)
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients",
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string =''

    for x in ingredients_list:
        ingredients_string += x + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(x +' Nutrition infromation')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + x)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
   
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                             VALUES ('{ingredients_string}', '{name_on_order.strip()}')"""
        
    time_to_insert=st.button('Submit Order')
    if(time_to_insert):
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {name_on_order}', icon="✅")




        
