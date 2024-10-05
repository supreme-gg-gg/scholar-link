import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import Graph from './graph';

const GraphPage = () => {
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(true);
  const [expandedPaper, setExpandedPaper] = useState(null);
  const [papers, setPapers] = useState([]);
  const [matrix, setMatrix] = useState([]);
  const [hoveredPaperIndex, setHoveredPaperIndex] = useState(null);
  const [originPaperIndex, setOriginPaperIndex] = useState(null);
  const [allPapers, setAllPapers] = useState([]);  // Store all papers from initial search

  const location = useLocation();
  const paperRefs = useRef({});
  const sidebarContentRef = useRef(null);

  useEffect(() => {
    if (location.state && location.state.graphData) {
      const { papers, matrix } = location.state.graphData;
      setPapers(papers);
      setMatrix(matrix);
      setAllPapers(papers);  // Store all papers from initial search
      setOriginPaperIndex(location.state.originPaperIndex);
    }
  }, [location]);

  useEffect(() => {
    if (expandedPaper !== null && paperRefs.current[expandedPaper] && sidebarContentRef.current) {
      const paperElement = paperRefs.current[expandedPaper];
      const sidebarContent = sidebarContentRef.current;
      
      const paperTop = paperElement.offsetTop;
      const sidebarScrollTop = sidebarContent.scrollTop;
      const sidebarHeight = sidebarContent.clientHeight;

      if (paperTop < sidebarScrollTop || paperTop > sidebarScrollTop + sidebarHeight) {
        sidebarContent.scrollTo({
          top: paperTop - sidebarHeight / 2,
          behavior: 'smooth'
        });
      }
    }
  }, [expandedPaper]);

  const originColor = '#FF4500';  // Bright orange-red for the origin paper

  const handleSetAsOrigin = async (index) => {
    try {
      const response = await fetch('http://localhost:5000/graph', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ index: allPapers[index].index }),  // Use the original index from allPapers
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const newGraphData = await response.json();
      
      // Update your state with the new graph data
      setPapers(newGraphData.papers);
      setMatrix(newGraphData.matrix);
      setOriginPaperIndex(0);  // The new origin will always be at index 0 in the new set of papers
      setExpandedPaper(null);  // Close any expanded paper view
    } catch (error) {
      console.error('Error regenerating graph:', error);
      // Handle the error (e.g., show an error message to the user)
    }
  };

  const handleNodeClick = (index) => {
    setExpandedPaper(index);
    setLeftSidebarOpen(true);  // Ensure the sidebar is open when a node is clicked
  };

  return (
    <div className="flex h-screen bg-white relative">
      {/* Left Sidebar and Toggle Button */}
      <div className="relative h-full flex flex-col">
        <div className={`bg-white transition-all duration-300 h-full ${leftSidebarOpen ? 'w-80' : 'w-0'} overflow-hidden shadow-lg flex flex-col`}>
          {/* Navbar */}
          <div className="p-4 border-b">
            <h2 className="text-lg font-semibold text-black">Papers</h2>
          </div>
          {/* Scrollable content */}
          <div ref={sidebarContentRef} className="flex-grow overflow-y-auto">
            <div className="p-4">
              <div className="space-y-4">
                {papers.map((paper, index) => (
                  <div 
                    key={paper.index}  // Use the original index as key
                    ref={el => paperRefs.current[index] = el}
                    className={`card bg-white shadow-sm ${index === originPaperIndex ? 'border-2 border-orange-500' : ''} ${expandedPaper === index ? 'ring-2 ring-blue-500' : ''}`}
                    onMouseEnter={() => setHoveredPaperIndex(index)}
                    onMouseLeave={() => setHoveredPaperIndex(null)}
                    style={{
                      backgroundColor: index === originPaperIndex ? 'rgba(255, 69, 0, 0.1)' : 'white'
                    }}
                  >
                    <div className="card-body p-4">
                      <div className="flex justify-between items-center">
                        <h3 className="card-title text-sm text-black font-Fustat">
                          <a href={paper.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                            {paper.title}
                          </a>
                        </h3>
                        <button
                          onClick={() => setExpandedPaper(expandedPaper === index ? null : index)}
                          className="text-black/75"
                        >
                          {expandedPaper === index ? '-' : '+'}
                        </button>
                      </div>
                      <p className="text-xs text-base-content/70 font-Fustat">
                        {paper.authors.join(', ')}, {new Date(paper.date).getFullYear()}
                      </p>
                      {expandedPaper === index && (
                        <div className="mt-2 text-xs">
                          <button
                            onClick={() => handleSetAsOrigin(index)}
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-2 rounded text-xs mb-2"
                          >
                            Set as origin
                          </button>
                          <p className="mt-2 text-sm text-black">{paper.summary}</p>
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
          <span className="text-2xl text-primary">{leftSidebarOpen ? '◀' : '▶'}</span>
        </button>
      </div>
      {/* Main Content Area */}
      <div className="flex-grow p-4 overflow-auto">
        <Graph 
          papers={papers} 
          matrix={matrix} 
          hoveredPaperIndex={hoveredPaperIndex}
          originPaperIndex={originPaperIndex}
          onNodeClick={handleNodeClick}
        />
      </div>
      {/* Right Sidebar (AI Chatbot) and Toggle Button */}
      <div className="relative h-full flex flex-col">
        <button
          onClick={() => setRightSidebarOpen(!rightSidebarOpen)}
          className={`absolute top-1/2 -translate-y-1/2 transition-all duration-300 bg-white hover:bg-white p-2 rounded-l-md shadow-lg ${rightSidebarOpen ? 'left-0 -translate-x-full' : 'right-0'}`}
        >
          <span className="text-2xl text-primary">{rightSidebarOpen ? '▶' : '◀'}</span>
        </button>
        <div className={`bg-white transition-all duration-300 h-full ${rightSidebarOpen ? 'w-80' : 'w-0'} overflow-hidden shadow-lg flex flex-col`}>
          {/* Navbar */}
          <div className="p-4 border-b">
            <h2 className="text-lg font-semibold text-black">AI Chatbot</h2>
          </div>
          {/* Scrollable content */}
          <div className="flex-grow overflow-y-auto">
            <div className="p-4 text-black/70 font-Fustat">
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