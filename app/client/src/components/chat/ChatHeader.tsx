

export function ChatHeader() {
  return (
    <div className="p-4 border-b bg-white flex items-center gap-2">
      <span className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></span>
      <h1 className="text-lg font-semibold text-gray-800">EnglisChat</h1>
      <span className="ml-auto text-xs text-gray-400">Llama3 Local</span>
    </div>
  );
}