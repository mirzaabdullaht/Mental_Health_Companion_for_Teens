# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E6VWBt0jdrfhNBa1ygggvcgZ9SZe7eQC
"""

!pip install transformers torch gradio streamlit

from transformers import pipeline

# Load the Hugging Face model for emotion classification
emotion_classifier = pipeline("text-classification",
                              model="esuriddick/distilbert-base-uncased-finetuned-emotion",
                              return_all_scores=True)

# Define the chatbot response function
def chatbot_response(user_message):
    result = emotion_classifier(user_message)[0]
    emotion = max(result, key=lambda x: x['score'])['label']

    # Generate a response based on the detected emotion
    responses = {
        "sadness": "I'm sorry you're feeling sad. Remember, it's okay to feel this way.",
        "joy": "I'm glad you're feeling happy! That's wonderful.",
        "anger": "It seems like you're feeling angry. Let's try to calm down together.",
        "fear": "It sounds like you're feeling anxious or scared. Take a deep breath.",
        "love": "It's great that you're feeling love! Can you tell me more about it?",
        "surprise": "Wow, you seem surprised! What happened?"
    }

    return responses.get(emotion, "I'm here to listen. Can you tell me more about how you're feeling?")

# Test the chatbot
user_input = "I'm feeling really sad today"
response = chatbot_response(user_input)
print(f"Chatbot: {response}")