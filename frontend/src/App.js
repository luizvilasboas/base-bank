import React, { useState } from 'react';
import { useAuth } from './context/AuthContext';
import Login from './components/Login';
import Register from './components/Register';

function App() {
  const [isRegister, setIsRegister] = useState(false);
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <div className="flex items-center justify-center min-h-screen bg-gray-100">Você está logado!</div>;
  }

  return (
    <div>
      {isRegister ? <Register onLogin={() => setIsRegister(false)} /> : <Login onRegister={() => setIsRegister(true)} />}
      <div className="text-center mt-4">
        {isRegister ? (
          <p>
            Já tem uma conta?{' '}
            <button className="text-blue-500 hover:underline" onClick={() => setIsRegister(false)}>
              Login
            </button>
          </p>
        ) : (
          <p>
            Não tem uma conta?{' '}
            <button className="text-blue-500 hover:underline" onClick={() => setIsRegister(true)}>
              Registrar
            </button>
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
