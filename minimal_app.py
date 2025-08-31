import streamlit as st

st.title("Africa-USA Trade Intelligence - Minimal Test")
st.write("If you can see this, Streamlit deployment is working!")

# Simple test of functionality
if st.button("Test Button"):
    st.success("Button works!")
    
st.write("Repository file structure:")
st.code("""
src/
  web_app/
    dashboard/
      main.py
""")

st.write("Main dashboard file path: `src/web_app/dashboard/main.py`")