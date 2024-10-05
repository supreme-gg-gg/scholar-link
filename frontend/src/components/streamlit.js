import React from 'react';

const StreamlitEmbed = () => {
  return (
    <div style={{ width: '100%', height: '600px' }}>
      <iframe
        src="http://localhost:8501"
        width="100%"
        height="100%"
        frameBorder="0"
      ></iframe>
    </div>
  );
};

export default StreamlitEmbed;    