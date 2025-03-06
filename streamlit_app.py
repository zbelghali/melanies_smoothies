# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Custom Smoothie :banana:")
st.subheader("""
Choose the fruits you want in your custom Smoothie!""")
name_on_order =st.text_input("Name on Smoothie")
st.write(f'The name of the smoothie will be:{name_on_order}')

# Retrieve the Base64 encoded private key from Streamlit secrets
encoded_private_key = st.secrets["connections.snowflake"]["private_key"]

# Decode the Base64 string back to the original private key binary
private_key = base64.b64decode(encoded_private_key)

session = get_active_session()
cnx = st.connection("snowflake", type="snowflake", private_key=private_key, passphrase='snowflake')
session=cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

# st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredient_list:
    ingredient_sring=''
    for x in ingredient_list:
        ingredient_sring += x + ' '

    st.write(ingredient_sring)

    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients, name_on_order)
    values ('{ingredient_sring}', '{name_on_order}')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!')
