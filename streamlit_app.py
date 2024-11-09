import streamlit as st
from transformers import pipeline

# Load Hugging Face model for emotion classification
emotion_classifier = pipeline("text-classification", 
                              model="esuriddick/distilbert-base-uncased-finetuned-emotion",
                              return_all_scores=True)

# Define chatbot response function
def chatbot_response(user_message):
    result = emotion_classifier(user_message)[0]
    emotion = max(result, key=lambda x: x['score'])['label']
    
    # Generate response based on detected emotion
    responses = {
        "sadness": "I'm sorry you're feeling sad. Remember, it's okay to feel this way.",
        "joy": "I'm glad you're feeling happy! That's wonderful.",
        "anger": "It seems like you're feeling angry. Let's try to calm down together.",
        "fear": "It sounds like you're feeling anxious or scared. Take a deep breath.",
        "love": "It's great that you're feeling love! Can you tell me more about it?",
        "surprise": "Wow, you seem surprised! What happened?"
    }
    
    return responses.get(emotion, "I'm here to listen. Can you tell me more about how you're feeling?")

# Streamlit UI setup
st.title("Mental Health Companion for Teens")
st.write("A chatbot that helps teens manage anxiety, stress, and loneliness by offering real-time guidance and coping exercises.")

# User input text box
user_input = st.text_input("How are you feeling today?", "")

if user_input:
    response = chatbot_response(user_input)
    st.write(f"Chatbot: {response}")
