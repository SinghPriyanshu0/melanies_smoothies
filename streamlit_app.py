# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col 

# Write directly to the app
st.title(":cup_with_straw: Customize your soomthie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie
    """
)

cnx=st.connection('snowflake')


name_on_order = st.text_input("Name on Smoothie")
st.write("The name of your smoothie is ", name_on_order)
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

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
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
   
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                             VALUES ('{ingredients_string}', '{name_on_order.strip()}')"""
        
    time_to_insert=st.button('Submit Order')
    if(time_to_insert):
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {name_on_order}', icon="✅")




        
