# Automated Inquiry Handling System

## Overview
The Automated Inquiry Handling System is a Streamlit-based web application designed to process different types of user inquiries related to film equipment. It leverages Gemini AI for context extraction and sentiment analysis to provide accurate and insightful responses. The application can handle inquiries, reviews, and assistance requests.

## Features
- **Inquiry Handling**: Checks the availability of film equipment based on the user's inquiry.
- **Review Analysis**: Analyzes the sentiment of user reviews and provides appropriate responses.
- **Assistance Request**: Uses AI to provide answers to complex queries based on a knowledge base.

## Technologies Used
- **Streamlit**: For building the web application.
- **Gemini AI**: For AI-based context extraction and question-answering.
- **LangChain**: For handling prompts and chains.
- **SQLite**: For storing and retrieving film equipment data.
- **VADER Sentiment Analysis**: For analyzing the sentiment of user reviews.
- **FAISS**: For efficient similarity search.

## Usage
1. **Select Service Type**: Choose the type of service you want to handle (Inquiry, Review, Assistance Request).
2. **Enter Content**: Provide the relevant details in the text area.
3. **Process**: Click the "Process" button to get a response based on the selected service type.

## File Structure
```plaintext
.
├── __pycache__/              # Cache files
├── faiss_index/              # FAISS index files
├── .env                      # Environment variables
├── equipment_FAQS.txt        # FAQ text file
├── film_equipment.db         # SQLite database with film equipment data
├── main.py                   # Main application file
├── requirements.txt          # Python dependencies
└── sql.py                    # SQL queries and database interactions
```

## Functions

### check_availability
Checks the availability of equipment in the specified category from the SQLite database.

### analyze_sentiment
Analyzes the sentiment of the given text using VADER Sentiment Analysis.

### extract_category_from_email
Extracts the category of equipment from the email content.

### get_chunks
Splits the text into manageable chunks for vectorization.

### get_vector
Generates vector embeddings for the text chunks and saves them locally.

### conversation_chain
Creates a conversation chain using LangChain for handling QA.

### get_answer
Retrieves an answer to the given question using vector similarity search and the conversation chain.

### issue_handling
Handles different types of user issues (Inquiry, Review, Assistance Request) and returns appropriate responses.

## screenshots
-`Assistance`
![Screenshot 2024-07-28 181552](https://github.com/user-attachments/assets/e1d1ff58-b8c5-4f4a-8319-524ea19ee02d)
-`Review`
![Screenshot 2024-07-28 181502](https://github.com/user-attachments/assets/7ae3da2e-d509-444d-84c0-3783a1fb1113)
-`Inquiry`
![Screenshot 2024-07-28 181416](https://github.com/user-attachments/assets/f9e7a1fe-63ea-460b-abc6-9c32bea3321a)
