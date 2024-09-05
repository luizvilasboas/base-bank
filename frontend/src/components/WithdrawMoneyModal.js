import React, { useState } from "react";
import axios from "axios";
import { useMessage } from "../context/MessageContext";

const WithdrawMoneyModal = ({ onClose }) => {
  const [amount, setAmount] = useState("");
  const { setMessage } = useMessage();

  const handleWithdrawMoney = async () => {
    const token = localStorage.getItem("token");

    try {
      const response = await axios.post(
        "http://localhost/transaction/withdraw",
        { amount: amount },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 200) {
        setMessage("success", "Dinheiro adicionado com sucesso!");
        onClose();
      }
    } catch (error) {
      setMessage(
        "error",
        error.response?.data?.detail || "Erro ao adicionar dinheiro."
      );
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Retirar Valor</h2>
        <input
          type="number"
          className="border p-2 w-full mb-4"
          placeholder="Digite o valor"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <div className="flex justify-end space-x-4">
          <button
            className="bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700"
            onClick={handleWithdrawMoney}
          >
            Retirar
          </button>
          <button
            className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            onClick={onClose}
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};

export default WithdrawMoneyModal;
