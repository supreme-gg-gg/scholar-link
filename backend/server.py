from flask import Flask, request, jsonify
import heapq

app = Flask(__name__)

class Paper:
    def __init__(self, name, citations):
        self.name = name
        self.citations = citations
        self.cited_by = []  # Papers that cite this paper

# makes paper list into matrix of distances
def process_papers(papers: list[Paper]):
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
                
    
    return {
        'matrix': matrix,
        'paper_names': [paper.name for paper in papers]
    }

# find k nearest neighbors using dijkstra
def dijkstra(matrix, start, k):
    n = len(matrix)
    distances = [float('inf')] * n
    min_heap = [(0, start)]
    result = []

    while min_heap:
        dist, node = heapq.heappop(min_heap)
        print(node)
        if len(result) == k:
            break

        if dist < distances[node]: 
            distances[node] = dist
            result.append([node, distances[node]])

            # Explore neighbors
            for i in range(n):
                if i != node and dist + matrix[node][i] < distances[i]:
                    heapq.heappush(min_heap, (dist + matrix[node][i], i))

    return result

papers = [
    Paper("Paper A", ["Paper B", "Paper C", "Paper D"]),
    Paper("Paper B", ["Paper C", "Paper E"]),
    Paper("Paper C", ["Paper E"]),
    Paper("Paper D", ["Paper B", "Paper C"]),
    Paper("Paper E", [])
]

result = dijkstra(process_papers(papers)["matrix"], 0, 3)

print(result)

if __name__ == '__main__':
    app.run(debug=True)