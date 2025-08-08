import { useState } from "react";
import { ChatHeader } from "@chatcomponents/ChatHeader";
import { ChatMessage } from "@chatcomponents/ChatMessage";
import { ChatInput } from "@chatcomponents/ChatInput";
import SliderChat from "@ui/SliderChat";
import useWebSocket from "@chatcomponents/WebSocket";
import { useRef, useEffect } from "react";
import Chargechat from "@ui/Chargechat";

function Chat() {
   const { messages, sendMessage } = useWebSocket("ws://localhost:3000/ws/chat");

  const [chatMessages, setChatMessages] = useState([
    { text: "Welcome to EnglisChat! How can I help you day?", isUser: false, parpadeo:false, fixmessage : false }
  ]);

  const [input, setInput] = useState("");
  const [sliderVisible, setSliderVisible] = useState(false);
  const [chargeChat, setChargeChat] = useState(true);

  const lastMessageIndex = useRef(0);
  const responseRef = useRef(0)

  const handleSend = () => {
    if (input.trim() === "") return;
    setChatMessages(prev => [...prev, { text: input, isUser: true, parpadeo : false, fixmessage : false }]);
    setInput("");
    responseRef.current = 2
    setSliderVisible(true); 
    for (const action of ["response", "fix"]) {
      sendMessage({ action, message: input });
    }
  };

  const handleCall = async () => {
    try {
      await fetch("http://localhost:3000/api/v1/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: "How are you?"})
      })
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setChargeChat(false);
    }
  }

  useEffect(() => {
    const updateMessages = async () => {
      setChargeChat(true);
      await handleCall();
    };
    updateMessages();
  }, []);

  useEffect(() => {
    const diff = messages.length - lastMessageIndex.current;
    if (diff > 0) {
      const newMessages = messages.slice(lastMessageIndex.current);
      newMessages.forEach((msg) => {
        const parsedMsg = JSON.parse(msg);
        setChatMessages((prev) => [
          ...prev,
          { text: parsedMsg.content, isUser: false, parpadeo : false, fixmessage : parsedMsg.fixmessage },
        ]);
        if (responseRef.current > 0 && (parsedMsg.type === "response" || parsedMsg.type === "fix")) { responseRef.current--; if (responseRef.current === 0) setSliderVisible(false);}
      });
      lastMessageIndex.current = messages.length;
    }
  }, [messages]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex items-center justify-center">
      <div className="w-full max-w-md h-[600px] flex flex-col rounded-xl shadow-lg bg-white border">
        <ChatHeader />
        <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-gray-50">
          {chargeChat ? <Chargechat /> : chatMessages.map((msg, idx) => (
            <ChatMessage key={idx} message={msg.text} isUser={msg.isUser} fixmessage={msg.fixmessage} />
          ))}
          {sliderVisible && <SliderChat />}
        </div>
        <ChatInput
          value={input}
          onChange={e => setInput(e.target.value)}
          onSend={handleSend}
          disabled={chargeChat || sliderVisible}
        />
      </div>
    </div>
  );
}

export default Chat;
