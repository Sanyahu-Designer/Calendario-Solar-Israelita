import React from 'react';
import './LocationGuide.css';

interface LocationGuideProps {
  error: string | null;
  onRetry: () => void;
}

export const LocationGuide: React.FC<LocationGuideProps> = ({ error, onRetry }) => {
  return (
    <div className="location-guide">
      <div className="location-guide-content">
        <h2>Permissão de Localização Necessária</h2>
        
        <p>
          Para calcular com precisão os horários solares na sua região, 
          precisamos saber sua localização atual.
        </p>

        {error ? (
          <>
            <div className="error-message">
              <p>{error}</p>
              <button onClick={onRetry}>Tentar Novamente</button>
            </div>
            
            <div className="help-section">
              <h3>Como permitir a localização:</h3>
              <ol>
                <li>Procure o ícone 🔒 ou 🌍 na barra de endereço do seu navegador</li>
                <li>Clique nele para abrir as configurações do site</li>
                <li>Selecione "Permitir" para a localização</li>
                <li>Recarregue a página</li>
              </ol>
            </div>
          </>
        ) : (
          <div className="loading-message">
            <p>Aguardando sua permissão...</p>
            <div className="loading-spinner"></div>
          </div>
        )}
      </div>
    </div>
  );
};
