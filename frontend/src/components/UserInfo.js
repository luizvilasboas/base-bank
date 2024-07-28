import React from "react";

const UserInfo = ({ user }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold mb-4">Informações do Usuário</h3>
      <p>
        <strong>Nome:</strong> {user.username}
      </p>
      <p>
        <strong>Email:</strong> {user.email}
      </p>
      <p>
        <strong>Saldo Bancário:</strong> ${user.balance.toFixed(2)}
      </p>
    </div>
  );
};

export default UserInfo;
