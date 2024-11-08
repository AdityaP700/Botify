import React from 'react';

const Header = () => {
  return (
    <div className="flex items-center justify-between p-4 rounded-lg bg-gradient-to-r from-blue-500 to-blue-400 text-white max-w-sm mx-auto shadow-md">
      <div className="flex items-center space-x-3">
        <img
          src="https://via.placeholder.com/40" 
          alt="Profile"
          className="w-10 h-10 rounded-full"
        />
        <div>
          <p className="text-sm">Chat with</p>
          <p className="font-semibold">Atlas</p>
        </div>
      </div>
      <div className="flex items-center space-x-2">
        <button className="text-xl">⋮</button>
        <button className="text-xl">⌄</button>
      </div>
    </div>
  );
};

export default Header;
