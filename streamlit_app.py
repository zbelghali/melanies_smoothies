# Import python packages
import base64
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Custom Smoothie :banana:")
st.subheader("""
Choose the fruits you want in your custom Smoothie!""")
name_on_order =st.text_input("Name on Smoothie")
st.write(f'The name of the smoothie will be:{name_on_order}')

# st.write(st.secrets)
# st.write(st.secrets["connections"]["snowflake"])


# Retrieve the Base64 encoded private key from Streamlit secrets
encoded_private_key = st.secrets["connections"]["snowflake"]["private_key"]

# Decode the Base64 string back to the original private key binary
private_key = base64.b64decode(encoded_private_key)

cnx = st.connection("snowflake", type="snowflake", private_key=private_key, passphrase='snowflake')
session=cnx.session()
