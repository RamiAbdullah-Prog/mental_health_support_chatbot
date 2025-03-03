import streamlit as st
from langchain_ollama import OllamaLLM
from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon if not already downloaded
# nltk.download('vader_lexicon')

# App title with a robot emoji
st.title("🪴 Mental Health Support Chatbot")

# Session setup to store conversations
if "conversations" not in st.session_state:
    st.session_state.conversations = []
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = {
        "id": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": [],
        "title": "New Conversation"
    }

# Function to generate an automatic title for the conversation
def generate_conversation_title(messages):
    if not messages:
        return "New Conversation"
    first_user_message = next((msg["content"] for msg in messages if msg["role"] == "user"), None)
    if first_user_message:
        title = " ".join(first_user_message.split()[:5])
        return title
    else:
        return "Untitled Conversation"

# Resource dictionary based on sentiment
resources = {
    "Your words are kind and positive": {
        "Here are some online therapy platforms": [
            "BetterHelp: An online platform offering therapy sessions with specialists.",
            "Talkspace: Connect with therapists via text or calls."
        ],
        "Or how about some mindfulness exercises provided by these apps, which offer various options like": [
            "Headspace: An app that helps with meditation and calming the mind.",
            "Calm: An app offering relaxation exercises to improve mental health."
        ],
        "You can also do self-care activities like reading books or relaxation sessions. What about": [
            "The Power of Now by Eckhart Tolle: A book that encourages living in the present moment and enhances positive feelings."
        ],
        "You can also take positive thinking courses on platforms like": [
            "Coursera or Udemy"
        ]
    },
    "Your words are calming": {
        "Here are some online therapy platforms": [
            "7 Cups: An online platform offering emotional support via counselors and community.",
            "Online Therapy: Offers video or email therapy sessions."
        ],
        "You can also practice some mindfulness exercises": [
            "Insight Timer: A free app that provides meditation sessions and relaxation activities.",
            "Breethe: A platform for meditation, guidance, and breathing techniques."
        ],
        "You can do some self-care activities that improve your mood, such as": [
            "The 'Stress Management' course on platforms like LinkedIn Learning."
        ],
        "Or you could try reading a book like": [
            "'Rich Dad Poor Dad' by Robert Kiyosaki to develop positive thinking about money and personal growth. I think it will help you a lot."
        ]
    },
    "Your words are balanced": {
        "Here are some online therapy platforms": [
            "Amwell: Provides online therapy with specialists in mental health.",
            "Doctor on Demand: Offers therapy sessions and health advice online."
        ],
        "You can also practice some mindfulness exercises with these apps, offering various options like": [
            "MyLife Meditation: An app offering guided meditation, inspiration, and breathing exercises.",
            "Smiling Mind: A program for self-development through meditation and emotional management."
        ],
        "You can also do some self-care activities that improve your mood like": [
            "'A Sound Mind in a Sound Body' book: Discusses the relationship between good thinking and physical health."
        ],
        "You can also take a 'Critical Thinking' course on platforms like": [
            "Coursera"
        ]
    },

    "Your words are somewhat uncomfortable": {
        "But don't worry, there are always ways to transform negative energy into positive. Here are some options that might help you regain your balance": [
            "BetterHelp: Online therapy with specialists to help you overcome any negative feelings.",
            "Talkspace: Connect with therapists through text or calls, as talking might be the beginning of healing."
        ],
        "Meditation and mindfulness might be the key to regaining mental clarity. Try these apps that offer guided experiences": [
            "Headspace: Meditation exercises to calm your mind and find moments of inner peace.",
            "Calm: Take moments to relax and improve your mental health through deep breathing and meditation."
        ],
        "Sometimes we need some self-support to renew positive energy within us. Here are some activities that may help": [
            "'Stress Management' course on platforms like LinkedIn Learning: Because you deserve to feel at ease.",
            "'The Power of Now' by Eckhart Tolle: Learn how to enjoy the present moment and recharge your mental life."
        ],
        "Here are also some platforms that may help you better manage relationships and negative emotions": [
            "ReGain: A platform for relationship counseling.",
            "Therapy Chat: Offers counseling with specialists in relationships and negative emotions."
        ],
        "Improving self-awareness and managing negative emotions may be an important step toward healing. Try these apps": [
            "Stop, Breathe & Think: An app that helps with self-awareness and managing negative emotions.",
            "Headspace: Focuses on helping users deal with anxiety and negative emotions."
        ],
        "Also, you can benefit from some self-help materials to improve your skills in managing your emotions": [
            "'Emotional Intelligence' by Daniel Goleman: Explains how to improve emotional intelligence, useful for managing negative emotions.",
            "'Managing Emotions' course on platforms like Udemy."
        ]
    },

    "Your words are discouraging": {
        "But don't let discouragement take over. Every tough moment is an opportunity for growth and learning. Here are some platforms that may help you get through this phase": [
            "BetterHelp: Online therapy with specialists who can help you overcome feelings of discouragement.",
            "Talkspace: Connect with therapists to help you deal with negative emotions and find inner balance."
        ],
        "Perhaps mindfulness exercises are what you need to improve your mental state and move away from discouragement. Try these apps": [
            "Insight Timer: A free app that provides meditation sessions for relaxation and inner peace.",
            "Headspace: Helps reduce anxiety and negative emotions with meditation and breathing exercises."
        ],
        "If you feel discouraged, self-help materials may be a powerful tool to change your perspective. Try these books and courses": [
            "'The Power of Now' by Eckhart Tolle: Helps you live in the present moment and free yourself from negative thoughts.",
            "'Stress Management' course on platforms like LinkedIn Learning: To learn how to manage stress and restore balance in your life."
        ],
        "If discouragement is affecting your relationships or emotional life, here are some platforms that might help": [
            "ReGain: A platform for relationship counseling to help you overcome challenges.",
            "Therapy Chat: Counseling with specialists in dealing with negative emotions and discouragement."
        ],
        "If you need more support to overcome discouragement or sadness, here are some additional resources": [
            "'Overcoming Depression' book: A guide to mental and spiritual improvement during tough times.",
            "'Dealing with Sadness' course on platforms like Coursera."
        ]
    },

    "Undefined": {
        "If your emotions are undefined or the challenges you're facing are unclear, here are some resources that might help you find direction": [
            "Talkspace or BetterHelp: Platforms offering online counseling with specialists in all undefined situations."
        ],
        "Mindfulness exercises can help you focus on the present moment and move away from distracting thoughts. Try these apps": [
            "Calm: Helps you bring attention to the present moment with relaxation and meditation exercises.",
            "Headspace: Offers meditation exercises and ways to improve focus and self-awareness."
        ],
        "If you're looking for self-help materials to assist you in prioritizing and making important decisions, here's this book": [
            "'Principles' by Ray Dalio: A book that helps guide people in facing challenges and making important decisions."
        ]
    }
}


# Custom titles dictionary based on sentiment
custom_titles = {
    "Your words are kind and positive": "I will present you with a collection of materials and activities to increase your positive energy and optimism.",
    "Your words are calming": "I will show you a collection of materials and activities to help you relax and calm down to increase your positive energy.",
    "Your words are balanced": "I will show you a collection of materials and activities that elevate your positive energy and help you think more clearly.",
    "Your words are somewhat uncomfortable": "I will present you with materials and activities to cope with stress and tension, and help you increase your positive energy and improve your mood.",
    "Your words are discouraging": "We all go through tough times, I will present you with materials and activities to cope with your current emotions and help improve your mood.",
    "Undefined": "I will present you with a collection of materials and activities to spend more optimistic time."
}

# Sidebar to customize bot settings
with st.sidebar:
    st.header("⚙️ Settings ")
    st.write("This bot is designed to offer support and advice related to mental health")

    # Choose the AI model
    model_name = st.selectbox("Choose an AI model:", ["llama2:latest", "llama3.2:latest", "llama2:13b"])

    # Enable sentiment analysis
    enable_sentiment_analysis = st.checkbox("Enable Sentiment Analysis", value=True)

    # Enable self-help suggestions
    enable_self_help_suggestions = st.checkbox("Suggest Self-Help Materials", value=True)

    # Start a new conversation
    if st.button("💬 Start a New Conversation", key="new_conversation"):
        if st.session_state.current_conversation["messages"]:
            st.session_state.current_conversation["title"] = generate_conversation_title(st.session_state.current_conversation["messages"])
            st.session_state.conversations.append(st.session_state.current_conversation)
        st.session_state.current_conversation = {"id": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "messages": [], "title": "New Conversation"}

    # Show previous conversations
    st.subheader("Previous Conversations")
    for i, conv in enumerate(st.session_state.conversations):
        with st.expander(f"{conv['title']}"):
            # Reload previous conversation
            if st.button(f"Return to Conversation", key=f"load_{i}"):
                st.session_state.current_conversation = conv
                st.rerun()
            # Delete conversation
            if st.button("Delete", key=f"delete_{i}"):
                st.session_state.conversations.pop(i)
                st.rerun()
                break

# Set up VADER for sentiment analysis
sia = SentimentIntensityAnalyzer()

# Display messages in the current conversation
if st.session_state.current_conversation["messages"]:
    st.write("Number of current messages:", len(st.session_state.current_conversation["messages"]))
    for index, message in enumerate(st.session_state.current_conversation["messages"]):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Add a download button for AI-generated responses
            if message["role"] == "assistant":
                st.download_button(
                    label="Download Response",
                    data=message["content"],
                    file_name="response.txt",
                    mime="text/plain",
                    key=f"download_{index}"
                )

# Get user input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.current_conversation["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if enable_sentiment_analysis:
        try:
            # Analyze sentiment using VADER
            sentiment_score = sia.polarity_scores(user_input)
            compound_score = sentiment_score['compound']

            # Adjust the classification based on compound_score
            if compound_score > 0.6:
                sentiment_emoji = "😍✨"
                sentiment_description = "Your words are kind and positive"
            elif compound_score > 0.3:
                sentiment_emoji = "😌🌿"
                sentiment_description = "Your words are calming"
            elif compound_score > -0.2:
                sentiment_emoji = "🤔"
                sentiment_description = "Your words are balanced"
            elif compound_score < -0.3:
                sentiment_emoji = "😕"
                sentiment_description = "Your words are somewhat uncomfortable"
            elif compound_score < -0.6:
                sentiment_emoji = "😞💔"
                sentiment_description = "Your words are discouraging"
            else:
                sentiment_emoji = "🤷‍♂️"
                sentiment_description = "Undefined"

            # Display the emoji and description at the beginning of the response
            sentiment_message = f"{sentiment_emoji} {sentiment_description}"
            with st.chat_message("assistant"):
                st.markdown(sentiment_message)

        except Exception as e:
            st.error(f"An error occurred while analyzing sentiment: {e}")

    # Generate AI responses gradually
    try:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            # Initialize the model
            llm = OllamaLLM(model=model_name)

            # Generate the response gradually
            for chunk in llm.stream(user_input):
                full_response += chunk
                placeholder.markdown(full_response)

            # Add the full response to the current conversation
            st.session_state.current_conversation["messages"].append({"role": "assistant", "content": full_response})

            # If self-help suggestions are enabled, display resources
            if enable_self_help_suggestions:
                st.write(f"## {custom_titles[sentiment_description]}")
                if sentiment_description in resources:
                    for category, items in resources[sentiment_description].items():
                        st.write(f"**{category}:**")
                        for item in items:
                            st.write(f"- {item}")
                else:
                    st.write("No resources suggested for this situation.")

    except Exception as e:
        st.error(f"An error occurred while generating the response: {e}")
