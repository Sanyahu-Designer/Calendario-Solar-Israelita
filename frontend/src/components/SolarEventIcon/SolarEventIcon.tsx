import React from 'react';
import './SolarEventIcon.css';
import { EventType } from '../../types';

interface SolarEventIconProps {
  eventType: EventType;
  solarMonth?: string;
}

export const SolarEventIcon: React.FC<SolarEventIconProps> = ({ eventType, solarMonth }) => {
  const getSeasonFromMonth = (month: string = '') => {
    const lowerMonth = month.toLowerCase();
    
    // Primavera/Spring
    if (lowerMonth.includes('primeiro') || 
        lowerMonth.includes('first') || 
        lowerMonth.includes('march') ||
        lowerMonth.includes('décimo segundo') || 
        lowerMonth.includes('decimo segundo') ||
        lowerMonth.includes('december')) {
      return 'spring';
    }
    
    // Verão/Summer
    if (lowerMonth.includes('quarto') || 
        lowerMonth.includes('fourth') || 
        lowerMonth.includes('june')) {
      return 'summer';
    }
    
    // Outono/Autumn
    if (lowerMonth.includes('sétimo') || 
        lowerMonth.includes('setimo') || 
        lowerMonth.includes('seventh') || 
        lowerMonth.includes('september')) {
      return 'autumn';
    }
    
    // Inverno/Winter
    if (lowerMonth.includes('décimo') || 
        lowerMonth.includes('decimo') || 
        lowerMonth.includes('tenth') || 
        lowerMonth.includes('december')) {
      // Se incluir "segundo", é primavera
      if (lowerMonth.includes('segundo') || lowerMonth.includes('second')) {
        return 'spring';
      }
      return 'winter';
    }
    
    return 'spring'; // default
  };

  const getEventIcon = () => {
    switch (eventType) {
      case 'equinox':
        const isSpring = getSeasonFromMonth(solarMonth) === 'spring';
        return (
          <svg className={`solar-event-icon ${isSpring ? 'spring' : 'autumn'}`} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="5" className="sun" />
            <g className="rays">
              {/* Raios principais */}
              <path d="M12 2V6M12 18V22M2 12H6M18 12H22" strokeWidth="2" strokeLinecap="round" />
              {/* Raios diagonais */}
              <path d="M4.93 4.93L7.76 7.76M16.24 16.24L19.07 19.07M4.93 19.07L7.76 16.24M16.24 7.76L19.07 4.93" strokeWidth="2" strokeLinecap="round" />
            </g>
            {isSpring ? (
              // Flores para primavera - pétalas mais definidas
              <g className="spring-detail">
                <path d="M4 12C4 9 7 8 8 8C9 8 12 9 12 12" transform="rotate(0 12 12)" />
                <path d="M4 12C4 9 7 8 8 8C9 8 12 9 12 12" transform="rotate(72 12 12)" />
                <path d="M4 12C4 9 7 8 8 8C9 8 12 9 12 12" transform="rotate(144 12 12)" />
                <path d="M4 12C4 9 7 8 8 8C9 8 12 9 12 12" transform="rotate(216 12 12)" />
                <path d="M4 12C4 9 7 8 8 8C9 8 12 9 12 12" transform="rotate(288 12 12)" />
              </g>
            ) : (
              // Folhas para outono - padrão mais orgânico
              <g className="autumn-detail">
                <path d="M6 6C8 4 10 5 12 6C10 7 8 8 6 6" transform="rotate(0 12 12)" />
                <path d="M6 6C8 4 10 5 12 6C10 7 8 8 6 6" transform="rotate(72 12 12)" />
                <path d="M6 6C8 4 10 5 12 6C10 7 8 8 6 6" transform="rotate(144 12 12)" />
                <path d="M6 6C8 4 10 5 12 6C10 7 8 8 6 6" transform="rotate(216 12 12)" />
                <path d="M6 6C8 4 10 5 12 6C10 7 8 8 6 6" transform="rotate(288 12 12)" />
              </g>
            )}
          </svg>
        );
      
      case 'solstice':
        const isSummer = getSeasonFromMonth(solarMonth) === 'summer';
        return (
          <svg className={`solar-event-icon ${isSummer ? 'summer' : 'winter'}`} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="5" className="sun" />
            {isSummer ? (
              // Raios mais longos e intensos para solstício de verão
              <g className="rays">
                <path d="M12 1V7M12 17V23M1 12H7M17 12H23" strokeWidth="2.5" strokeLinecap="round" />
                <path d="M3.93 3.93L8.76 8.76M15.24 15.24L20.07 20.07M3.93 20.07L8.76 15.24M15.24 8.76L20.07 3.93" strokeWidth="2.5" strokeLinecap="round" />
                {/* Raios extras para verão */}
                <path d="M2 7L6 9M18 15L22 17M22 7L18 9M6 15L2 17" strokeWidth="2" strokeLinecap="round" />
              </g>
            ) : (
              // Raios mais curtos e suaves para solstício de inverno
              <g className="rays">
                <path d="M12 4V8M12 16V20M4 12H8M16 12H20" strokeWidth="1.5" strokeLinecap="round" />
                <path d="M6.93 6.93L9.76 9.76M14.24 14.24L17.07 17.07M6.93 17.07L9.76 14.24M14.24 9.76L17.07 6.93" strokeWidth="1.5" strokeLinecap="round" />
              </g>
            )}
          </svg>
        );
      
      default:
        return <span className="event-icon">›</span>;
    }
  };

  return (
    <div className={`solar-event-icon-wrapper ${eventType}`}>
      {getEventIcon()}
    </div>
  );
};
