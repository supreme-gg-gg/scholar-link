import React from 'react';
import { useNavigate } from 'react-router-dom';

const Results = () => {
    const navigate = useNavigate();

    const handleBuildGraph = () => {
        navigate('/graph');
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Paper Suggestions</h1>
            <div className="card bg-base-100 shadow-xl mb-4">
                <div className="card-body">
                    <h2 className="card-title">Finding Chaos in Noisy Systems</h2>
                    <p className="text-sm">Douglas Nychkatl, S. Ellner, Daniel Mccaffrey, et al.</p>
                    <p className="text-sm">1992. 327 Citations, 41 References</p>
                    <p className="text-sm mt-2">In the past twenty years there has been much interest in the physical and biological sciences in nonlinear dynamical systems that appear to have random, unpredictable behavior...</p>
                    <div className="card-actions justify-end mt-2">
                        <button 
                            className="btn btn-primary btn-sm"
                            onClick={handleBuildGraph}
                        >
                            Build Graph
                        </button>
                        <button className="btn btn-outline btn-sm">Save</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Results;