import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";
import { useMessage } from "./MessageContext";

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [userInfo, setUserInfo] = useState({
    username: "",
    email: "",
    balance: 0,
  });
  const { setMessage } = useMessage();

  useEffect(() => {
    const fetchUserInfo = async () => {
      const token = localStorage.getItem("token");

      if (token) {
        try {
          const response = await axios.get("http://localhost:8000/users/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          setUserInfo(response.data);
        } catch (error) {
          setMessage("error", "Erro ao buscar informações do usuário.");
        }
      }
    };

    fetchUserInfo();
  }, [setMessage]);

  return (
    <UserContext.Provider value={userInfo}>{children}</UserContext.Provider>
  );
};

export const useUser = () => {
  return useContext(UserContext);
};
