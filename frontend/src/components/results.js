import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Results = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const searchResults = location.state?.searchResults || [];

    const handleBuildGraph = async (index) => {
        try {
            const response = await fetch('http://127.0.0.1:5000/graph', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ index }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            navigate('/graph', { 
                state: { 
                    graphData: data,
                    originPaperIndex: index
                } 
            });
        } catch (error) {
            console.error('Error building graph:', error);
            // Handle error (e.g., show error message to user)
        }
    };

    return (
        <div className="container mx-auto p-4 bg-white text-black font-Fustat">
            <h1 className="text-2xl font-semibold mb-4 bg-white">Paper Suggestions</h1>
            {searchResults.map((paper, index) => (
                <div key={index} className="card bg-white shadow-xl mb-4">
                    <div className="card-body">
                        <h2 className="card-title">{paper.title}</h2>
                        <p className="text-sm">{paper.authors.join(', ')}</p>
                        <p className="text-sm">{new Date(paper.date).getFullYear()}. Cited by: {paper.cited_by}</p>
                        <p className="text-sm mt-2">{paper.summary}</p>
                        <div className="card-actions justify-end mt-2">
                            <button
                                className="btn btn-primary btn-sm"
                                onClick={() => handleBuildGraph(index)}
                            >
                                Build Graph
                            </button>
                            <button className="btn btn-outline btn-sm">Save</button>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Results;