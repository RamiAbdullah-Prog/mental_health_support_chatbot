# Mental Health Support Chatbot

This project is a mental health support chatbot built using **Streamlit** and **Langchain**, enhanced with sentiment analysis to provide emotional support and self-help resources based on user input. It analyzes user messages, categorizes them by sentiment, and offers personalized suggestions for mental well-being.

## Features

- **Sentiment Analysis**: The chatbot uses the VADER sentiment analyzer to assess the sentiment of user inputs and responds accordingly.
- **Personalized Responses**: Based on sentiment, the bot provides tailored advice, resources, and self-help materials.
- **Conversation History**: All conversations are stored in the session, and users can start new conversations or load previous ones.
- **Customizable Settings**: You can choose the AI model and enable or disable features like sentiment analysis and self-help suggestions.
- **Resource Suggestions**: Depending on the sentiment analysis, the chatbot offers relevant therapy platforms, mindfulness apps, books, and courses.
- **Gradual Response Generation**: The AI generates responses gradually, providing a more natural conversation flow.

## Installation

To run the chatbot, you'll need to have Python installed along with the following dependencies:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/mental-health-chatbot.git
    cd mental-health-chatbot
    ```

2. **Install required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Streamlit App**:
    ```bash
    streamlit run app.py
    ```

2. **Customize Settings**:  
   In the sidebar, you can select:
   - The AI model to use (e.g., `llama2:latest`, `llama3.2:latest`, etc.).
   - Enable or disable **Sentiment Analysis** and **Self-Help Suggestions**.

3. **Start a New Conversation**:  
   The chatbot will automatically create a new conversation when you click the **Start a New Conversation** button.

4. **View Previous Conversations**:  
   Conversations are saved in the session, and you can revisit or delete them as needed.

## How It Works

1. **Sentiment Analysis**:  
   The chatbot uses **VADER** from the **NLTK** library to analyze the sentiment of each user message. Based on the sentiment score:
   - Positive emotions will trigger kind and calming resources.
   - Negative emotions will suggest resources aimed at coping with stress or discouragement.

2. **Custom Titles and Resources**:  
   The bot provides titles and relevant resources (books, apps, courses) based on the identified sentiment of the user’s input.

3. **AI Responses**:  
   The bot generates AI responses using **Langchain Ollama** integration, offering suggestions and advice based on the user’s sentiment and queries.

4. **Downloadable Responses**:  
   Users can download AI-generated responses as text files for later reference.

## Features in Detail

### Sentiment Analysis

- **Positive Sentiment**:  
   Provides resources related to mindfulness, positive thinking, and self-care.
  
- **Calming Sentiment**:  
   Recommends resources like relaxation techniques and stress management.

- **Balanced Sentiment**:  
   Suggests resources for maintaining a healthy balance in life, such as courses on critical thinking or mental health apps.

- **Uncomfortable Sentiment**:  
   Recommends resources for managing anxiety, negative emotions, and stress.

- **Discouraging Sentiment**:  
   Offers resources to help overcome discouragement, such as therapy platforms and motivational books.

- **Undefined Sentiment**:  
   Provides general resources for individuals who may be uncertain or confused about their emotions.

### Self-Help Suggestions

For each sentiment, the chatbot provides links to:
- **Online Therapy Platforms**: BetterHelp, Talkspace, 7 Cups, etc.
- **Mindfulness Apps**: Calm, Insight Timer, Headspace, etc.
- **Self-Care Activities**: Books like *The Power of Now*, courses on platforms like Coursera, etc.

### Previous Conversations

You can start a new conversation or load a previous conversation. Every conversation is stored in the session state, allowing you to revisit past chats.

### Chat UI

- **User Input**: A simple text box allows users to send messages to the chatbot.
- **Bot Responses**: Responses are displayed in a chat-like interface with a gradual display.
- **Downloadable Responses**: Option to download AI-generated responses.

## Requirements

- Python 3.7+
- Streamlit
- Langchain
- nltk
- ollama

## Project Structure

```
mental-health-chatbot/
│
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
