import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        {/* Coluna 1 - Sobre */}
        <div className="footer-column">
          <div className="footer-logo">
            <span className="footer-icon">☀️</span>
            <h3>Calendário Solar Israelita</h3>
          </div>
          <p className="footer-description">
            Um calendário baseado no ciclo solar e nas Escrituras Sagradas,
            marcando as comemorações e eventos históricos do povo de Israel.
          </p>
        </div>

        {/* Coluna 2 - Links Rápidos */}
        <div className="footer-column">
          <h3 className="footer-title">
            <span className="title-icon">🔗</span>
            Links Rápidos
          </h3>
          <div className="footer-links">
            <Link to="/sobre" className="footer-link" target="_blank" rel="noopener noreferrer">
              <span className="link-icon">ℹ️</span>
              Sobre
            </Link>
            <a 
              href="https://sanyahudesigner.com.br" 
              target="_blank"
              rel="noopener noreferrer"
              className="footer-link"
            >
              <span className="link-icon">❓</span>
              Ajuda
            </a>
          </div>
        </div>

        {/* Coluna 3 - Contato */}
        <div className="footer-column">
          <h3 className="footer-title">
            <span className="title-icon">💬</span>
            Contato
          </h3>
          <p className="footer-description">
            Tem alguma dúvida ou sugestão? Entre em contato conosco!
          </p>
          <a 
            href="https://api.whatsapp.com/send?phone=5551996164731" 
            className="contact-button"
            target="_blank"
            rel="noopener noreferrer"
          >
            <span className="contact-icon">✉️</span>
            <span>Entre em contato</span>
          </a>
        </div>
      </div>
      
      {/* Rodapé de direitos autorais */}
      <div className="footer-bottom">
        <p>{new Date().getFullYear()} Calendário Solar Israelita. Todos os direitos reservados.</p>
        <p>
          Desenvolvido por{' '}
          <a 
            href="https://sanyahudesigner.com.br" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="developer-link"
          >
            Sanyahu Designer
          </a>
        </p>
      </div>
    </footer>
  );
};

export default Footer;
