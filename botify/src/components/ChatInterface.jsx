/* global chrome */
import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';

// API URL now includes /api/v1 prefix
const API_URL = 'http://localhost:8000/api/v1';
const isExtension = window.chrome && chrome.runtime && chrome.runtime.id;

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleExtensionRequest = async (endpoint, data) => {
    return new Promise((resolve, reject) => {
      chrome.runtime.sendMessage(
        { type: 'API_REQUEST', endpoint, data },
        (response) => {
          if (chrome.runtime.lastError) {
            reject(new Error(chrome.runtime.lastError.message));
          } else if (!response || !response.success) {
            reject(new Error(response?.error || 'Request failed'));
          } else {
            resolve(response.data);
          }
        }
      );
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = inputValue.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInputValue('');
    setIsLoading(true);

    try {
      let response;
      // Check if it's a search query
      if (userMessage.toLowerCase().startsWith('/search ')) {
        const query = userMessage.slice(8); // Remove '/search ' prefix
        const searchData = { query, top_k: 3 };
        
        if (isExtension) {
          response = await handleExtensionRequest('/search', searchData);
        } else {
          const axiosResponse = await axios.post(
            `${API_URL}/search`,
            searchData,
            { headers: { 'Content-Type': 'application/json' } }
          );
          response = axiosResponse.data;
        }

        if (!response) {
          throw new Error('No search results returned');
        }

        const searchResponse = Array.isArray(response) ? response.map(result => 
          `Score: ${(result.score * 100).toFixed(1)}% - ${result.text}`
        ).join('\n\n') : 'No results found';

        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `Here are the search results:\n\n${searchResponse}`
        }]);
      } else {
        // Regular chat message
        const chatData = {
          message: userMessage
        };

        if (isExtension) {
          response = await handleExtensionRequest('/chat', chatData);
        } else {
          const axiosResponse = await axios.post(
            `${API_URL}/chat`,
            chatData,
            { headers: { 'Content-Type': 'application/json' } }
          );
          response = axiosResponse.data;
        }

        if (!response) {
          throw new Error('No response from chat endpoint');
        }

        setMessages(prev => [...prev, {
          role: 'assistant',
          content: response.response
        }]);
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, there was an error processing your request: ' + error.message
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full rounded-lg shadow-lg bg-white">
      <div className="px-6 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-t-lg">
        <h2 className="text-xl font-bold">Atlas</h2>
        <p className="text-sm opacity-75">Your AI Assistant</p>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-6" aria-live="polite">
        <AnimatePresence>
          {messages.map((message, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-4 rounded-2xl shadow-sm ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : message.content && message.content.startsWith('Sorry, there was an error')
                      ? 'bg-red-100 text-red-600'
                      : 'bg-gray-100 text-gray-800'
                }`}
              >
                <div className="prose prose-sm">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
              </div>
            </motion.div>
          ))}
          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="bg-gray-100 p-4 rounded-2xl shadow-sm">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
        <div className="flex space-x-3">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type a message or '/search query' to search..."
            className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none"
            disabled={isLoading}
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;