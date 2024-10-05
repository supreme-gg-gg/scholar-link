import React, { useState } from 'react';
import Graph from './graph';

const GraphPage = () => {
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(true);
  const [expandedPaper, setExpandedPaper] = useState(null);

  return (
    <div className="flex h-screen bg-white relative">
      {/* Left Sidebar and Toggle Button */}
      <div className="relative h-full">
        <div className={`bg-white transition-all duration-300 h-full ${leftSidebarOpen ? 'w-80' : 'w-0'} overflow-hidden shadow-lg flex flex-col`}>
          <div className="flex-grow overflow-y-auto">
            <div className="p-4">
              <div className="space-y-4">
                {[1, 2, 3, 4, 5].map((index) => (
                  <div key={index} className="card bg-white shadow-sm">
                    <div className="card-body p-4">
                      <div className="flex justify-between items-center">
                        <h3 className="card-title text-sm text-black  font-Fustat">Paper Title {index}</h3>
                        <button
                          onClick={() => setExpandedPaper(expandedPaper === index ? null : index)}
                          className="text-black/75"
                        >
                          {expandedPaper === index ? '+' : '+'}
                        </button>
                      </div>
                      <p className="text-xs text-base-content/70  font-Fustat">Authors, Year</p>
                      {expandedPaper === index && (
                        <div className="mt-2 text-xs">
                            <p className='text-black/70'>Citations: 42</p>
                            <p className="mt-4 text-sm text-black">In the past twenty years there has been much interest in the physical and biological sciences in nonlinear dynamical systems that appear to have random, unpredictable behavior...</p>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
        <button
          onClick={() => setLeftSidebarOpen(!leftSidebarOpen)}
          className={`absolute top-1/2 -translate-y-1/2 transition-all duration-300 bg-white hover:bg-white p-2 rounded-r-md shadow-lg ${leftSidebarOpen ? 'right-0 translate-x-full' : 'left-0'}`}
        >
          <span className="text-2xl text-black">{leftSidebarOpen ? '◀' : '▶'}</span>
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex-grow p-4 overflow-auto">
        <Graph />
      </div>

      {/* Right Sidebar (AI Chatbot) and Toggle Button */}
      <div className="relative h-full">
        <button
          onClick={() => setRightSidebarOpen(!rightSidebarOpen)}
          className={`absolute top-1/2 -translate-y-1/2 transition-all duration-300 bg-white hover:bg-white p-2 rounded-l-md shadow-lg ${rightSidebarOpen ? 'left-0 -translate-x-full' : 'right-0'}`}
        >
          <span className="text-2xl text-black">{rightSidebarOpen ? '▶' : '◀'}</span>
        </button>
        <div className={`bg-white transition-all duration-300 h-full ${rightSidebarOpen ? 'w-80' : 'w-0'} overflow-hidden shadow-lg flex flex-col`}>
          <div className="flex-grow overflow-y-auto">
            <div className="p-4 text-black/70  font-Fustat">
              <h2 className="text-lg font-semibold mb-4 text-black">AI Chatbot</h2>
              {/* Placeholder for AI Chatbot */}
              <div className="bg-gray-100 p-4 rounded">
                <p className="text-sm">AI CHATBOT CONTAINER IT WILL GO HERE</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphPage;