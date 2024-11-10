import fitz  # PyMuPDF for PDF processing
import re
from transformers import pipeline

# Load the summarization model pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# Function to extract text from each page of the PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Clean up the extracted text
def preprocess_text(text):
    # Remove excess whitespace and non-printable characters
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\x0c', ' ', text)  # Remove page break characters
    return text.strip()

# Identify and extract relevant sections based on keywords
def extract_key_sections(text):
    sections = {
        "growth_prospects": [],
        "business_changes": [],
        "key_triggers": [],
        "material_effects": []
    }
    
    # Split text into lines for easier keyword matching
    lines = text.split('.')
    
    for line in lines:
        line_lower = line.lower()
        
        if "growth" in line_lower or "prospect" in line_lower:
            sections["growth_prospects"].append(line)
        elif "change" in line_lower or "restructure" in line_lower or "business model" in line_lower:
            sections["business_changes"].append(line)
        elif "trigger" in line_lower or "driver" in line_lower:
            sections["key_triggers"].append(line)
        elif "impact" in line_lower or "effect" in line_lower or "earnings" in line_lower:
            sections["material_effects"].append(line)
    
    return sections

# Summarize each extracted section
def summarize_sections(sections):
    summarized_data = {}
    for section, sentences in sections.items():
        if sentences:
            # Concatenate sentences and summarize
            joined_text = " ".join(sentences)
            try:
                summary = summarizer(joined_text, max_length=100, min_length=30, do_sample=False)
                summarized_data[section] = summary[0]['summary_text']
            except Exception as e:
                print(f"Error summarizing section '{section}': {e}")
                summarized_data[section] = "Summary not available."
    return summarized_data

# Main function to orchestrate the PDF analysis and summarization
def analyze_pdf(pdf_path):
    # Step 1: Extract and preprocess the text
    raw_text = extract_text_from_pdf(pdf_path)
    clean_text = preprocess_text(raw_text)
    
    # Step 2: Extract key sections based on keywords
    sections = extract_key_sections(clean_text)
    
    # Step 3: Summarize each identified section
    summaries = summarize_sections(sections)
    
    return summaries

# Run the function on a sample PDF
if __name__ == "__main__":
    pdf_path = "example.pdf"  # Update with actual file path
    extracted_data = analyze_pdf(pdf_path)
    
    # Display the results in a JSON-like format
    import json
    print(json.dumps(extracted_data, indent=4))
