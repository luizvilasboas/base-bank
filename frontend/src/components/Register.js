import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

function Register({ onLogin }) {
  const { register } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    register(name, email, password);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h2 className="text-2xl font-bold mb-6 text-center">Registrar</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700">Nome</label>
            <input 
              type="text" 
              className="w-full p-2 border border-gray-300 rounded mt-2" 
              placeholder="Seu nome" 
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Email</label>
            <input 
              type="email" 
              className="w-full p-2 border border-gray-300 rounded mt-2" 
              placeholder="Seu email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700">Senha</label>
            <input 
              type="password" 
              className="w-full p-2 border border-gray-300 rounded mt-2" 
              placeholder="Sua senha" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Registrar</button>
        </form>
        <div className="text-center mt-4">
          <p>
            Já tem uma conta?{' '}
            <button className="text-blue-500 hover:underline" onClick={onLogin}>
              Login
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Register;
