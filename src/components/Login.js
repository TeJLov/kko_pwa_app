import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ onLogin, onClose }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      
      console.log('Attempting login with:', {
        username: username,
        password: password
      });

      for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
      }

      const response = await axios.post('/api/token', formData);
      console.log('Login response:', response.data);
      
      localStorage.setItem('token', response.data.access_token);
      onLogin();
    } catch (err) {
      console.error('Login error:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status
      });
      setError('Неверное имя пользователя или пароль');
    }
  };

  return (
    <div className="login-container">
      <button className="close-btn" onClick={onClose}>&times;</button>
      <form onSubmit={handleSubmit}>
        <h2>Вход в систему</h2>
        {error && <div className="error">{error}</div>}
        <div>
          <input
            type="text"
            placeholder="Имя пользователя"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Войти</button>
      </form>
    </div>
  );
};

export default Login; 