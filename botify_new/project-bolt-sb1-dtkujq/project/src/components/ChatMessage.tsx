import { Bot, User } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatMessageProps {
  message: {
    text: string;
    sender: 'user' | 'bot';
    timestamp: string;
  };
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.sender === 'user';

  return (
    <div className={cn('flex items-start gap-3 group', isUser && 'flex-row-reverse')}>
      <div className={cn(
        'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow',
        isUser ? 'bg-blue-600 text-white' : 'bg-white'
      )}>
        {isUser ? <User size={18} /> : <Bot size={18} />}
      </div>
      <div className={cn(
        'flex flex-col gap-1 min-w-0 max-w-[calc(100%-4rem)]',
        isUser && 'items-end'
      )}>
        <div className={cn(
          'rounded-lg px-4 py-2.5 shadow-md',
          isUser ? 'bg-blue-600 text-white' : 'bg-white border'
        )}>
          <p className="prose break-words">{message.text}</p>
        </div>
        <span className="px-2 text-xs text-muted-foreground">
          {message.timestamp}
        </span>
      </div>
    </div>
  );
}