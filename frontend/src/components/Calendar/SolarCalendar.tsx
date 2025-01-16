import React from 'react';
import { format, isToday, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import './SolarCalendar.css';
import { Event, CalendarMonth, CalendarDay } from '../../types';
import { LocationGuide } from '../LocationGuide/LocationGuide';
import { useGeolocation } from '../../hooks/useGeolocation';
import { DayLengthGraph } from '../DayLengthGraph/DayLengthGraph';
import { SolarEventIcon } from '../SolarEventIcon/SolarEventIcon';

interface SolarCalendarProps {
  calendarData: CalendarMonth | null;
  currentDate: Date;
  onEventSelect: (event: Event) => void;
  handlePreviousMonth: () => void;
  handleNextMonth: () => void;
  error?: string;
}

const SolarCalendar: React.FC<SolarCalendarProps> = ({ 
  calendarData, 
  currentDate, 
  onEventSelect, 
  handlePreviousMonth, 
  handleNextMonth,
  error 
}) => {
  const { latitude, longitude, error: locationError, loading: locationLoading, requestGeolocation } = useGeolocation();
  const [slideDirection, setSlideDirection] = React.useState<'left' | 'right' | null>(null);
  const [isTransitioning, setIsTransitioning] = React.useState(false);

  const handlePrevious = () => {
    if (isTransitioning) return;
    setIsTransitioning(true);
    setSlideDirection('right');
    handlePreviousMonth();
    setTimeout(() => {
      setSlideDirection(null);
      setIsTransitioning(false);
    }, 600);
  };

  const handleNext = () => {
    if (isTransitioning) return;
    setIsTransitioning(true);
    setSlideDirection('left');
    handleNextMonth();
    setTimeout(() => {
      setSlideDirection(null);
      setIsTransitioning(false);
    }, 600);
  };

  if (error) {
    return (
      <div className="solar-calendar">
        <div className="error-state">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  // Mostrar o guia de localização se houver erro ou estiver carregando
  if (locationError || locationLoading) {
    return (
      <div className="solar-calendar">
        <LocationGuide 
          error={locationError} 
          onRetry={requestGeolocation}
        />
      </div>
    );
  }

  if (!calendarData) {
    return (
      <div className="solar-calendar">
        <div className="loading-state">
          <p>Carregando...</p>
        </div>
      </div>
    );
  }

  const hasSolarEvent = (events: Event[]) => {
    return events.some(event => 
      ['equinox', 'solstice'].includes(event.event_type)
    );
  };

  const formatDate = (dateString: string) => {
    const date = parseISO(dateString);
    return {
      day: format(date, 'dd'),
      weekDay: format(date, 'EEEE', { locale: ptBR }).replace(/^./, 
        (letra) => letra.toUpperCase()
      ),
      isToday: isToday(date)
    };
  };

  return (
    <div className="solar-calendar">
      <div className="calendar-header">
        <button 
          onClick={handlePrevious} 
          className="nav-button" 
          aria-label="Mês anterior"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18L9 12L15 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
        <h2 className="current-month">{format(currentDate, 'MMMM yyyy', { locale: ptBR })}</h2>
        <button 
          onClick={handleNext} 
          className="nav-button"
          aria-label="Próximo mês"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>

      <div className={`calendar-list ${slideDirection ? `slide-${slideDirection}` : ''}`}>
        {calendarData.days.map((day: CalendarDay) => {
          const dateInfo = formatDate(day.gregorian_date);
          return (
            <div 
              key={day.gregorian_date}
              className={`calendar-day-item ${dateInfo.isToday ? 'today' : ''} ${
                hasSolarEvent(day.events) ? 'has-solar-event' : ''
              }`}
            >
              <div className="day-info">
                <div className="day-number">{dateInfo.day}</div>
                <div className="date-details">
                  <div className="weekday-container">
                    <span className="weekday">{dateInfo.weekDay}</span>
                    {dateInfo.isToday && <span className="today-tag">Hoje</span>}
                    {day.solar_date && (
                      <span className="solar-date">
                        <span className="solar-icon" aria-hidden="true">🌞</span>
                        Dia {day.solar_date.solar_day} do {day.solar_date.solar_month.toLowerCase()}
                      </span>
                    )}
                  </div>
                  {day.solar_times && (
                    <div className="solar-times">
                      <div className="times-container">
                        <div className="sunrise">
                          <span className="time-label">Nascer do Sol:</span>
                          <span className="time-value">
                            {day.solar_times.sunrise.replace(/(\d+):(\d+)/, '$1h$2')}
                          </span>
                        </div>
                        <div className="sunset">
                          <span className="time-label">Pôr do Sol:</span>
                          <span className="time-value">
                            {day.solar_times.sunset.replace(/(\d+):(\d+)/, '$1h$2')}
                          </span>
                        </div>
                      </div>
                      <DayLengthGraph 
                        sunrise={day.solar_times.sunrise.replace(/(\d+):(\d+)/, '$1h$2')}
                        sunset={day.solar_times.sunset.replace(/(\d+):(\d+)/, '$1h$2')}
                      />
                    </div>
                  )}
                </div>
              </div>
              
              <div className="events-list">
                {day.events?.map((event: Event, eventIndex: number) => {
                  console.log('Event type:', event.event_type);
                  console.log('Event:', event);
                  return (
                    <div
                      key={eventIndex}
                      className="event-item"
                      onClick={() => onEventSelect?.(event)}
                    >
                      {(event.event_type === 'equinox' || event.event_type === 'solstice') ? (
                        <>
                          {console.log('Solar Month:', day.solar_date.solar_month)}
                          <SolarEventIcon 
                            eventType={event.event_type}
                            solarMonth={day.solar_date.solar_month}
                          />
                        </>
                      ) : (
                        <span className="event-icon">{event.event_type_new?.icon || '›'}</span>
                      )}
                      <span className="event-title">{event.title}</span>
                      <span className="event-chevron">›</span>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      <div className="calendar-header footer">
        <button 
          onClick={handlePrevious} 
          className="nav-button" 
          aria-label="Mês anterior"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18L9 12L15 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
        <button 
          onClick={handleNext} 
          className="nav-button"
          aria-label="Próximo mês"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default SolarCalendar;
