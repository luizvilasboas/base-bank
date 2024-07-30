import React from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { FaSignOutAlt, FaUserCircle } from "react-icons/fa";
import { useUser } from "../context/UserContext";

const Header = () => {
  const { logout } = useAuth();
  const user = useUser();

  const navigate = useNavigate();

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
          onClick={handleLogout}
          className="flex items-center bg-red-600 px-4 py-2 rounded-lg text-white hover:bg-red-700 transition duration-300"
        >
          <FaSignOutAlt className="mr-2" />
          Logout
        </button>
      </div>
    </header>
  );
};

export default Header;
