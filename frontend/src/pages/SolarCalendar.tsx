import React, { useState } from 'react';
import SolarCalendar from '../components/Calendar/SolarCalendar';
import { Event } from '../types';
import SolarEventDetails from '../components/EventDetails/SolarEventDetails';
import { useSolarCalendar } from '../hooks/useSolarCalendar';

const SolarCalendarPage: React.FC = () => {
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const { 
    currentDate, 
    calendarData, 
    loading, 
    error, 
    handlePreviousMonth,
    handleNextMonth 
  } = useSolarCalendar();

  const handleEventSelect = (event: Event) => {
    console.log('Event selected:', event);
    setSelectedEvent(event);
  };

  const handleCloseEventDetails = () => {
    console.log('Closing event details');
    setSelectedEvent(null);
  };

  if (loading) {
    return <div className="loading">Carregando...</div>;
  }

  console.log('Selected event:', selectedEvent);

  return (
    <div className="calendar-page">
      <SolarCalendar
        calendarData={calendarData}
        currentDate={currentDate}
        onEventSelect={handleEventSelect}
        handlePreviousMonth={handlePreviousMonth}
        handleNextMonth={handleNextMonth}
        error={error || undefined}
      />
      {selectedEvent && (
        <SolarEventDetails
          event={selectedEvent}
          onClose={handleCloseEventDetails}
        />
      )}
    </div>
  );
};

export default SolarCalendarPage;
