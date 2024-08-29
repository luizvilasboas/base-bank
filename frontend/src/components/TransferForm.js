import axios from "axios";
import React, { useState, useEffect } from "react";
import { useMessage } from "../context/MessageContext";
import { FaKey, FaMoneyBillWave } from "react-icons/fa";

const TransferForm = () => {
  const [userPixKeys, setUserPixKeys] = useState([]);
  const [selectedUserPixKey, setSelectedUserPixKey] = useState("");
  const [recipientPixKey, setRecipientPixKey] = useState("");
  const [amount, setAmount] = useState("");
  const { setMessage } = useMessage();

  useEffect(() => {
    const fetchUserPixKeys = async () => {
      try {
        const response = await axios.get("http://localhost:8000/pix/list", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setUserPixKeys(response.data);
      } catch (error) {
        setMessage("error", "Erro ao carregar suas chaves PIX.");
      }
    };

    fetchUserPixKeys();
  }, [setMessage]);

  const handleTransfer = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://localhost:8000/transaction/create ",
        {
          sender_pix_key: selectedUserPixKey,
          receiver_pix_key: recipientPixKey,
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
        setSelectedUserPixKey("");
        setRecipientPixKey("");
        setAmount("");
      } else {
        setMessage("error", response.data.message);
      }
    } catch (error) {
      setMessage("error", "Erro ao realizar a transferência.");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-2xl font-extrabold mb-6 text-gray-900">Transferir Dinheiro</h3>
      <form onSubmit={handleTransfer}>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold">
            <FaKey className="inline-block text-blue-500 mr-2" />
            Selecionar sua chave PIX
          </label>
          <select
            className="w-full p-3 border border-gray-300 rounded mt-2 focus:outline-none focus:ring-2 focus:ring-blue-600"
            value={selectedUserPixKey}
            onChange={(e) => setSelectedUserPixKey(e.target.value)}
            required
          >
            <option value="" disabled>Selecione uma chave PIX</option>
            {userPixKeys.map((key) => (
              <option key={key.id} value={key.key}>{key.key}</option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold">
            <FaKey className="inline-block text-blue-500 mr-2" />
            Chave PIX do Destinatário
          </label>
          <input
            type="text"
            className="w-full p-3 border border-gray-300 rounded mt-2 focus:outline-none focus:ring-2 focus:ring-blue-600"
            value={recipientPixKey}
            onChange={(e) => setRecipientPixKey(e.target.value)}
            placeholder="Digite a chave PIX do destinatário"
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
