import React, { createContext, useContext, useState } from "react";

const MessageContext = createContext();

export const MessageProvider = ({ children }) => {
  const [message, setMessage] = useState({ type: "", text: "" });

  const setMessageContext = (type, text) => {
    setMessage({ type, text });
  };

  const clearMessage = () => {
    setMessage({ type: "", text: "" });
  };

  return (
    <MessageContext.Provider
      value={{ message, setMessage: setMessageContext, clearMessage }}
    >
      {children}
    </MessageContext.Provider>
  );
};

export const useMessage = () => useContext(MessageContext);
