import React from 'react';
import './Menu.css';

interface MenuProps {
  isOpen: boolean;
  onClose: () => void;
}

const Menu: React.FC<MenuProps> = ({ isOpen, onClose }) => {
  return (
    <>
      {/* Overlay escuro quando o menu está aberto */}
      <div 
        className={`menu-overlay ${isOpen ? 'active' : ''}`} 
        onClick={onClose}
      />
      
      {/* Menu lateral */}
      <div className={`menu-container ${isOpen ? 'open' : ''}`}>
        <button className="close-button" onClick={onClose}>
          <span>×</span>
        </button>
        
        <nav className="menu-content">
          <ul>
            <li>
              <a href="/">Calendário</a>
            </li>
            <li>
              <a href="/sobre">Sobre</a>
            </li>
            <li>
              <a href="/ajuda">Ajuda</a>
            </li>
          </ul>
        </nav>
      </div>
    </>
  );
};

export default Menu;
