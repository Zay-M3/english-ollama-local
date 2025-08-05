import { useEffect, useRef, useState } from 'react';

function useWebSocket(url: string) {
    const [messages, setMessages] = useState<string[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const socketRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        socketRef.current = new WebSocket(url);

        socketRef.current.onopen = () => {
            setIsConnected(true);
        };

        socketRef.current.onmessage = (event) => {
            setMessages((prevMessages) => [...prevMessages, event.data]);
        };

        socketRef.current.onclose = () => {
            setIsConnected(false);
        };

        return () => {
            socketRef.current?.close();
        };
    }, [url]);

    const sendMessage = (message: { action: string; message: string }) => {
        if (!isConnected) {
            console.error("WebSocket is not connected.");
            return;
        }
        socketRef.current?.send(JSON.stringify(message));
    };

    return { messages, isConnected, sendMessage };
}

export default useWebSocket;