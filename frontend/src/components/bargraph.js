import React from "react";

const BarGraphEmbed = () => {
  return (
    <div style={{ width: "100%", height: "600px" }}>
      <iframe
        id="bargraph-iframe"
        src="http://localhost:8503"
        // This depends on whether this or the graph app is launched first
        width="100%"
        height="100%"
        frameBorder="0"
      ></iframe>
    </div>
  );
};

export default BarGraphEmbed;
