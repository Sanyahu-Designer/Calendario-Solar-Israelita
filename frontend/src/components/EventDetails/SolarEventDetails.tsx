import React from 'react';
import type { Event, BiblicalReference, SolarDate } from '../../types';
import { format, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import './SolarEventDetails.css';

interface EventDetailsProps {
  event: Event | null;
  onClose: () => void;
}

const SolarEventDetails: React.FC<EventDetailsProps> = ({ event, onClose }) => {
  if (!event) return null;

  const formattedDate = event.gregorian_date 
    ? format(parseISO(event.gregorian_date), "dd 'de' MMMM 'de' yyyy", { locale: ptBR })
    : '';

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const formatBiblicalReference = (ref: BiblicalReference) => {
    return `${ref.book} ${ref.chapter}:${ref.verse} - ${ref.text}`;
  };

  return (
    <div className="event-details-overlay" onClick={handleOverlayClick}>
      <div className="event-details-modal">
        <div className="event-details-header">
          <span className="event-details-icon">{event.event_type_new?.icon || '›'}</span>
          <div>
            <h2 className="event-details-title">{event.title}</h2>
            {formattedDate && (
              <p className="event-details-info">
                {formattedDate}
                {event.sunset_start && ' (começa no pôr do sol)'}
              </p>
            )}
            {event.solar_date && (
              <p className="event-details-info solar-date-info">
                <span className="solar-icon">🌞</span>
                Dia {event.solar_date.solar_day} do {event.solar_date.solar_month.toLowerCase()}
              </p>
            )}
          </div>
        </div>

        {event.description && (
          <div className="event-details-info">
            {event.description}
          </div>
        )}

        {event.biblical_references && event.biblical_references.length > 0 && (
          <div className="event-details-info biblical-references">
            <h3 className="references-title">Referências Bíblicas:</h3>
            <ul className="references-list">
              {event.biblical_references.map((reference) => (
                <li key={reference.id} className="reference-item">
                  {formatBiblicalReference(reference)}
                </li>
              ))}
            </ul>
          </div>
        )}

        <button className="event-details-close" onClick={onClose}>
          Fechar
        </button>
      </div>
    </div>
  );
};

export default SolarEventDetails;
