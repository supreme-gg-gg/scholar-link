import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
    const navigate = useNavigate();

    const handleRedirect = (e) => {
        e.preventDefault();
        navigate('/results');
    };

    return (
        <main className="flex-grow flex flex-col items-center justify-center p-4 bg-white">
            <header className="text-center mb-8">
                <h1 className="text-6xl font-semibold mb-2 text-black">Explore connected papers in a visual graph</h1>
                <p className="text-xl text-black">To start, enter a paper identifier</p>
            </header>
            <div className="form-control w-full max-w-3xl">
                <form onSubmit={handleRedirect} className="flex shadow-lg">
                    <input
                        type="text"
                        placeholder="Search by keywords, paper title, DOI or another identifier"
                        className="input input-bordered w-full rounded-r-none bg-white"
                    />
                    <button type="submit" className="btn btn-primary rounded-l-none">Build a graph</button>
                </form>
            </div>
        </main>
    );
};

export default HomePage;