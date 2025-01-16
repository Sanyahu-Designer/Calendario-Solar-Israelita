import React from 'react';
import './DayLengthGraph.css';

interface DayLengthGraphProps {
  sunrise: string;
  sunset: string;
}

export const DayLengthGraph: React.FC<DayLengthGraphProps> = ({ sunrise, sunset }) => {
  const calculateDayLength = () => {
    // Converte os horários para minutos desde meia-noite
    const getMinutes = (time: string) => {
      const [hours, minutes] = time.split('h').map(Number);
      return (hours * 60) + (minutes || 0);
    };

    const sunriseMinutes = getMinutes(sunrise);
    const sunsetMinutes = getMinutes(sunset);
    
    // Calcula a diferença em minutos
    const dayLengthMinutes = sunsetMinutes - sunriseMinutes;
    
    const hours = Math.floor(dayLengthMinutes / 60);
    const minutes = dayLengthMinutes % 60;
    
    return {
      hours,
      minutes,
      percentage: (dayLengthMinutes / (24 * 60)) * 100
    };
  };

  const dayLength = calculateDayLength();
  const minutesText = dayLength.minutes > 0 ? `${dayLength.minutes.toString().padStart(2, '0')}` : '';

  return (
    <div className="day-length-graph">
      <div className="graph-container">
        <div 
          className="day-progress" 
          style={{ width: `${dayLength.percentage}%` }}
          title={`O dia tem ${dayLength.hours}h${minutesText} de luz solar`}
        />
      </div>
      <span className="day-length-text">
        O dia tem {dayLength.hours}h{minutesText} de luz solar
      </span>
    </div>
  );
};
