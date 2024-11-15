import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';

const isExtension = window.chrome && chrome.runtime && chrome.runtime.id;

const ChatInterface = () => {
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem('chatMessages');
    return saved ? JSON.parse(saved) : [];
  });
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const audioRef = useRef(new Audio('/message.mp3'));

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(() => {
    scrollToBottom();
    localStorage.setItem('chatMessages', JSON.stringify(messages));
  }, [messages]);

  const playMessageSound = () => {
    audioRef.current.play().catch(e => console.log('Audio play failed:', e));
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
      hour: 'numeric',
      minute: 'numeric',
      hour12: true
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    setError(null);

    const userMessage = {
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      let response;
      
      if (isExtension) {
        // Use chrome.runtime.sendMessage in extension mode
        response = await new Promise((resolve, reject) => {
          chrome.runtime.sendMessage({
            type: 'API_REQUEST',
            data: {
              prompt: inputValue,
              max_tokens: 500,
              temperature: 0.7,
              top_p: 0.9,
              stop_sequences: ["Human:", "Assistant:"],
            }
          }, response => {
            if (response.success) {
              resolve({ data: response.data });
            } else {
              reject(new Error(response.error));
            }
          });
        });
      } else {
        // Use axios in local mode
        response = await axios.post(
          "http://localhost:8000/groq",
          {
            prompt: inputValue,
            max_tokens: 500,
            temperature: 0.7,
            top_p: 0.9,
            stop_sequences: ["Human:", "Assistant:"],
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );
      }

      const botMessage = {
        text: response.data,
        sender: 'bot',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, botMessage]);
      playMessageSound();

    } catch (error) {
      console.error("Error:", error);
      setError(
        error.response?.data?.message || error.message || 
        "Sorry, something went wrong. Please try again."
      );
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
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-4 rounded-2xl shadow-sm ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <div className="prose prose-sm">
                  <ReactMarkdown>{message.text}</ReactMarkdown>
                </div>
                <span className="text-xs opacity-75 block mt-2">
                  {formatTimestamp(message.timestamp)}
                </span>
              </div>
            </motion.div>
          ))}
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="bg-gray-100 p-4 rounded-2xl shadow-sm">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-red-100 text-red-600 p-4 rounded-lg text-sm"
          >
            {error}
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
        <div className="flex space-x-3">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            disabled={isLoading}
          />
          <button
            type="submit"
            className={`px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all ${
              isLoading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            disabled={isLoading}
          >
            <Send size={20} />
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
