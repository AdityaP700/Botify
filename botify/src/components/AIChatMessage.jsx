import React from 'react';

const AIChatMessage = ({ messages }) => {
  return (
    <div className="flex flex-col space-y-4 p-4">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'
            }`}
        >
          <div className="flex max-w-[80%] items-start space-x-2">
            {message.type === 'ai' && (
              <div className="min-h-8 min-w-8 max-h-8 max-w-8 rounded-full bg-gray-200 overflow-hidden">
                <img
                  src={"https://cdn3.iconfinder.com/data/icons/earth-and-space/512/saturn-1024.png"}
                  alt="AI Avatar"
                  className="w-full h-full object-cover"
                />
              </div>
            )}
            <div className="flex flex-col space-y-1">
              {message.type === 'ai' && (
                <span className="text-sm text-gray-400">{message.name}</span>
              )}
              <div
                className={`rounded-2xl px-4 py-2 ${message.type === 'user'
                    ? 'bg-[#d37abc] text-black font-normal'
                    : 'bg-gray-800 text-white'
                  }`}
              >
                <p className="text-[0.925rem]">{message.text}</p>
              </div>

              <span className="text-xs text-gray-500">{message.timestamp}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default AIChatMessage;