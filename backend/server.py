from flask import Flask, request, jsonify

app = Flask(__name__)

class Paper:
    def __init__(self, name, citations):
        self.name = name
        self.citations = citations
        self.cited_by = []  # Papers that cite this paper

def process_papers(papers: list[Paper]):
    matrix = [[0 for _ in range(len(papers))] for _ in range(len(papers))]
    paper_dict = {}
    
    for i in range(len(papers)):
        paper_dict[papers[i].name] = i

    for i in range(len(papers)):
        for j in range(len(papers[i].citations)):
            if papers[i].citations[j] in paper_dict:
                papers[paper_dict[papers[i].citations[j]]].cited_by.append(papers[i].name)
    print(papers)

    for i in range(len(papers)):
        paper_dict[papers[i].name] = [papers[i], i]
    
    # Process all papers
    for i in range(len(papers)):
        for j in range(len(papers[i].citations)):
            if papers[i].citations[j] in paper_dict:
                print(papers[i].name + " cites " + papers[i].citations[j])
                matrix[paper_dict[papers[i].citations[j]][1]][i] += 1
                matrix[i][paper_dict[papers[i].citations[j]][1]] += 1
                for k in range(j+1, len(papers[i].citations)):
                    if papers[i].citations[k] in paper_dict:
                        print(papers[i].citations[j] + " cited along with " + papers[i].citations[k] + " by paper " + papers[i].name)
                        matrix[paper_dict[papers[i].citations[k]][1]][paper_dict[papers[i].citations[j]][1]] += 1
                        matrix[paper_dict[papers[i].citations[j]][1]][paper_dict[papers[i].citations[k]][1]] += 1
        
        for j in range(len(papers[i].cited_by)):
            if papers[i].cited_by[j] in paper_dict:
                for k in range(j + 1, len(papers[i].cited_by)):
                    if papers[i].cited_by[k] in paper_dict:
                        print(papers[i].cited_by[j] + " and " + papers[i].cited_by[k] + " both cite " + papers[i].name)
                        matrix[paper_dict[papers[i].cited_by[k]][1]][paper_dict[papers[i].cited_by[j]][1]] += 1
                        matrix[paper_dict[papers[i].cited_by[j]][1]][paper_dict[papers[i].cited_by[k]][1]] += 1
                
    
    return {
        'matrix': matrix,
        'paper_names': [paper.name for paper in papers]
    }

papers = [
    Paper("Paper A", ["Paper B", "Paper C", "Paper D"]),
    Paper("Paper B", ["Paper C", "Paper E"]),
    Paper("Paper C", ["Paper E"]),
    Paper("Paper D", ["Paper B", "Paper C"]),
    Paper("Paper E", [])
]

result = process_papers(papers)

print(result)

if __name__ == '__main__':
    app.run(debug=True)