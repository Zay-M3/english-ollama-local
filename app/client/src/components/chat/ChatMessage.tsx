import type { ChatMessageProps } from "@chatutils/chatform";


export function ChatMessage({ message, isUser, parpadeo, fixmessage }: ChatMessageProps) {
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
      <div
        className={`max-w-xs px-4 py-2 rounded-lg shadow
          ${isUser
            ? "bg-blue-500 text-white rounded-br-none"
            : !fixmessage ? "bg-gray-200 text-gray-900 rounded-bl-none" : "bg-amber-200 text-gray-900 rounded-bl-none"
          }
          ${parpadeo ? "animate-pulse" : ""
          }
          `}
      >
        {message}
      </div>
    </div>
  );
}