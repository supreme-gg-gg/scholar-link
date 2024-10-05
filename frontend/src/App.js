import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import NavBar from './components/navBar';
import Results from './components/results';
import GraphPage from './components/graphPage';
import HomePage from './components/homePage'
import Graph from './components/graph';

const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-base-100 flex flex-col">
        <NavBar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/graph" element={<GraphPage />} />
          <Route path="/results" element={<Results />} />
          <Route path="/contact" element={<div></div>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;