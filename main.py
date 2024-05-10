import os
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_vision_response,
                            embedding_model_response,
                            gemini_pro_response)

# Get the Working Directory
working_directory = os.path.dirname(os.path.abspath(__file__))

# Page Configuration
st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:
    selected = option_menu("Gemini AI",
                           ["ChatBot",
                            "ImageCaptioning",
                            "Embed Text",
                            "Ask me Anything"],
                           menu_icon="robot", icons=["chat-quote-fill",
                                                    "image-fill", "textarea-t", "patch-question-fill"],
                           default_index=0)


def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role

# Assuming load_gemini_pro_model is a function that loads your chat model
if selected == "ChatBot":
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # streamlit page title
    st.title("🤖 ChatBot")

    # Display the chat History
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # input field for user's message
    user_prompt = st.chat_input("Ask Gemini pro...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # display gemini chat-pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Image Captioning Page
if selected == "ImageCaptioning":

    #streamlit title page 
    st.title(" Snap Narrate")

    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):

        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)

        default_prompt = "Write a short caption for this image"

        #getting the response from gemini-pro-model
        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)

# text embedding page 
if selected == "Embed Text":

    st.title(" Embed text")

    #input text box
    input_text = st.text_area(label="", placeholder="Enter the text to get the embeddings")

    if st.button("Get Embeddings"):
        response = embedding_model_response(input_text)
        st.markdown(response)

# ask me a question
if selected == "Ask me Anything":

    st.title("Ask me a question")
    #text box to enter prompt
    user_prompt = st.text_area(label="", placeholder="Ask Gemini-Pro...")

    if st.button("Get an answer"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)