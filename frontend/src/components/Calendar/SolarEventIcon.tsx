import React from 'react';

interface SolarEventIconProps {
  eventType: string;
  solarMonth: string;
}

export const SolarEventIcon: React.FC<SolarEventIconProps> = ({ eventType, solarMonth }) => {
  const getIcon = () => {
    if (eventType === 'equinox') {
      return '⚖️';
    } else if (eventType === 'solstice') {
      return '☀️';
    }
    return '•';
  };

  const getTitle = () => {
    if (eventType === 'equinox') {
      return 'Equinócio';
    } else if (eventType === 'solstice') {
      return 'Solstício';
    }
    return '';
  };

  return (
    <span className="event-icon" title={getTitle()}>
      {getIcon()}
    </span>
  );
};
