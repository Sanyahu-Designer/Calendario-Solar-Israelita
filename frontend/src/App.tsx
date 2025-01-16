import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import SolarCalendarPage from './pages/SolarCalendar';
import AboutPage from './pages/About';
import './App.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<SolarCalendarPage />} />
            <Route path="/solar" element={<SolarCalendarPage />} />
            <Route path="/sobre" element={<AboutPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
