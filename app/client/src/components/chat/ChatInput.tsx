import type { ChatInputProps } from "@chatutils/chatform";

export function ChatInput({ value , onChange, onSend }: ChatInputProps) {
  return (
    <div className="flex items-center gap-2 p-4 border-t bg-white">
      <input
        className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-400"
        type="text"
        placeholder="Escribe tu mensaje..."
        value={value}
        onChange={onChange}
        onKeyDown={e => e.key === "Enter" && onSend()}
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded-full hover:bg-blue-600 transition"
        onClick={onSend}
      >
        Enviar
      </button>
    </div>
  );
}