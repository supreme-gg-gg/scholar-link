from flask import Flask, request, jsonify

app = Flask(__name__)

class Paper:
    def __init__(self, name, citations):
        self.name = name
        self.citations = citations
        self.cited_by = []  # Papers that cite this paper

def process_papers(papers: list[Paper]):
    # Create paper dictionary for easy lookup
    paper_dict = {paper.name: paper for paper in papers}
    
    # Build cited_by lists
    for paper in papers:
        for cited_paper_name in paper.citations:
            if cited_paper_name in paper_dict:
                paper_dict[cited_paper_name].cited_by.append(paper.name)
    
    # Create matrix for edge weights
    n = len(papers)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # Process all papers
    for i in range(n):
        paper = papers[i]
        
        # Process citations (bibliographic coupling)
        for j in range(n):
            paper1 = papers[j]
            for k in range(j + 1, n):
                paper2 = papers[k]
                
                # Check if papers[j] and papers[k] are both cited by papers[i]
                if paper1.name in paper.citations and paper2.name in paper.citations:
                    matrix[j][k] += 1
                    matrix[k][j] += 1
        
        # Process cited_by (co-citation)
        for j in range(n):
            paper1 = papers[j]
            for k in range(j + 1, n):
                paper2 = papers[k]
                
                # Check if papers[j] and papers[k] both cite papers[i]
                if paper.name in paper1.citations and paper.name in paper2.citations:
                    matrix[j][k] += 1
                    matrix[k][j] += 1
        
        # Direct citations
        for j in range(n):
            if papers[j].name in paper.citations:
                matrix[i][j] += 1
                matrix[j][i] += 1
    
    return {
        'matrix': matrix,
        'paper_names': [paper.name for paper in papers]
    }

@app.route('/generate_citation_graph', methods=['POST'])
def generate_citation_graph():
    try:
        papers_data = request.json
        if not papers_data:
            return jsonify({'error': 'Invalid input data'}), 400
        
        papers = [Paper(p['name'], p['citations']) for p in papers_data]
        result = process_papers(papers)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)