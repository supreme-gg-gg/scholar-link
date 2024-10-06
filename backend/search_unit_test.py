import unittest
from scrape_paper import create_papers

class TestCreatePapers(unittest.TestCase):
    def test_create_papers(self):
        paper_list = create_papers("machine learning", limit=2)
        self.assertEqual(len(paper_list), 2)
        self.assertIsNotNone(paper_list[1].citations)

if __name__ == "__main__":
    unittest.main()