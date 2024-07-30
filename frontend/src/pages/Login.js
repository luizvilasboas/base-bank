import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useMessage } from "../context/MessageContext";
import { useNavigate } from "react-router-dom";
import Alert from "../components/Alert";

const Login = () => {
  const { login } = useAuth();
  const { message, setMessage } = useMessage();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const result = await login(email, password);

    if (result.status) {
      setMessage("success", result.text);
      navigate("/dashboard");
    } else {
      setMessage("error", result.text); 
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-purple-400 via-pink-500 to-red-500">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h2 className="text-3xl font-extrabold mb-6 text-center text-gray-900">Login</h2>
        {message.text && <Alert type={message.type} text={message.text} />}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 font-semibold">Email</label>
            <input
              type="email"
              className="w-full p-2 border border-gray-300 rounded mt-2 focus:outline-none focus:ring-2 focus:ring-purple-600"
              placeholder="Seu email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 font-semibold">Senha</label>
            <input
              type="password"
              className="w-full p-2 border border-gray-300 rounded mt-2 focus:outline-none focus:ring-2 focus:ring-purple-600"
              placeholder="Sua senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button className="w-full bg-purple-600 text-white p-2 rounded-lg hover:bg-purple-700 transition duration-300">
            Entrar
          </button>
        </form>
        <div className="text-center mt-4">
          <p className="text-gray-700">
            Não tem uma conta?{" "}
            <button
              className="text-purple-600 hover:underline"
              onClick={() => navigate("/register")}
            >
              Registrar
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
