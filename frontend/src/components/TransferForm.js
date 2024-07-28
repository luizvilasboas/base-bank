import axios from "axios";
import React, { useState } from "react";
import { useMessage } from "../context/MessageContext";

const TransferForm = () => {
  const [recipientEmail, setRecipientEmail] = useState("");
  const [amount, setAmount] = useState("");
  const {setMessage} = useMessage();

  const handleTransfer = async (e) => {
    e.preventDefault();
  
    try {
      const response = await axios.post(
        "http://localhost:8000/transfer",
        {
          "receiver_email": recipientEmail,
          "amount": amount,
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
    <div className="bg-white p-4 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold mb-4">Transferir Dinheiro</h3>
      <form onSubmit={handleTransfer}>
        <div className="mb-4">
          <label className="block text-gray-700">Email do Destinatário</label>
          <input
            type="email"
            className="w-full p-2 border border-gray-300 rounded mt-2"
            value={recipientEmail}
            onChange={(e) => setRecipientEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Quantidade</label>
          <input
            type="number"
            className="w-full p-2 border border-gray-300 rounded mt-2"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Transferir
        </button>
      </form>
    </div>
  );
};

export default TransferForm;
