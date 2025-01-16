import React, { useEffect } from 'react';
import { Event, SolarTimeDay } from '../../types';
import './EventModal.css';

interface EventModalProps {
  event: Event | null;
  isOpen: boolean;
  onClose: () => void;
  solarTimes?: SolarTimeDay;
}

export const EventModal: React.FC<EventModalProps> = ({ event, isOpen, onClose, solarTimes }) => {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen || !event) return null;

  console.log('Event data:', event); // Temporário para debug

  return (
    <div 
      className="event-modal-overlay" 
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div 
        className="event-modal-content" 
        onClick={e => e.stopPropagation()}
        role="document"
      >
        <h2 id="modal-title">{event.title}</h2>
        <div className="event-details">
          {event.description && (
            <p className="description">{event.description}</p>
          )}
          
          <div className="event-info">
            {event.event_type_new && (
              <p>
                <strong>Tipo:</strong> {event.event_type_new.name}
                {event.event_type_new.icon && (
                  <span className="event-type-icon">{event.event_type_new.icon}</span>
                )}
              </p>
            )}
            
            {event.solar_date && (
              <p>
                <strong>Data Solar:</strong> {
                  event.solar_date.is_extra_day 
                    ? `Dia +${event.solar_date.extra_day_number}`
                    : `Dia ${event.solar_date.solar_day} do ${event.solar_date.solar_month}`
                }
              </p>
            )}
            
            {event.is_holy_day && (
              <p className="holy-day-info">
                <i className="fas fa-star"></i> Dia Santo
              </p>
            )}
            
            {typeof event.sunset_start !== 'undefined' && (
              <p className="sunset-info">
                <i className="fas fa-sun"></i>
                {event.sunset_start ? 'Começa no pôr do sol' : 'Começa no amanhecer'}
              </p>
            )}
          </div>

          {event.biblical_references && event.biblical_references.length > 0 && (
            <div className="biblical-references">
              <h3>Referências Bíblicas 📖<i className="fas fa-book"></i></h3>
              {event.biblical_references.map((ref, index) => (
                <p key={ref.id} className="biblical-reference">
                  <strong>{ref.book} {ref.chapter}:{ref.verse}</strong> - {ref.text}
                </p>
              ))}
            </div>
          )}
          
          {event.event_type === 'equinox' || event.event_type === 'solstice' ? (
            <div className="solar-event-info">
              <p>
                <strong>Tipo:</strong> {event.event_type === 'equinox' ? 'Equinócio' : 'Solstício'}
              </p>
              {solarTimes?.season_type && (
                <p>
                  <strong>Estação:</strong> {solarTimes.season_type}
                </p>
              )}
              {solarTimes?.season_time && (
                <p>
                  <strong>Horário:</strong> {solarTimes.season_time}
                </p>
              )}
            </div>
          ) : null}
        </div>
        <button 
          className="close-button"
          onClick={onClose}
          aria-label="Fechar modal"
        >
          Fechar
        </button>
      </div>
    </div>
  );
};
