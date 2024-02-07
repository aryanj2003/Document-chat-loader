import streamlit as st
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate


# Function to get the final response from the LLama 2 model
def getLLaMAResponse(Input_Text, No_Of_Words, Blog_Style):
    #LLaMA 2 model
    llm = CTransformers(model = '')

# Use the direct link to the FontAwesome icon
Icon_Link = 'https://emoji.discourse-cdn.com/google/bar_chart.png?v=12'

st.set_page_config(Page_Title = "Generate Blogs", Page_Icon = Icon_Link, Layout = 'centered', Initial_Sidebar_State = 'collapsed')

st.head("Generate Blogs")

input_Text = st.text_input("Enter the Blog topic")

## Creating two more columns for additional 2 fields

col1, col2 = st.columns([5, 5])

with col1:
    no_Of_Words = st.text_input('No of words')

with col2:
    blog_Style = st.selectbox("Writing the blog for", ("Researchers", "Data Scientists", "Common people"), index = 0)

submit = st.button("Generate")

# Final response
if submit: 
    st.write(getLLaMAResponse(input_Text, no_Of_Words, blog_Style))
