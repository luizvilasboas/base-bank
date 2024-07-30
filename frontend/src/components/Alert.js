import React from "react";
import { useMessage } from "../context/MessageContext";
import { FaTimes } from "react-icons/fa";

const Alert = ({ type, text }) => {
  const { clearMessage } = useMessage();
  const bgColor = type === "error" ? "bg-red-500" : "bg-green-500";
  const borderColor = type === "error" ? "border-red-400" : "border-green-400";
  const bgLightColor = type === "error" ? "bg-red-100" : "bg-green-100";
  const textColor = type === "error" ? "text-red-700" : "text-green-700";
  const title = type === "error" ? "Erro" : "Sucesso";

  return (
    <div role="alert" className="mb-4">
      <div
        className={`flex justify-between ${bgColor} text-white font-bold rounded-t px-4 py-2`}
      >
        {title}
        <button onClick={clearMessage} className="text-white font-bold">
          <FaTimes className="text-xl" />
        </button>
      </div>
      <div
        className={`border border-t-0 ${borderColor} rounded-b ${bgLightColor} px-4 py-3 ${textColor}`}
      >
        <p>{text}</p>
      </div>
    </div>
  );
};

export default Alert;
