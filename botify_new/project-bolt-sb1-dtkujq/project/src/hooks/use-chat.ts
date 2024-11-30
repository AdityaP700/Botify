import { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

interface ChatResponse {
  message: string;
  error?: string;
}

export function useChat() {
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (message: string): Promise<ChatResponse> => {
    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message,
      });
      
      setError(null);
      return response.data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);
      throw err;
    }
  };

  return {
    sendMessage,
    error,
  };
}
