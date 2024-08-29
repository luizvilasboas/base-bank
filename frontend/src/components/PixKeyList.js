import React, { useEffect, useState } from "react";
import axios from "axios";
import { useMessage } from "../context/MessageContext";

const PixKeyList = () => {
  const [pixKeys, setPixKeys] = useState([]);
  const { setMessage } = useMessage();

  useEffect(() => {
    const fetchPixKeys = async () => {
      const token = localStorage.getItem("token");

      if (token) {
        try {
          const response = await axios.get("http://localhost/pix/list", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          setPixKeys(response.data);
        } catch (error) {
          setMessage("error", "Erro ao buscar chaves PIX.");
        }
      }
    };

    fetchPixKeys();
  }, [setMessage]);

  return (
    <div className="bg-white p-6 rounded-lg">
      <h3 className="text-2xl font-extrabold mb-6 text-gray-900">Chaves PIX</h3>
      <ul>
        {pixKeys.map((key, index) => (
          <li key={index} className="border-b border-gray-300 py-2">
            {key.key}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PixKeyList;
