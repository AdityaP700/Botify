import React, { useState, useRef, useEffect } from 'react';


const axios = require('axios').default;

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = {
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      console.log('Sending request with prompt:', inputValue);
      
      const {data} = await axios.post("http://localhost:8000/groq", {
        prompt: inputValue,
        max_tokens: 500,
        temperature: 0.7,
        top_p: 0.9,
        stop_sequences: ["Human:", "Assistant:"]
      },{
        headers: {
          'Content-Type': 'application/json' // Set the Content-Type header
      }
      });

      alert('Raw response:', data);

      if (data) {
        throw new Error('No message in response');
      }

      // Add the response from the assistant to the messages
      const botMessage = {
        text: data,  // Using the correct key
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };
      
      console.log('Adding bot message:', botMessage.data);
      setMessages(prev => [...prev, botMessage]);
      console.log(messages)

    } catch (error) {
      console.error("Error details:", {
        message: 'gogo',
        response: error.response?.data,
        status: error.response?.status
      });

      const errorMessage = {
        text: "Sorry, something went wrong. Please try again.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col w-full h-full border rounded-lg shadow-lg bg-white">
      {/* Chat header */}
      <div className="px-4 py-3 bg-blue-600 text-white rounded-t-lg">
        <h2 className="text-lg font-semibold">Chatbot</h2>
      </div>

      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[75%] p-3 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              <p className="text-sm break-words">{message.message}</p>
              <span className="text-xs opacity-75 block mt-1">
                {message.timestamp}
              </span>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-800 p-3 rounded-lg">
              <p className="text-sm">Typing...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            disabled={isLoading}
          >

          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;