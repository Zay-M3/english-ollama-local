import type { ChatInputProps } from "@chatutils/chatform";
import { Button } from "@ui/Button";

export function ChatInput({ value , onChange, onSend, disabled }: ChatInputProps) {
  return (
    <div className="flex items-center gap-2 p-4 border-t bg-white">
      <input
        className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-400"
        type="text"
        placeholder="Type your message..."
        value={value}
        onChange={onChange}
        onKeyDown={e => e.key === "Enter" && onSend()}
        disabled={disabled}
      />
      <Button
        label="Send"
        onClick={onSend}
        className="px-6 py-2 rounded-full"
        disabled={disabled}
      />
    </div>
  );
}