import { createContext, useContext, useState, useEffect } from "react";

const ChatContext = createContext(null);

const STORAGE_KEY = "ai_cfo_chat_messages";

export function ChatProvider({ children }) {
  const [messages, setMessages] = useState(() => {
    try {
      const saved = sessionStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    } catch {
      // sessionStorage full or unavailable — chat still works, just won't persist
    }
  }, [messages]);

  function addMessage(message) {
    setMessages((prev) => [...prev, message]);
  }

  function clearMessages() {
    setMessages([]);
    sessionStorage.removeItem(STORAGE_KEY);
  }

  return (
    <ChatContext.Provider value={{ messages, addMessage, clearMessages, setMessages }}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  return useContext(ChatContext);
}