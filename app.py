import streamlit as st
import json
from PIL import Image
import os
import google.generativeai as genai

 
st.set_page_config(page_title="benGPT", page_icon="image4.png", layout="centered", initial_sidebar_state="auto") # Srujan choose this "Dororo AI" name

# Apply custom CSS for enhanced background and lighter sidebar color
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,pink, #f5f7fa, gray, #f5f7fa);
    color: #333;
}
[data-testid="stSidebar"] {
    background: linear-gradient(skyblue, blue) !important;
    color: white;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: white;
}
footer {
    visibility: hidden;
}
header {
    visibility: hidden;
}
body {
    font-family: "Source Sans Pro", sans-serif;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    font-size: 16px;
    border-radius: 8px;
    padding: 10px 24px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.stButton>button:hover {
    background-color: #45a049;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #2c3e50;
}
.stMarkdown p {
    color: #333;
}
.stDataFrame {
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.stProgress > div > div > div {
    background-color: #4CAF50;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.logo("image5.png", icon_image="image4.png")

GOOGLE_API_KEY = 'AIzaSyCJzha8fEyQg-0F6jxHnswpEreMzxisyQw' # Replace with Google_Api_Key 
genai.configure(api_key=GOOGLE_API_KEY)
geminiModel=genai.GenerativeModel("gemini-1.5-flash") 

if "history" not in st.session_state:
    st.session_state.history: list[dict] = []   # List for storing history messages

if "messages" not in st.session_state:
    st.session_state.messages: list[dict] = []   # List to store messages for main page

if "creativity" not in st.session_state:
        st.session_state.creativity = 0


def replace_key_in_dict_list(dict_list):
    """
    Takes a list of dictionaries and returns a new list of dictionaries where
    the key 'contents' is replaced with 'name parts'.
    
    :param dict_list: List of dictionaries, each containing a key 'contents'
    :return: New list of dictionaries with 'contents' replaced by 'name parts'
    """
    # Create a new list to hold the modified dictionaries
    new_list = []

    # Define the prefix to be stripped
    prefix1 = '**Me**:'
    prefix1_len = len(prefix1)
    prefix2 = '**benji**:'
    prefix2_len = len(prefix2)
    
    for d in dict_list:
        # Create a new dictionary for each entry
        new_dict = {}
        for key, value in d.items():
            # Replace 'contents' with 'name parts'
            if value == 'assistant':
                new_dict['role'] = "model"
            elif key == 'contents':
                # Remove the prefix if it exists
                if value.startswith(prefix1):
                    value = value[prefix1_len:].strip()
                elif value.startswith(prefix2):
                    value = value[prefix2_len:].strip()
                new_dict['parts'] = value
            else:
                new_dict[key] = value
        # Append the new dictionary to the new list
        new_list.append(new_dict)
    
    return new_list

chat = geminiModel.start_chat(history=replace_key_in_dict_list(st.session_state.messages))
  

# Main page
def ChatBot() -> None:
    ''' Stuff you see on Main page '''
    st.header("🎇 benGPT", divider="orange",)
    st.markdown(
        """
        **WELCOME TO THE WORLD OF PRO-HUMANOID INTELLIGENCE**

        benGPT will here to provide you with **accurate**, **informative**, and **insightful** responses to your queries. 
        

        
        """
    )

    # Load and display images
    image1 = Image.open("image3.png")
    st.image(image1, use_container_width=True, width=300)
    st.subheader(" Ask Dororo AI anything ")

    sidebar()

    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["contents"])

    # Chat 
    prompt: str = st.chat_input("Message Dodoro...")
    if prompt:
        prompt = f"**You**: {prompt}"
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "contents": prompt})

        response = chat.send_message(prompt, 
                                    generation_config=genai.types.GenerationConfig(
                                    candidate_count=1,
                                    temperature=st.session_state.creativity,
                                    ),)
  
        response = f"**Dororo**: \n{response.text}"

        with st.chat_message("assistant", avatar="image5.png"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "contents": response})

        st.session_state.history.extend([{"role": "user", "contents": prompt}, {"role": "assistant", "contents": response}])


def sidebar() -> None:
    ''' Stuff you see in the sidebar on the main page '''

    st.session_state.creativity = st.sidebar.slider(label="**Creativity**", 
                                                    min_value=0.0, max_value= 2.0, step=0.1,
                                                    value=float(st.session_state.creativity), 
                                                    help="This increases creativity of responce but also decreases accuracy")
    
    if st.sidebar.button("Clear", use_container_width=True):
        st.session_state.messages.clear()

    st.sidebar.markdown(
        """
        benGPT is a powerful AI assistant designed to help you with a variety of tasks.

        

        **Contact us:**
        * Email: benjaminukaimo@gmail.com
        * Phone: +2347067193071
        """
    )
    image4 = Image.open("image1.png")
    st.sidebar.image(image4, use_container_width=True)
    
    st.sidebar.button("Learn More")


# History page
def history() -> None:
    ''' Stuff you see on History page '''
    st.header("🕔 History", divider="red")

    # Sidebar for history page
    if st.sidebar.button("Delete", use_container_width=True):
        st.session_state.history.clear()
        st.session_state.messages.clear()

    if st.session_state.history:
        # Display Chat stored in st.session_state.history
        for message in st.session_state.history:
            with st.chat_message(message["role"]):
                st.markdown(message["contents"])
    else:
        st.subheader("Nothing to show.")

# Pages  
pages: list = []
main_page = st.Page(ChatBot, title="Dororo AI", icon=":material/add_circle:")
history_page = st.Page(history, title="History", icon=":material/add_circle:")


pages.extend([main_page, history_page])

pg = st.navigation(pages=pages)
pg.run()
