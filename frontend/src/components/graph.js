import React, { useState, useEffect, useRef } from 'react';

const Graph = ({ papers, matrix }) => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [transform, setTransform] = useState({ x: 0, y: 0, scale: 1 });
  const [hoveredNode, setHoveredNode] = useState(null);
  const svgRef = useRef(null);

  const primaryColor = '#7884fc';  
  const primaryColorHover = '#4657FB';  

  useEffect(() => {
    if (!papers || !matrix || papers.length === 0 || matrix.length === 0) return;

    const width = 800;
    const height = 600;
    const nodeRadius = 40;

    // Create nodes
    const newNodes = papers.map((paper, index) => ({
      id: index,
      name: paper.title,
      x: Math.random() * (width - 2 * nodeRadius) + nodeRadius,
      y: Math.random() * (height - 2 * nodeRadius) + nodeRadius,
    }));

    // Create edges
    const newEdges = [];
    for (let i = 0; i < matrix.length; i++) {
      for (let j = i + 1; j < matrix[i].length; j++) {
        if (matrix[i][j] !== -1) {
          newEdges.push({
            source: i,
            target: j,
            strength: matrix[i][j],
          });
        }
      }
    }

    setNodes(newNodes);
    setEdges(newEdges);

    // Apply force-directed layout
    const simulation = () => {
      const force = 0.1;
      const minDistance = nodeRadius * 2;

      newNodes.forEach((node, i) => {
        newNodes.forEach((otherNode, j) => {
          if (i !== j) {
            const dx = node.x - otherNode.x;
            const dy = node.y - otherNode.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < minDistance) {
              const angle = Math.atan2(dy, dx);
              const moveDistance = (minDistance - distance) / 2;

              node.x += Math.cos(angle) * moveDistance * force;
              node.y += Math.sin(angle) * moveDistance * force;
              otherNode.x -= Math.cos(angle) * moveDistance * force;
              otherNode.y -= Math.sin(angle) * moveDistance * force;

              // Keep nodes within bounds
              node.x = Math.max(nodeRadius, Math.min(width - nodeRadius, node.x));
              node.y = Math.max(nodeRadius, Math.min(height - nodeRadius, node.y));
              otherNode.x = Math.max(nodeRadius, Math.min(width - nodeRadius, otherNode.x));
              otherNode.y = Math.max(nodeRadius, Math.min(height - nodeRadius, otherNode.y));
            }
          }
        });
      });

      setNodes([...newNodes]);
    };

    const interval = setInterval(simulation, 50);
    return () => clearInterval(interval);
  }, [papers, matrix]);

  const handleWheel = (e) => {
    e.preventDefault();
    const scaleFactor = e.deltaY > 0 ? 0.95 : 1.05;
    setTransform(prev => ({
      ...prev,
      scale: Math.max(0.1, Math.min(10, prev.scale * scaleFactor)),
    }));
  };

  const handleMouseDown = (e) => {
    const startX = e.clientX;
    const startY = e.clientY;
    const startTransform = { ...transform };

    const handleMouseMove = (e) => {
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      setTransform({
        ...startTransform,
        x: startTransform.x + dx / transform.scale,
        y: startTransform.y + dy / transform.scale,
      });
    };

    const handleMouseUp = () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  const calculateLineThickness = (strength) => {
    const minThickness = 1;
    const maxThickness = 10;
    const minStrength = Math.min(...edges.map(e => e.strength));
    const maxStrength = Math.max(...edges.map(e => e.strength));
    
    return minThickness + ((strength - minStrength) / (maxStrength - minStrength)) * (maxThickness - minThickness);
  };

  return (
    <svg
      ref={svgRef}
      width="3840"
      height="2160"
      onWheel={handleWheel}
      onMouseDown={handleMouseDown}
      style={{ cursor: 'move' }}
    >
      <defs>
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      <g transform={`translate(${transform.x},${transform.y}) scale(${transform.scale})`}>
        {edges.map((edge, index) => (
          <line
            key={index}
            x1={nodes[edge.source].x}
            y1={nodes[edge.source].y}
            x2={nodes[edge.target].x}
            y2={nodes[edge.target].y}
            stroke={primaryColor}
            strokeWidth={calculateLineThickness(edge.strength)}
          />
        ))}
        {nodes.map((node) => (
          <g 
            key={node.id}
            onMouseEnter={() => setHoveredNode(node.id)}
            onMouseLeave={() => setHoveredNode(null)}
          >
            <circle
              cx={node.x}
              cy={node.y}
              r="40"
              fill={hoveredNode === node.id ? primaryColorHover : primaryColor}
              stroke={hoveredNode === node.id ? primaryColorHover : "transparent"}
              strokeWidth="3"
              filter={hoveredNode === node.id ? "url(#glow)" : "none"}
            />
            <text
              x={node.x}
              y={node.y}
              textAnchor="middle"
              dominantBaseline="central"
              fontSize="14"
              fontWeight={hoveredNode === node.id ? "bold" : "normal"}
              fill="white"
            >
              {node.name}
            </text>
          </g>
        ))}
      </g>
    </svg>
  );
};

export default Graph;