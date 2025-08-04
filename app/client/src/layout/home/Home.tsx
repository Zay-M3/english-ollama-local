import { Button } from "@ui/Button";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  return (
    <>
        <div className="bg-gray-100 min-h-screen flex items-center justify-center flex-col gap-2">
            <div>
                <img src="/icon_english.webp" alt="Logo" className="w-50 mb-4" />
            </div>
            <div className="text-center mb-2">
                <h1 className="text-4xl font-bold">Welcome to EnglishChat!</h1>
                <h2 className="text-lg text-gray-700">Your AI-powered English learning assistant.</h2>
                <p className="text-gray-500 max-w-lg text-[12px]">Our goal is for you to learn English by speaking conventionally with your AI agent, for free, and on the topic of your interest. She'll correct you and continue with a pleasant conversation. Have fun!</p>
            </div>
            <Button
              label="Start Chatting"
                className="px-6 py-2 bg-blue-500 text-white hover:bg-blue-600 hover:scale-105 transition"
              onClick={() => navigate("/chat")}
            />
       </div>
    </>
    
  )
}

export default Home