import React, { createContext, useContext, useState } from "react";

const MessageContext = createContext();

export const MessageProvider = ({ children }) => {
  const [message, setMessage] = useState("");

  const setMessageContent = (type, text) => {
    setMessage({ type, text });
  };

  return (
    <MessageContext.Provider value={{ message, setMessage: setMessageContent }}>
      {children}
    </MessageContext.Provider>
  );
};

export const useMessage = () => useContext(MessageContext);
