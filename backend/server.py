from flask import Flask, request, jsonify
import heapq

app = Flask(__name__)

class Paper:
    def __init__(self, name, citations):
        self.name = name
        self.citations = citations
        self.cited_by = []  # Papers that cite this paper

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
        'paper_names': [papers[result[i][0]] for i in range(i+1, len(result))]
    }



@app.route('/graph', methods=['POST'])
def make_graph():
    papers = [
        Paper("Paper A", ["Paper B", "Paper C", "Paper D"]),
        Paper("Paper B", ["Paper C", "Paper E"]),
        Paper("Paper C", ["Paper E"]),
        Paper("Paper D", ["Paper B", "Paper C"]),
        Paper("Paper E", [])
    ]
    return jsonify(process_papers(papers, 0, 3))

if __name__ == '__main__':
    app.run(debug=True)