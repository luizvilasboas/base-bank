import React, { createContext, useContext } from "react";
import axios from "axios";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const login = async (email, password) => {
    try {
      const response = await axios.post("http://localhost:8000/login", {
        email: email,
        password: password,
      });

      if (response.status === 200) {
        const { access_token } = response.data;

        localStorage.setItem("token", access_token);

        axios.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;

        return { status: true, text: "Login feito com sucesso." };
      }
    } catch (error) {
      return {
        status: false,
        text: `Não foi possível fazer o login: ${error.response.data["detail"]}`,
      };
    }
  };

  const logout = async () => {
    try {
      await axios.post("http://localhost:8000/logout", {});

      localStorage.removeItem("token");

      delete axios.defaults.headers.common["Authorization"];
    } catch (error) {
      console.error(`Erro ao fazer logout: ${error}`);
    }
  };

  const register = async (name, email, password) => {
    try {
      const response = await axios.post("http://localhost:8000/register", {
        username: name,
        email: email,
        password: password,
      });

      if (response.status === 200) {
        return { status: true, text: "Conta criada com sucesso." };
      }
    } catch (error) {
      return {
        status: false,
        text: `Erro ao registrar: ${error.response.data["datail"]}`,
      };
    }
  };

  return (
    <AuthContext.Provider value={{ login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
