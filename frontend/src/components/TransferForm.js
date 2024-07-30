import axios from "axios";
import React, { useState } from "react";
import { useMessage } from "../context/MessageContext";
import { FaEnvelope, FaMoneyBillWave } from "react-icons/fa";

const TransferForm = () => {
  const [recipientEmail, setRecipientEmail] = useState("");
  const [amount, setAmount] = useState("");
  const { setMessage } = useMessage();

  const handleTransfer = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://localhost:8000/transfer",
        {
          receiver_email: recipientEmail,
          amount: amount,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      if (response.status === 200) {
        setMessage("success", "Transferência realizada com sucesso.");
      } else {
        setMessage("error", response.data.message);
      }
    } catch (error) {
      setMessage("error", "Erro ao realizar a transferência.");
    }
  };

  return (
    <div className="bg-white p-6">
      <h3 className="text-2xl font-extrabold mb-6 text-gray-900">Transferir Dinheiro</h3>
      <form onSubmit={handleTransfer}>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold">
            <FaEnvelope className="inline-block text-blue-500 mr-2" />
            Email do Destinatário
          </label>
          <input
            type="email"
            className="w-full p-3 border border-gray-300 rounded mt-2 focus:outline-none focus:ring-2 focus:ring-blue-600"
            value={recipientEmail}
            onChange={(e) => setRecipientEmail(e.target.value)}
            placeholder="Digite o email do destinatário"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold">
            <FaMoneyBillWave className="inline-block text-green-500 mr-2" />
            Quantidade
          </label>
          <input
            type="number"
            className="w-full p-3 border border-gray-300 rounded mt-2 focus:outline-none focus:ring-2 focus:ring-green-600"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Digite o valor a ser transferido"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition duration-300"
        >
          Transferir
        </button>
      </form>
    </div>
  );
};

export default TransferForm;
