from server import create_papers

if __name__ == "__main__":
    paper_list = create_papers("machine learning", limit=2)
    print(paper_list[1].citations)