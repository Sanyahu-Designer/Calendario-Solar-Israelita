import React from 'react';
import './Navbar.css';

export const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <img src="/sun.svg" alt="Logo" className="navbar-logo" />
        <span className="navbar-title">Calendário Solar Israelita</span>
      </div>
    </nav>
  );
};

export default Navbar;
