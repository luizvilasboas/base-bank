import React from "react";
import { FaUser, FaEnvelope, FaDollarSign } from "react-icons/fa";
import { useUser } from "../context/UserContext";

const UserInfo = () => {
  const user = useUser();
  return (
    <div className="bg-white p-6">
      <h3 className="text-2xl font-extrabold mb-6 text-gray-900">Informações do Usuário</h3>
      <div className="mb-4 flex items-center">
        <FaUser className="text-blue-500 mr-2" />
        <p className="text-lg font-medium text-gray-700">
          <strong className="font-semibold">Nome:</strong> {user.username}
        </p>
      </div>
      <div className="mb-4 flex items-center">
        <FaEnvelope className="text-green-500 mr-2" />
        <p className="text-lg font-medium text-gray-700">
          <strong className="font-semibold">Email:</strong> {user.email}
        </p>
      </div>
      <div className="mb-4 flex items-center">
        <FaDollarSign className="text-purple-500 mr-2" />
        <p className="text-lg font-medium text-gray-700">
          <strong className="font-semibold">Saldo Bancário:</strong> ${user.balance.toFixed(2)}
        </p>
      </div>
    </div>
  );
};

export default UserInfo;
