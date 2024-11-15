import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

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
  
        if (!data) {
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
        <div className="flex flex-col w-full h-full border rounded-lg shadow-lg bg-gray-800">
            {/* Chat header */}
            <div className="px-4 py-3 bg-purple-700 text-white rounded-t-lg">
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
                            className={`max-w-xs p-3 rounded-lg ${message.sender === 'user'
                                    ? 'bg-purple-500 text-white'
                                    : 'bg-gray-700 text-gray-200'
                                }`}
                        >
                            <p className="text-sm">{message.text}</p>
                            <span className="text-xs opacity-75 block mt-1">
                                {message.timestamp}
                            </span>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-700 text-gray-200 p-3 rounded-lg">
                            <p className="text-sm">Typing...</p>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input form */}
            <form onSubmit={handleSubmit} className="p-4 border-t bg-gray-700">
                <div className="flex space-x-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder="Type your message..."
                        className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 bg-gray-900 text-white placeholder-gray-400"
                    />
                    <button
                        type="submit"
                        className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500"
                        disabled={isLoading}
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            className="send-button"
                        >
                            <path d="M22 2L11 13" />
                            <path d="M22 2L15 22L11 13L2 9L22 2Z" />
                        </svg>
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ChatInterface;
