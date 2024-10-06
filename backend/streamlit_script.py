import sys
from transformers import pipeline
from keybert import KeyBERT
import json
from collections import Counter
import re


def nlp_process_text(text):
    nlp_model = pipeline("summarization", model="facebook/bart-large-xsum")
    summary = nlp_model(text, max_length=50, min_length=10, do_sample=False)

    kw_model = KeyBERT(model='all-mpnet-base-v2')
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=4)

    return (summary[0]['summary_text'], [kw[0] for kw in keywords])


def count_keyword_frequencies(text, keywords):
    # Convert text to lowercase and split into words
    words = re.findall(r'\w+', text.lower())
    
    # Count occurrences of each keyword
    keyword_frequencies = Counter()
    for word in words:
        if word in keywords:
            keyword_frequencies[word] += 1
    
    return keyword_frequencies

if __name__ == "__main__":
    # Get the text input from Flask
    user_text = sys.argv[1]

    # Process the text
    summary, keywords = nlp_process_text(user_text)

    keyword_frequencies = count_keyword_frequencies(user_text, keywords)
    result = {
        "summary": summary,
        "keywords": keywords,
        "keyword_frequencies": dict(keyword_frequencies)  # Convert Counter to dict
    }

    # Output the result (captured by Flask)
    print(json.dumps(result))