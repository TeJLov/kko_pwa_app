import React, { useState, useEffect, useCallback } from 'react';
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
  const [deferredPrompt, setDeferredPrompt] = useState(null);

  const checkAuth = useCallback(async () => {
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
  }, []);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      checkAuth();
    }
  }, [checkAuth]);

  useEffect(() => {
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      console.log('beforeinstallprompt event fired');
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

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

  const handleInstallClick = () => {
    if (deferredPrompt) {
      console.log('Prompting for installation');
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
          console.log('User accepted the A2HS prompt');
        } else {
          console.log('User dismissed the A2HS prompt');
        }
        setDeferredPrompt(null);
      });
    } else {
      console.log('deferredPrompt is null');
    }
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
            <div className="user-info">
              <h2>Добро пожаловать, {user.username}!</h2>
            </div>
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

        {/* Кнопка для установки на главный экран */}
        {deferredPrompt && (
          <button onClick={handleInstallClick}>
            Установить на главный экран
          </button>
        )}
      </div>
    </Router>
  );
}
export default App;
