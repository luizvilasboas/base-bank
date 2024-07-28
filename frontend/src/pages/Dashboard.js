import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import UserInfo from "../components/UserInfo";
import TransferForm from "../components/TransferForm";
import { useMessage } from "../context/MessageContext";
import Alert from "../components/Alert";
import axios from "axios";

const Dashboard = () => {
  const { message, setMessage } = useMessage();
  const [userInfo, setUserInfo] = useState({
    username: "",
    email: "",
    balance: 0,
  });

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const response = await axios.get("http://localhost:8000/me", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setUserInfo(response.data);
      } catch (error) {
        setMessage("error", "Erro ao buscar informações do usuário.");
      }
    };

    fetchUserInfo();
  }, [setMessage]);

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <div className="container mx-auto p-4">
        {message.text && <Alert type={message.type} text={message.text} />}
        <div className="flex flex-col md:flex-row md:space-x-4">
          <div className="md:w-1/3">
            <UserInfo user={userInfo} />
          </div>
          <div className="md:w-2/3">
            <TransferForm />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
