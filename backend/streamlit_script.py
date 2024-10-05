import sys
from transformers import pipeline
from keybert import KeyBERT
import json

def nlp_process_text(text):
    nlp_model = pipeline("summarization", model="facebook/bart-large-xsum")
    summary = nlp_model(text, max_length=50, min_length=10, do_sample=False)
    
    kw_model = KeyBERT(model='all-mpnet-base-v2')
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=4)

    return (summary[0]['summary_text'], [kw[0] for kw in keywords])

if __name__ == "__main__":
    # Get the text input from Flask
    user_text = sys.argv[1]
    
    # Process the text
    summary, keywords = nlp_process_text(user_text)
    result = {
        "summary": summary,
        "keywords": keywords
    }
    
    # Output the result (captured by Flask)
    print(json.dumps(result))