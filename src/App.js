import logo from './logo.svg';
import './App.css';
import React from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1 className="title">
          <span className="title-word">Визитка</span>
          <span className="title-word">Крутого</span>
          <span className="title-word">Креативного</span>
          <span className="title-word">Отдела</span>
        </h1>
      </header>
    </div>
  );
}
/*
const App = () => {
  const videos = ['video1.mp4', 'video2.mp4'];
  return (
    <div>
      <h1>Сайт-визитка</h1>
      {videos.map((video, index) => (
        <video key={index} src={video} controls />
      ))}
    </div>
  );
};
*/
export default App;
