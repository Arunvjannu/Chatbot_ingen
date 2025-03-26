import pandas as pd
from fuzzywuzzy import fuzz
import streamlit as st

# Load CSV data
faq_data = pd.read_csv("faq_data_100.csv")
responses_data = pd.read_csv("responses_100.csv")

# Convert to dictionary
faq_dict = faq_data.groupby('intent')['example_question'].apply(list).to_dict()
responses_dict = pd.Series(responses_data.response.values, index=responses_data.intent).to_dict()

# Intent matcher
def find_intent(user_input, faq_dict):
    max_score = 0
    best_intent = None
    for intent, questions in faq_dict.items():
        for question in questions:
            score = fuzz.partial_ratio(user_input.lower(), question.lower())
            if score > max_score:
                max_score = score
                best_intent = intent
    return best_intent

# Response generator
def get_bot_response(user_input):
    intent = find_intent(user_input, faq_dict)
    if intent:
        return responses_dict.get(intent, "I'm not sure about that yet, but I'm learning!")
    else:
        return "I didn't understand that. Can you please rephrase?"

# Streamlit app UI
st.title("InGen Dynamics FAQ Chatbot 🤖")
st.write("Ask me anything about InGen Dynamics!")

user_input = st.text_input("You:")
if st.button("Ask"):
    if user_input:
        response = get_bot_response(user_input)
        st.text_area("InGen Bot:", value=response, height=100)
    else:
        st.warning("Please type something to ask!")
