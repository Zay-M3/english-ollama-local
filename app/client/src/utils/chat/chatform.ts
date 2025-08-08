export interface ChatInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSend: () => void;
  disabled?: boolean;
}

export interface ChatMessageProps {
  message: React.ReactNode;
  isUser: boolean;
  parpadeo?: boolean;
  fixmessage: boolean;
}