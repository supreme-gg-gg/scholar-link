from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from scrape_paper import process_papers, create_papers

app = Flask(__name__)

# Allow requests from your React frontend
CORS(app)

papers = []

stored_url = ""

@app.route('/send-url', methods=['POST'])
def receive_data():
    global stored_url
    data = request.get_json()
    pdf_url = data.get('url')
    
    if pdf_url:
        # Store the PDF URL for Streamlit to access
        stored_url = pdf_url
        return jsonify({"response": "Data received successfully!"}), 200
    else:
        return jsonify({"error": "No URL provided."}), 400

@app.route('/get-url', methods=['GET'])
def get_data():
    global stored_url
    # Return the stored PDF URL
    return jsonify({"url":stored_url}), 200

@app.route('/search', methods=['POST'])
def search_papers():
    global papers
    req = request.get_json()
    keyword = req.get("keyword")
    print(f"Received keyword: {keyword}")
    papers = create_papers(keyword, 10)
    papers_json = [paper.to_dict() for paper in papers]
    return jsonify(papers_json)

@app.route('/graph', methods=['POST'])
def make_graph():
    req = request.get_json()
    index= req.get("index")
    data = process_papers(papers, index, 10)
    papers_json = [paper.to_dict() for paper in papers if paper.name in data["paper_names"]]

    response = {
        "total_papers": len(papers_json),
        "source": "arXiv",
        "papers": papers_json, # only returns the papers that we have selected from the algorithm
        "matrix": data["matrix"]
    }

    return jsonify(response)

# streamlit data
@app.route('/graphdata', methods=['GET'])
def graph_data():
    paper_info = [[paper.published, sum(len(author) for author in paper.authors)] for paper in papers]
    return jsonify(paper_info)

@app.route('/prompt', methods=["POST"])
def prompt():
    global papers
    import subprocess

    data = request.get_json()
    user_input = data["prompt"]

    # Trigger the Streamlit script using subprocess
    result = subprocess.run(
        ["python3", "backend/streamlit_script.py", user_input], capture_output=True, text=True
    )

    # Get the output from the Streamlit script
    processed_output = result.stdout

    # Parse the JSON output from the script
    try:
        processed_data = json.loads(processed_output)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse output."}), 500

    keyword = processed_data["keywords"]
    result = ", ".join(f"'{item}'" for item in keyword)
    print(f"Received keyword: {result}")
    papers = create_papers(result, 10)
    papers_json = [paper.to_dict() for paper in papers]
    return jsonify(papers_json)

@app.route('/paper_keywords', methods=['POST'])
def paper_keywords():
    import subprocess
    data = request.json
    paper_index = data['index']
    paper = papers[paper_index]
   
    # Process the paper's text to get keywords and frequencies
    result = subprocess.run(
        ["python3", "streamlit_script.py", paper.summary],
        capture_output=True, text=True
    )
    processed_data = json.loads(result.stdout)
   
    return jsonify(processed_data)

@app.route('/set_paper_index', methods=['POST'])
def set_paper_index():
    global current_paper_index
    data = request.get_json()
    index = data.get('index')
    if index is not None:
        current_paper_index = index
        return jsonify({"message": "Paper index set sucessfully"}), 200
    else:
        return jsonify({"error": "No index provided"}), 400

@app.route('/get_paper_index', methods=['GET'])
def get_paper_index():
    global current_paper_index
    return jsonify({"index": current_paper_index}), 200

if __name__ == '__main__':
    app.run(debug=True)