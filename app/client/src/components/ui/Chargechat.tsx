
import { ChatMessage } from "@chatcomponents/ChatMessage"


const Chargechat = () => {
   
  

  const messages = [
    { text: "Welcome to EnglisChat! How can I help you today?", isUser: false },
    { text: "Hello! I need help with my English.", isUser: true },
    { text: "Sure! What specific areas do you want to improve?", isUser: false },
    { text: "I want to work on my vocabulary and pronunciation.", isUser: true },
    { text: "Great! Let's start with some vocabulary exercises.", isUser: false },
    { text: "Sounds good! What kind of vocabulary?", isUser: true },
    { text: "How about we focus on everyday conversation phrases?", isUser: false },
  ];

  return (
    <>
        {messages.map((msg, index) => (
          <div key={index} >
            <ChatMessage message={<span className="invisible">{msg.text}</span>} isUser={msg.isUser} parpadeo={true} />
          </div>
        ))}
    </>
  )
}

export default Chargechat
               