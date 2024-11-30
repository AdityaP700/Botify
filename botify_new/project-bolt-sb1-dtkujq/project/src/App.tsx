import ChatInterface from './components/ChatInterface';
import { Toaster } from '@/components/ui/toaster';

function App() {
  return (
    <div className="min-h-screen bg-slate-50 p-4 flex items-center justify-center">
      <ChatInterface />
      <Toaster />
    </div>
  );
}

export default App;