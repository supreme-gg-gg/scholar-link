import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
    const navigate = useNavigate();
    const [keyword, setKeyword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:5000/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ keyword }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setIsLoading(false);
           
            // Navigate directly to GraphPage with the search data, including links if available
            navigate('/graph', { 
                state: { 
                    searchResults: {
                        papers: data.papers,
                        matrix: data.matrix,
                        links: data.links || []
                    } 
                } 
            });
        } catch (error) {
            console.error('Error fetching search results:', error);
            setIsLoading(false);
            // Handle error (e.g., show error message to user)
        }
    };

    return (
        <main className="flex-grow flex flex-col items-center justify-center p-4 bg-cover bg-center bg-no-repeat bg-white font-Fustat" style={{ backgroundImage: 'url("/bg_scholarlink.png")' }}>
            <div className="bg-white bg-opacity-80 p-8 rounded-lg shadow-xl max-w-5xl w-full">
                <header className="text-center mb-">
                    <h1 className="text-5xl font-semibold mb-2 text-black font-Fustat font-bold">Explore connected papers in a visual graph</h1>
                    <p className="text-xl text-black">To start, enter a paper identifier</p>
                    <br></br>
                </header>
                <div className="form-control w-full">
                    <form onSubmit={handleSearch} className="flex shadow-lg">
                        <input
                            type="text"
                            value={keyword}
                            onChange={(e) => setKeyword(e.target.value)}
                            placeholder="Search by keywords, paper title, DOI or another identifier"
                            className="input input-bordered w-full rounded-r-none bg-white"
                        />
                        <button type="submit" className="btn btn-primary rounded-l-none" disabled={isLoading}>
                            {isLoading ? 'Searching...' : 'Build a graph'}
                        </button>
                    </form>
                </div>
            </div>
        </main>
    );
};

export default HomePage;