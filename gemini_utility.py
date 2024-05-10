import os
import json

import google.generativeai as genai

#Get the Working Directory
working_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = f"{working_directory}\config.json"

config_data = json.load(open(config_file_path))

#loading api key
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]
print(GOOGLE_API_KEY)

#configure google.generativeai with API Key
genai.configure(api_key=GOOGLE_API_KEY)

#function to ]oad Gemini Pro Model
def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

#function for Image Captioning
def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel('gemini-pro-vision')
    response = gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result

#function to get embedding for text
def embedding_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model=embedding_model, 
                                    content=input_text,
                                    task_type="retrieval_document")

    embedding_list =  embedding["embedding"]               
    return embedding_list

#function to get a response from gemini-pro LLM
def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result