import React from "react";
import Header from "../components/Header";
import UserInfo from "../components/UserInfo";
import TransferForm from "../components/TransferForm";
import { useMessage } from "../context/MessageContext";
import Alert from "../components/Alert";
import PixKeyForm from "../components/PixKeyForm";

const Dashboard = () => {
  const message = useMessage();

  return (
    <div className="min-h-screen bg-gradient-to-r from-green-400 via-blue-500 to-purple-500">
      <Header />
      <div className="container mx-auto p-4">
        {message.text && <Alert type={message.type} text={message.text} />}
        <div className="flex flex-col md:flex-row md:space-x-4">
          <div className="md:w-1/2 gap-5">
            <div className="md:h-fit bg-white px-6 rounded-lg shadow-lg">
              <UserInfo />
            </div>
            <div className="md:h-fit bg-white px-6 rounded-lg shadow-lg">
              <PixKeyForm />
            </div>
          </div>
          <div className="md:w-1/2">
            <div className="md:h-fit bg-white px-6 rounded-lg shadow-lg">
              <TransferForm />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
