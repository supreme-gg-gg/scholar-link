import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
    const navigate = useNavigate();
    const [searchInput, setSearchInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [searchMode, setSearchMode] = useState('keyword'); 

    const handleSearch = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const endpoint = searchMode === 'keyword' ? '/search' : '/prompt';
            const response = await fetch(`http://127.0.0.1:5000${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    [searchMode === 'keyword' ? 'keyword' : 'prompt']: searchInput 
                }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setIsLoading(false);
           
            // Navigate to Results page with the search data
            navigate('/results', { state: { searchResults: data } });
        } catch (error) {
            console.error('Error fetching search results:', error);
            setIsLoading(false);
            // Handle error (e.g., show error message to user)
        }
    };

    return (
        <main className="flex-grow flex flex-col items-center justify-center p-4 bg-cover bg-center bg-no-repeat bg-white font-Fustat" style={{ backgroundImage: 'url("/bg_scholarlink.png")' }}>
            <div className="bg-white bg-opacity-80 p-8 rounded-lg shadow-xl max-w-5xl w-full">
                <header className="text-center mb-8">
                    <h1 className="text-5xl font-semibold mb-2 text-black font-Fustat font-bold">Explore connected papers in a visual graph</h1>
                    <p className="text-xl text-black">To start, enter a {searchMode === 'keyword' ? 'keyword' : 'prompt'}</p>
                </header>
                <div className="form-control w-full mb-4">
                    <div className="flex justify-center mb-4">
                        <button 
                            className={`btn ${searchMode === 'keyword' ? 'btn-primary' : 'btn-outline'} mr-2`}
                            onClick={() => setSearchMode('keyword')}
                        >
                            Search by keyword
                        </button>
                        <button 
                            className={`btn ${searchMode === 'prompt' ? 'btn-primary' : 'btn-outline'} ml-2`}
                            onClick={() => setSearchMode('prompt')}
                        >
                            Search by prompt
                        </button>
                    </div>
                    <form onSubmit={handleSearch} className="flex shadow-lg">
                        <input
                            type="text"
                            value={searchInput}
                            onChange={(e) => setSearchInput(e.target.value)}
                            placeholder={searchMode === 'keyword' ? "Enter keywords, paper title, DOI or another identifier" : "Enter your prompt"}
                            className="input input-bordered w-full rounded-r-none bg-white"
                        />
                        <button type="submit" className="btn btn-primary rounded-l-none" disabled={isLoading}>
                            {isLoading ? 'Searching...' : 'Search'}
                        </button>
                    </form>
                </div>
            </div>
        </main>
    );
};

export default HomePage;