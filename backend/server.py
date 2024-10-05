from flask import Flask, request, jsonify
import heapq
import math

from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import feedparser
import fitz  # PyMuPDF
import re
import json
import time

app = Flask(__name__)

class Paper:
    def __init__(self, name, citations):
        self.name = name
        self.citations = citations
        self.cited_by = []  # Papers that cite this paper

def search_arxiv(query, start, max_results):
    base_url = "http://export.arxiv.org/api/query?"
    search_query = f"search_query=all:{query}&start={start}&max_results={max_results}"
    for attempt in range(5):  # Try up to 5 times
        try:
            response = requests.get(base_url + search_query)
            response.raise_for_status()  # Raise an error for bad responses
            break
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}: {e}")
            if attempt < 4:  # Don't sleep on the last attempt
                time.sleep(2 ** attempt)  # Exponential backoff
    else:
        print("Failed to fetch results after 5 attempts")
        return []

    # Parse the response
    feed = feedparser.parse(response.content)
    papers = []

    for entry in feed.entries:
        paper = {
            'title': entry.title,
            'summary': entry.summary,
            'pdf': entry.links[1].href,  # returns PDF link for further parsing
            'published': entry.published,
            'authors': [author.name for author in entry.authors]
        }
        papers.append(paper)

    return papers

def extract_text_from_web_pdf(pdf_url):
    try: 
        # Step 1: Get PDF content from URL
        response = requests.get(pdf_url)
        response.raise_for_status()  # Check if the request was successful
        
        # Step 2: Check if the response content type is a PDF
        if response.headers['Content-Type'] != 'application/pdf':
            raise ValueError("URL does not point to a valid PDF file")

        pdf_bytes = response.content

        # Step 3: Open the PDF from bytes in-memory using PyMuPDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Step 4: Extract the text from the PDF
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()  # Extract text from each page

        return text
    except Exception as e:
        print(f"Error processing PDF from {pdf_url}: {str(e)}")
        return None

def extract_citations_from_text(text):

    def clean_text(text):
        cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)
        return cleaned_text.lower()

    # Find the citations section by searching for "References" or "Bibliography"
    reversed_text = text[::-1]
    citations_start = re.search(r'^\s*(secnerefer|yhpargoilbib)\s*$', reversed_text.lower(), re.MULTILINE)
    try:
        original_start_pos = len(text) - citations_start.end()
    except AttributeError:
        return []

    if original_start_pos:
        # Extract the citations section from the text
        citations_section = text[original_start_pos:]

        # Split by common delimiters used in citations
        # citations = re.split(r'\[\d+\]|\n\d+\. ', citations_section)  # For numbered reference   
        citations = re.split(r'\[\d+\]\s*', citations_section)
        parsed_citations = []
        for citation in citations:
            citation = citation.strip()  # Clean up whitespace
            if citation:  # Only process non-empty citations
                
                # Step 1: Initialize variables
                authors = ""
                title = ""
                
                # Step 2: Iterate through the citation and find the last valid period
                last_valid_period_index = -1

                for index, char in enumerate(citation):
                    if char == '.':
                        # Check the character before the period
                        if index > 0 and citation[index - 1].isupper():
                            # If the previous character is uppercase, skip this period (possible initial)
                            continue
                        else:
                            # If we're not skipping, we found the last valid period
                            last_valid_period_index = index
                            break

                # If a valid period was found, extract authors and title
                if last_valid_period_index != -1:
                    authors = citation[:last_valid_period_index].strip()
                    title = citation[last_valid_period_index + 1:].strip()

                    # Handle additional periods in the title (cut off at the first valid period in title)
                    title_end_index = title.find('.')
                    if title_end_index != -1:
                        # Keep the title until the first period that is not part of additional information
                        title = title[:title_end_index].strip()

                # If title is just numbers or non-meaningful text, handle that case
                if title.isdigit() or title == '' or authors == '':
                    continue

                parsed_citations.append({"title": clean_text(title), "author": clean_text(authors)})

        return parsed_citations

    return []

def fetch_batch(query, start, batch_size):
    return search_arxiv(query, start, batch_size)

def create_papers(query, limit=100, batch_size=20):
    print("FETCHING START")
    
    def process_paper(paper):
        if "pdf" not in paper["pdf"]:
            return None
        text = extract_text_from_web_pdf(paper["pdf"])
        if text is None:
            return None
        citations_json = extract_citations_from_text(text)
        return Paper(paper["title"], [entry["title"] for entry in citations_json])

    # Calculate the number of batches
    num_batches = math.ceil(limit / batch_size)
    
    all_papers = []
    processed_papers = []

    with ThreadPoolExecutor() as executor:
        # Fetch papers in batches concurrently
        batch_futures = [executor.submit(fetch_batch, query, i * batch_size, batch_size) 
                         for i in range(num_batches)]

        for future in as_completed(batch_futures):
            batch_papers = future.result()
            all_papers.extend(batch_papers)
            if len(all_papers) >= limit:
                break

        # Limit the number of papers to the requested limit
        all_papers = all_papers[:limit]

        # Process papers concurrently
        process_futures = [executor.submit(process_paper, paper) for paper in all_papers]

        for future in as_completed(process_futures):
            result = future.result()
            if result is not None:
                processed_papers.append(result)

    print("FETCHING DONE")
    return processed_papers


# makes paper list into matrix of distances
def process_papers(papers: list[Paper], start, neighbors):
    # make graph
    matrix = [[10000 for _ in range(len(papers))] for _ in range(len(papers))]
    paper_dict = {}
    
    for i in range(len(papers)):
        paper_dict[papers[i].name] = i

    for i in range(len(papers)):
        for j in range(len(papers[i].citations)):
            if papers[i].citations[j] in paper_dict:
                papers[paper_dict[papers[i].citations[j]]].cited_by.append(papers[i].name)

    for i in range(len(papers)):
        paper_dict[papers[i].name] = [papers[i], i]
    
    for i in range(len(papers)):
        for j in range(len(papers[i].citations)):
            if papers[i].citations[j] in paper_dict:
                matrix[paper_dict[papers[i].citations[j]][1]][i] /= 2
                matrix[i][paper_dict[papers[i].citations[j]][1]] /= 2
                for k in range(j+1, len(papers[i].citations)):
                    if papers[i].citations[k] in paper_dict:
                        matrix[paper_dict[papers[i].citations[k]][1]][paper_dict[papers[i].citations[j]][1]] /= 2
                        matrix[paper_dict[papers[i].citations[j]][1]][paper_dict[papers[i].citations[k]][1]] /= 2
        
        for j in range(len(papers[i].cited_by)):
            if papers[i].cited_by[j] in paper_dict:
                for k in range(j + 1, len(papers[i].cited_by)):
                    if papers[i].cited_by[k] in paper_dict:
                        matrix[paper_dict[papers[i].cited_by[k]][1]][paper_dict[papers[i].cited_by[j]][1]] /= 2
                        matrix[paper_dict[papers[i].cited_by[j]][1]][paper_dict[papers[i].cited_by[k]][1]] /= 2

    # dijkstra on graph
    distances = [float('inf')] * len(papers)
    min_heap = [(0, start)]
    result = []

    while min_heap:
        dist, node = heapq.heappop(min_heap)
        if len(result) == neighbors:
            break

        if dist < distances[node]: 
            distances[node] = dist
            result.append([node, distances[node]])

            for i in range(len(papers)):
                if i != node and dist + matrix[node][i] < distances[i]:
                    heapq.heappush(min_heap, (dist + matrix[node][i], i))

    # build final matrix
    matrix2 = [[-1 for _ in range(len(result))] for _ in range(len(result))]
    for i in range(len(result)):
        for j in range(i+1, len(result)):
            matrix2[i][j] = matrix[result[i][0]][result[j][0]]
            matrix2[j][i] = matrix[result[i][0]][result[j][0]]

    for i in range(len(result)):
        matrix[result[i][0]][start] = result[i][1]
        matrix[start][result[i][0]] = result[i][1]

    return {
        'matrix': matrix2,
        'paper_names': [papers[result[i][0]].name for i in range(len(result))]
    }


@app.route('/graph', methods=['GET'])
def make_graph():
    papers = create_papers("machine learning", 100)
    return jsonify(process_papers(papers, 0, 100))

if __name__ == '__main__':
    app.run(debug=True)