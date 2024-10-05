import React, { useState } from 'react';
import Graph from './graph';

const GraphPage = () => {
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen bg-white relative">
      {/* Left Sidebar and Toggle Button */}
      <div className="relative">
        <div className={`bg-bwhite transition-all duration-300 ${leftSidebarOpen ? 'w-80' : 'w-0'} overflow-hidden`}>
          <div className="p-4">
            <div className="space-y-4">
              {[1, 2, 3, 4, 5].map((index) => (
                <div key={index} className="card bg-white shadow-sm">
                  <div className="card-body p-4">
                    <h3 className="card-title text-sm text-black">Paper Title {index}</h3>
                    {/* there should be some indicator here that the first paper is the origin paper */}
                    <p className="text-xs text-base-content/70">Authors, Year</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        <button
          onClick={() => setLeftSidebarOpen(!leftSidebarOpen)}
          className={`absolute top-1/2 -translate-y-1/2 transition-all duration-300 bg-white hover:bg-white p-2 rounded-r-md shadow-md ${leftSidebarOpen ? 'right-0 translate-x-full' : 'left-0'}`}
        >
          <span className="text-2xl text-black">{leftSidebarOpen ? '◀' : '▶'}</span>
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex-grow p-4 overflow-auto">
        <h1 className="text-2xl font-bold mb-4">GRAPH HERE</h1>
        <Graph />
      </div>

      {/* Right Sidebar and Toggle Button */}
      <div className="relative">
        <button
          onClick={() => setRightSidebarOpen(!rightSidebarOpen)}
          className={`absolute top-1/2 -translate-y-1/2 transition-all duration-300 bg-white hover:bg-white p-2 rounded-l-md shadow-md ${rightSidebarOpen ? 'left-0 -translate-x-full' : 'right-0'}`}
        >
          <span className="text-2xl text-black">{rightSidebarOpen ? '▶' : '◀'}</span>
        </button>
        <div className={`bg-white transition-all duration-300 ${rightSidebarOpen ? 'w-80' : 'w-0'} overflow-hidden`}>
          <div className="p-4 text-black/70">
            <h2 className="text-lg font-semibold mb-4 text-black">Finding Chaos in Noisy Systems</h2>
            <p className="text-sm  mb-2">Douglas Nychkati + 7 authors · Neural Networks</p>
            <p className="text-sm mb-2">1992, Journal of the royal statistical society series b-methodological</p>
            <p className="text-sm mb-4">327 Citations</p>
            <div className="space-y-2">
              <div className="dropdown">
                <ul tabIndex={0} className="dropdown-content z-[1] menu p-2 shadow bg-white rounded-box w-52">
                  <li><a>Option 1</a></li>
                  <li><a>Option 2</a></li>
                </ul>
              </div>
              <button className="btn btn-sm btn-outline w-full text-black">Save</button>
            </div>
            <p className="mt-4 text-sm text-black">In the past twenty years there has been much interest in the physical and biological sciences in nonlinear dynamical systems that appear to have random, unpredictable behavior...</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphPage;