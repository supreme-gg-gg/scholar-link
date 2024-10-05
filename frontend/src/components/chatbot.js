import React from "react";

const ChatBotEmbed = () => {
  return (
    <div style={{ width: "100%", height: "600px" }}>
      <iframe
        id="chatbot-iframe"
        src="http://localhost:8502"
        // This depends on whether this or the graph app is launched first
        width="100%"
        height="100%"
        frameBorder="0"
      ></iframe>
    </div>
  );
};

export default ChatBotEmbed;
