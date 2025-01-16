import React from 'react';
import type { Event, EventType } from '../../types';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import './EventDetails.css';

interface EventDetailsProps {
  event: Event | null;
  onClose: () => void;
}

const EventDetails: React.FC<EventDetailsProps> = ({ event, onClose }) => {
  if (!event) return null;

  // Formata a data gregoriana
  const formattedDate = event.gregorian_date 
    ? format(new Date(event.gregorian_date + 'T12:00:00Z'), "dd 'de' MMMM 'de' yyyy", { locale: ptBR })
    : '';

  const getEventIcon = (event: Event): string => {
    // Verifica se existe event_type_new e se tem um ícone definido
    if (event.event_type_new && event.event_type_new.icon) {
      return event.event_type_new.icon;
    }
    
    // Fallback para ícones padrão baseado no event_type
    const iconMap = {
      equinox: '🌅',
      festival: '🎉',
      historical: '📜',
      sabbath: '🕎',
      new_month: '🌒',
      solstice: '🌞',
      tekufah: '🌍'
    } as const;

    return event.event_type ? iconMap[event.event_type] : '📅';
  };

  return (
    <div className="event-details-overlay" onClick={onClose}>
      <div className="event-details-modal" onClick={e => e.stopPropagation()}>
        <div className="event-details-header">
          <span className="text-3xl">{getEventIcon(event)}</span>
          <h2>{event.title}</h2>
          {formattedDate && (
            <p className="event-date">
              {formattedDate}
              {event.sunset_start && ' (começa no pôr do sol)'}
            </p>
          )}
        </div>

        <div className="event-details-content">
          {event.solar_date && (
            <div className="event-details-section">
              <h3>Data do Ciclo Solar</h3>
              <p>
                {event.solar_date.is_extra_day 
                  ? `Dia de Acréscimo +${event.solar_date.extra_day_number}`
                  : event.solar_date.solar_day && event.solar_date.solar_month
                    ? `Dia ${event.solar_date.solar_day} do ${event.solar_date.solar_month}`
                    : 'Data solar não disponível'
                }
              </p>
            </div>
          )}

          {event.description && (
            <div className="event-details-section">
              <h3>Sobre este evento</h3>
              <p>{event.description}</p>
            </div>
          )}

          {event.biblical_references && event.biblical_references.length > 0 && (
            <div className="event-details-section">
              <h3>Referências Bíblicas</h3>
              <div className="biblical-references">
                {event.biblical_references.map((ref) => (
                  <div key={ref.id} className="biblical-reference">
                    <p className="reference-location">
                      {ref.book} {ref.chapter}:{ref.verse}
                    </p>
                    <p className="reference-text">{ref.text}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <button className="event-details-close" onClick={onClose}>
          Fechar
        </button>
      </div>
    </div>
  );
};

export { EventDetails };
