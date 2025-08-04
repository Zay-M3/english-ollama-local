import { useState } from "react";
import { ChatHeader } from "@chatcomponents/ChatHeader";
import { ChatMessage } from "@chatcomponents/ChatMessage";
import { ChatInput } from "@chatcomponents/ChatInput";

function Chat() {
  const [messages, setMessages] = useState([
    { text: "Welcome to EnglisChat! How can I help you today?", isUser: false }
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() === "") return;
    setMessages([...messages, { text: input, isUser: true }]);
    setInput("");
    console.log("Mensaje enviado:", input);

  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex items-center justify-center">
      <div className="w-full max-w-md h-[600px] flex flex-col rounded-xl shadow-lg bg-white border">
        <ChatHeader />
        <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-gray-50">
          {messages.map((msg, idx) => (
            <ChatMessage key={idx} message={msg.text} isUser={msg.isUser} />
          ))}
        </div>
        <ChatInput
          value={input}
          onChange={e => setInput(e.target.value)}
          onSend={handleSend}
        />
      </div>
    </div>
  );
}

export default Chat;
