import React, { useState, useEffect } from 'react';
import './App.css';
import Login from './components/Login';
import axios from 'axios';
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import Dashboard from "./components/Dashboard";

function App() {
  // Состояние для отслеживания аутентификации пользователя
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // Состояние для хранения данных пользователя
  const [user, setUser] = useState(null);
  // Состояние для управления отображением компонента входа
  const [showLogin, setShowLogin] = useState(false);

  // Проверка токена при загрузке приложения
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      checkAuth();
    }
  }, [checkAuth]);

  /*
   * Проверяет валидность токена и получает данные пользователя
   * В случае ошибки удаляет невалидный токен
   */
  const checkAuth = async () => {
    try {
      const response = await axios.get('/api/users/me', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      localStorage.removeItem('token');
      setIsAuthenticated(false);
    }
  };

  /**
   * Обработчик успешного входа
   * Запускает проверку аутентификации
   */
  const handleLogin = () => {
    checkAuth();
  };

  /**
   * Обработчик выхода из системы
   * Удаляет токен и очищает данные пользователя
   */
  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <Router>
      <div className="App">
        <div className="App-header">
          <h1 className="title">
            <span className="title-word">Визитка</span>
            <span className="title-word">Крутого</span>
            <span className="title-word">Креативного</span>
            <span className="title-word">Отдела</span>
          </h1>
        </div>

        {isAuthenticated ? (
          <div className="admin-panel">
            <h2>Панель администратора</h2>
            <div className="stats">
              <h3>Навигация</h3>
              <ul>
                <li>
                  <Link to="/dashboard">Открыть дашборд</Link>
                </li>
              </ul>
            </div>
            <button className="logout-btn" onClick={handleLogout}>Выйти</button>
          </div>
        ) : (
          <button className="login-trigger" onClick={() => setShowLogin(!showLogin)}>
            Войти
          </button>
        )}

        {showLogin && !isAuthenticated && (
          <div className="login-overlay">
            <Login onLogin={handleLogin} onClose={() => setShowLogin(false)} />
          </div>
        )}

        <Routes>
          {/* Отдельный маршрут для дашборда */}
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}
export default App;
