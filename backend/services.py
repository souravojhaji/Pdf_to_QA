from langchain_community.document_loaders import PyMuPDFLoader
from transformers import pipeline

def extract_text_from_pdf(pdf_path):
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()
    
    # Join the text content of each document page into a single string
    text_content = "\n".join([doc.page_content for doc in documents])
    return text_content 

def answer_question(document_content, question):
    # Load a question-answering pipeline
    qa_pipeline = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")


    def answer_question_from_huggingface(context, question):
        return qa_pipeline(question=question, context=context)

    answer = answer_question_from_huggingface(document_content, question)
    print(answer['answer'])
    # answer = 'ss'
    return answer['answer']
