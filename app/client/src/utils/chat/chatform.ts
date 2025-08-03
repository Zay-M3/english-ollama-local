export interface ChatInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSend: () => void;
}

export interface ChatMessageProps {
  message: string;
  isUser: boolean;
}