import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { FaSignOutAlt, FaUserCircle, FaPlusCircle, FaMinusCircle } from "react-icons/fa";
import { useUser } from "../context/UserContext";
import AddMoneyModal from "./AddMoneyModal"; // Modal component for adding money
import WithdrawMoneyModal from "./WithdrawMoneyModal"; // Modal component for withdrawing money

const Header = () => {
  const { logout } = useAuth();
  const user = useUser();
  const navigate = useNavigate();

  const [isAddMoneyModalOpen, setIsAddMoneyModalOpen] = useState(false);
  const [isWithdrawMoneyModalOpen, setIsWithdrawMoneyModalOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <header className="flex justify-between items-center bg-white p-4 text-black shadow-lg">
      <div className="text-3xl font-extrabold tracking-wide">base-bank</div>
      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-2">
          <FaUserCircle className="text-xl" />
          <span className="text-lg font-medium">{user?.email}</span>
        </div>
        <button
          onClick={() => setIsAddMoneyModalOpen(true)}
          className="flex items-center bg-green-600 px-4 py-2 rounded-lg text-white hover:bg-green-700 transition duration-300"
        >
          <FaPlusCircle className="mr-2" />
          Adicionar Valor
        </button>
        <button
          onClick={() => setIsWithdrawMoneyModalOpen(true)}
          className="flex items-center bg-yellow-600 px-4 py-2 rounded-lg text-white hover:bg-yellow-700 transition duration-300"
        >
          <FaMinusCircle className="mr-2" />
          Retirar Valor
        </button>
        <button
          onClick={handleLogout}
          className="flex items-center bg-red-600 px-4 py-2 rounded-lg text-white hover:bg-red-700 transition duration-300"
        >
          <FaSignOutAlt className="mr-2" />
          Logout
        </button>
      </div>

      {/* Modais para adicionar e retirar dinheiro */}
      {isAddMoneyModalOpen && (
        <AddMoneyModal onClose={() => setIsAddMoneyModalOpen(false)} />
      )}
      {isWithdrawMoneyModalOpen && (
        <WithdrawMoneyModal onClose={() => setIsWithdrawMoneyModalOpen(false)} />
      )}
    </header>
  );
};

export default Header;
