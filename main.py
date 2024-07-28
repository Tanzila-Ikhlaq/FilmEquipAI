import os
import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
import warnings

warnings.filterwarnings("ignore")

os.environ['GRPC_VERBOSITY'] = 'ERROR'

st.set_page_config(
    page_title="Issue Resolver",
    page_icon=":smile:",
    layout="centered",
)

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def check_availability(category_name):
    try:
        conn = sqlite3.connect("film_equipment.db")
        cursor = conn.cursor()
        cursor.execute('SELECT name, price, availability FROM equipment WHERE type LIKE ?', (f'%{category_name}%',))
        result = cursor.fetchall()
        conn.close()

        available_items = [item for item in result if item[2]]
        unavailable_items = [item for item in result if not item[2]]

        total_items = len(available_items) + len(unavailable_items)
        available_count = len(available_items)
        unavailable_count = len(unavailable_items)

        response = f"Total {category_name} items: {total_items}\n"
        response += f"Available items: {available_count}\n"
        if available_items:
            response += "\nThe available items are :\n"
            for item in available_items:
                response += f"Product: {item[0]}, Price: {item[1]}\n"
        else:
            response += f"\nNo {category_name} items are available.\n"

        if unavailable_items:
            response += "\nThe items are out of stock:\n"
            for item in unavailable_items:
                response += f"Product: {item[0]}, Price: {item[1]}\n"

        return response
    except sqlite3.Error as e:
        return f"An error occurred while checking availability: {e}"

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)['compound']
    if sentiment_score >= 0.05:
        sentiment = "Positive"
    else:
        sentiment = "Negative"
    return sentiment

def extract_category_from_email(content):
    content_lower = content.lower()
    if "camera" in content_lower:
        return "Camera"
    elif "tripod" in content_lower:
        return "Accessory"
    elif "microphone" in content_lower:
        return "Audio"
    elif "lighting" in content_lower:
        return "Lighting"
    elif "drone" in content_lower:
        return "Drone"
    else:
        return None

def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=0
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectors = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    vectors.save_local("faiss_index")
    return vectors

def conversation_chain():
    prompt_template = '''
    You are a knowledgeable chatbot designed to provide insightful answers based on the context extracted from a knowledge base.

    Context: {context}

    Question: {question}

    Instructions:
    - Use the provided context to answer the question accurately.
    - If the question cannot be answered based on the context, politely inform the user.
    - Provide clear and concise answers.
    - Ensure your responses are directly related to the query asked.
    '''
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def get_answer(question, vectors):
    doc = vectors.similarity_search(question)
    chain = conversation_chain()
    response = chain({
        "input_documents": doc,
        "question": question,
        "return_only_outputs": True
    })
    return response["output_text"]

def issue_handling(service, content):
    print(f"Handling service: {service}")  # Debug statement
    if service.lower() == "inquiry":
        item_category = extract_category_from_email(content)
        print(f"Extracted category: {item_category}")  # Debug statement
        if item_category:
            return check_availability(item_category)
        else:
            return "Could not determine the category from your inquiry. Please specify the type of equipment you are interested in."
    elif service.lower() == "review":
        sentiment = analyze_sentiment(content)
        print(f"Sentiment: {sentiment}")  # Debug statement
        if sentiment == "Positive":
            return "Thank you for your positive response, we appreciate you. Kindly share your experience on our website as well.😊"
        else:
            return "We are sorry to hear that. Our executive will call you shortly to understand your issue better, and we are providing a coupon with 15% off for your next purchase."
    elif service.lower() == "assistance request":
        chunks = get_chunks(content)
        vectors = get_vector(chunks)
        response = get_answer(content, vectors)
        return response
    else:
        return "Sorry at the moment we are unable to solve your issue."

st.header(":rainbow[Automated Inquiry Handling System]👩‍💻")

service = st.selectbox("Select Service Type", ["Inquiry", "Review", "Assistance Request"])
content = st.text_area("Enter the content")

if st.button("Process"):
    response = issue_handling(service, content)
    st.write(response)