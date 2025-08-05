import { use, useEffect } from "react"


const SliderChat = () => {

  useEffect(() => {
    
  }, []);

  return (
    <>
      <div className="px-2 py-1 text-2xl w-25 font-medium leading-none text-center items-center text-blue-600 bg-blue-500 rounded-full animate-pulse flex justify-center">
        <div className="mx-1 animate-bounce" style={{ animationDelay: "0ms" }}>•</div>
        <div className="mx-1 animate-bounce" style={{ animationDelay: "200ms" }}>•</div>
        <div className="mx-1 animate-bounce" style={{ animationDelay: "300ms" }}>•</div>
      </div>
    </>
  )
}

export default SliderChat