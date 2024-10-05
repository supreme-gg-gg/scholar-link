from server import create_papers

if __name__ == "__main__":
    paper_list = create_papers("machine learning")
    print(paper_list[0].citations)