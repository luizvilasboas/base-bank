import React from "react";
import Header from "../components/Header";
import UserInfo from "../components/UserInfo";
import TransferForm from "../components/TransferForm";
import { useMessage } from "../context/MessageContext";
import Alert from "../components/Alert";
import PixKeyForm from "../components/PixKeyForm";
import PixKeyList from "../components/PixKeyList";

const Dashboard = () => {
  const { message } = useMessage();

  return (
    <div className="min-h-screen bg-gradient-to-r from-green-400 via-blue-500 to-purple-500">
      <Header />
      <div className="container mx-auto p-4">
        {message.text && <Alert type={message.type} text={message.text} />}
        <div className="flex flex-col items-center">
          <div className="flex flex-col md:flex-row w-full md:w-2/3">
            <div className="w-full md:w-1/2 p-4">
              <div className="bg-white p-6 rounded-lg shadow-lg h-full">
                <UserInfo />
              </div>
            </div>
            <div className="w-full md:w-1/2 p-4">
              <div className="bg-white p-6 rounded-lg shadow-lg h-full">
                <PixKeyForm />
              </div>
            </div>
          </div>
          <div className="flex flex-col md:flex-row w-full md:w-2/3">
            <div className="w-full md:w-1/2 p-4">
              <div className="bg-white p-6 rounded-lg shadow-lg h-full">
                <TransferForm />
              </div>
            </div>
            <div className="w-full md:w-1/2 p-4">
              <div className="bg-white p-6 rounded-lg shadow-lg h-full">
                <PixKeyList />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
