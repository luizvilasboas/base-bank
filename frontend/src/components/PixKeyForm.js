import React, { useState } from "react";
import axios from "axios";
import { useMessage } from "../context/MessageContext";
import { FaPix } from "react-icons/fa6";

const PixKeyForm = () => {
  const [pixKey, setPixKey] = useState("");
  const { setMessage } = useMessage();

  const handlePixKeyCreation = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://localhost:8000/pix/create",
        { key: pixKey },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      if (response.status === 200) {
        setMessage("success", "Chave PIX criada com sucesso.");
        setPixKey("");
      } else {
        setMessage("error", response.data.message);
      }
    } catch (error) {
      setMessage("error", "Erro ao criar a chave PIX.");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg">
      <h3 className="text-2xl font-extrabold mb-6 text-gray-900">
        Criar Chave PIX
      </h3>
      <form onSubmit={handlePixKeyCreation}>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold">
            <FaPix className="inline-block text-green-600 mr-2" />
            Chave PIX
          </label>
          <input
            type="text"
            className="w-full p-2 border border-gray-300 rounded mt-2"
            placeholder="Sua nova chave PIX"
            value={pixKey}
            onChange={(e) => setPixKey(e.target.value)}
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition duration-300"
        >
          Criar Chave
        </button>
      </form>
    </div>
  );
};

export default PixKeyForm;
