import streamlit as st
import random
from datetime import datetime
from gtts import gTTS
import os
import tempfile

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []

# Define coping strategies
coping_strategies = {
    "anxiety": [
        "Try deep breathing: Inhale for 4 counts, hold for 4, exhale for 4. Repeat 5 times.",
        "Practice the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
        "Write down your worries, then challenge each one with a positive counter-thought."
    ],
    "stress": [
        "Take a short walk or stretch for 5 minutes.",
        "Listen to calming music or nature sounds.",
        "Try progressive muscle relaxation: Tense and then relax each muscle group in your body."
    ],
    "loneliness": [
        "Reach out to a friend or family member, even if just for a quick chat.",
        "Join an online community related to one of your interests.",
        "Practice self-care: Do something you enjoy, like reading a book or watching a favorite show."
    ]
}

# Simple sentiment analysis function
def analyze_sentiment(text):
    positive_words = ['happy', 'good', 'great', 'awesome', 'excellent']
    negative_words = ['sad', 'bad', 'terrible', 'awful', 'worried', 'anxious', 'lonely']
    
    text = text.lower()
    if any(word in text for word in positive_words):
        return "positive"
    elif any(word in text for word in negative_words):
        return "negative"
    else:
        return "neutral"

# Chatbot response function
def get_response(user_input):
    sentiment = analyze_sentiment(user_input)
    
    if sentiment == "negative":
        if "anxious" in user_input or "worried" in user_input:
            return "I'm sorry you're feeling anxious. Let's try a coping strategy for anxiety.", "anxiety"
        elif "stressed" in user_input or "overwhelmed" in user_input:
            return "It sounds like you're under a lot of stress. How about we try a stress-relief technique?", "stress"
        elif "lonely" in user_input or "alone" in user_input:
            return "Feeling lonely can be tough. Let's explore some ways to connect with others.", "loneliness"
        else:
            return "I'm here to listen. Can you tell me more about what's bothering you?", "general"
    elif sentiment == "positive":
        return "I'm glad you're feeling positive! What's been going well for you?", "general"
    else:
        return "Thank you for sharing. How about we try a quick mood-boosting exercise?", "general"

# Text-to-speech function
def text_to_speech(text, language='en'):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(fp.name)
        st.audio(fp.name)

# Streamlit UI
st.title("🌟 Teen Talk: Mental Health Companion")

# Sidebar for mood tracking
with st.sidebar:
    st.header("🎭 Mood Tracker")
    mood = st.select_slider("How are you feeling right now?", 
                            options=["😞", "😟", "😐", "🙂", "😄"])
    if st.button("Save Mood"):
        st.session_state.mood_data.append({"date": datetime.now(), "mood": mood})
        st.success("Mood saved!")
    
    if st.button("View Mood History"):
        if st.session_state.mood_data:
            moods = [entry["mood"] for entry in st.session_state.mood_data]
            st.line_chart(moods)
        else:
            st.info("No mood data available yet. Start tracking your mood!")

# Main chat interface
st.header("💬 Chat with Teen Talk")
user_input = st.text_input("How are you feeling? Share what's on your mind:")

if user_input:
    response, category = get_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Teen Talk", response))
    
    # Text-to-speech for the response
    text_to_speech(response)
    
    if category in coping_strategies:
        strategy = random.choice(coping_strategies[category])
        st.session_state.chat_history.append(("Teen Talk", f"Here's a coping strategy you can try: {strategy}"))
        # Text-to-speech for the strategy
        text_to_speech(strategy)

# Display chat history
chat_container = st.container()
with chat_container:
    for i, (role, message) in enumerate(st.session_state.chat_history):
        if role == "You":
            st.text_area("You:", value=message, height=70, key=f"user_message_{i}")
        else:
            st.text_area("Teen Talk:", value=message, height=100, key=f"bot_message_{i}")

# Coping exercises section
st.header("🧘‍♀️ Coping Exercises")
exercise_type = st.selectbox("Choose a type of exercise:", ["Breathing", "Mindfulness", "Positive Affirmations"])

if exercise_type == "Breathing":
    exercise = "Try this 4-7-8 breathing technique: Inhale quietly through your nose for 4 seconds. Hold your breath for 7 seconds. Exhale completely through your mouth for 8 seconds. Repeat this cycle 4 times."
elif exercise_type == "Mindfulness":
    exercise = "Practice this 1-minute mindfulness exercise: Sit comfortably and close your eyes. Focus on your breathing, noticing each inhale and exhale. If your mind wanders, gently bring your attention back to your breath. Continue for one minute."
elif exercise_type == "Positive Affirmations":
    affirmations = [
        "I am capable of handling whatever comes my way.",
        "I choose to focus on what I can control.",
        "I am worthy of love and respect.",
        "My feelings are valid, and it's okay to express them.",
        "I am growing and learning every day."
    ]
    exercise = f"Repeat this affirmation to yourself: {random.choice(affirmations)}"

st.write(exercise)
text_to_speech(exercise)

st.markdown("---")
st.caption("Remember, you're not alone. If you need professional help, please reach out to a trusted adult or mental health professional.")
