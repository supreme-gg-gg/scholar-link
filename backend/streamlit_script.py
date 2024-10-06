import sys
from transformers import pipeline
from keybert import KeyBERT
import json
from collections import Counter


def nlp_process_text(text):
    nlp_model = pipeline("summarization", model="facebook/bart-large-xsum")
    summary = nlp_model(text, max_length=50, min_length=10, do_sample=False)
   
    kw_model = KeyBERT(model='all-mpnet-base-v2')
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=4)


    # Count frequencies of keywords
    keyword_list = [kw[0] for kw in keywords]
    keyword_frequencies = Counter(keyword_list)


    return (summary[0]['summary_text'], keyword_list, keyword_frequencies)


if __name__ == "__main__":
    # Get the text input from Flask
    user_text = sys.argv[1]
   
    # Process the text
    summary, keywords, keyword_frequencies = nlp_process_text(user_text)
    result = {
        "summary": summary,
        "keywords": keywords,
        "keyword_frequencies": dict(keyword_frequencies)  # Convert Counter to dict
    }
   
    # Output the result (captured by Flask)
    print(json.dumps(result))