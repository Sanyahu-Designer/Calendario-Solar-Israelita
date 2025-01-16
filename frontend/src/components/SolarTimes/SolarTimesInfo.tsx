import React from 'react';
import './SolarTimesInfo.css';
import { SolarTimeDay } from '../../types';

interface SolarTimesInfoProps {
  solarTimes: SolarTimeDay;
}

export const SolarTimesInfo: React.FC<SolarTimesInfoProps> = ({ solarTimes }) => {
  if (!solarTimes || !solarTimes.sunrise) return null;

  const formatTime = (time: string) => {
    if (!time) return '--:--';
    try {
      const [hours, minutes] = time.split(':');
      return `${hours}:${minutes}`;
    } catch {
      return '--:--';
    }
  };

  const getSeasonEmoji = (seasonType: string | null) => {
    switch (seasonType) {
      case 'spring_equinox':
        return '🌸';
      case 'summer_solstice':
        return '☀️';
      case 'autumn_equinox':
        return '🍂';
      case 'winter_solstice':
        return '❄️';
      default:
        return '';
    }
  };

  const getSeasonName = (seasonType: string | null) => {
    switch (seasonType) {
      case 'spring_equinox':
        return 'Equinócio de Primavera';
      case 'summer_solstice':
        return 'Solstício de Verão';
      case 'autumn_equinox':
        return 'Equinócio de Outono';
      case 'winter_solstice':
        return 'Solstício de Inverno';
      default:
        return '';
    }
  };

  return (
    <div className="solar-times-info">
      <div className="solar-time-item sunrise">
        <span className="time-label">Nascer do Sol:</span>
        <span className="time-value">{formatTime(solarTimes.sunrise)}</span>
      </div>
      
      {solarTimes.solar_noon && (
        <div className="solar-time-item solar-noon">
          <span className="time-label">Meio-dia Solar:</span>
          <span className="time-value">{formatTime(solarTimes.solar_noon)}</span>
        </div>
      )}
      
      {solarTimes.sunset && (
        <div className="solar-time-item sunset">
          <span className="time-label">Pôr do Sol:</span>
          <span className="time-value">{formatTime(solarTimes.sunset)}</span>
        </div>
      )}

      {solarTimes.season_type && (
        <div className="solar-time-item season-info">
          <span className="time-label">{getSeasonEmoji(solarTimes.season_type)}</span>
          <span className="time-value">{getSeasonName(solarTimes.season_type)}</span>
        </div>
      )}
    </div>
  );
};
