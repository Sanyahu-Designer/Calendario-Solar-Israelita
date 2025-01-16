import { useState, useEffect, useCallback } from 'react';
import { CalendarMonth, SolarTimeDay, Event } from '../types';
import { getSolarCalendarMonth, getSolarTimes, getSolarEventsByMonth } from '../services/api';
import { addMonths, subMonths } from 'date-fns';
import { useGeolocation } from './useGeolocation';

export const useSolarCalendar = () => {
  const [currentDate, setCurrentDate] = useState(() => {
    const now = new Date();
    return new Date(now.getFullYear(), now.getMonth(), 1);
  });
  const [calendarData, setCalendarData] = useState<CalendarMonth | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const { latitude, longitude } = useGeolocation();

  const navigateToMonth = useCallback((direction: 'next' | 'prev') => {
    setCurrentDate(currentDate => {
      return direction === 'next'
        ? addMonths(currentDate, 1)
        : subMonths(currentDate, 1);
    });
  }, []);

  const fetchData = useCallback(async () => {
    try {
      // Não setamos loading como true aqui para manter a transição suave
      setError(null);

      const year = currentDate.getFullYear();
      const month = currentDate.getMonth() + 1;

      // Buscar dados do calendário e eventos solares em paralelo
      const [calendarMonth, solarTimes, solarEvents] = await Promise.all([
        getSolarCalendarMonth(year, month),
        getSolarTimes(
          `${year}-${month.toString().padStart(2, '0')}-${currentDate.getDate()}`,
          latitude,
          longitude
        ),
        getSolarEventsByMonth(year, month)
      ]);

      // Criar um mapa dos horários solares indexado por data
      const solarTimesMap = solarTimes.reduce((acc, day) => {
        if (day.date) {
          acc[day.date] = day;
        }
        return acc;
      }, {} as Record<string, SolarTimeDay>);

      // Criar um mapa dos eventos solares indexado por data
      const solarEventsMap = solarEvents.reduce((acc, event) => {
        if (event.gregorian_date) {
          if (!acc[event.gregorian_date]) {
            acc[event.gregorian_date] = [];
          }
          acc[event.gregorian_date].push(event);
        }
        return acc;
      }, {} as Record<string, Event[]>);

      // Adicionar os horários solares e eventos solares aos dias do calendário
      const updatedDays = calendarMonth.days.map(day => {
        const solarTime = day.gregorian_date ? solarTimesMap[day.gregorian_date] : undefined;
        
        // Começar com os eventos não solares
        const events = [...(day.events || [])].filter(event => 
          event.event_type !== 'equinox' && event.event_type !== 'solstice'
        );
        
        // Adicionar eventos solares do backend
        if (day.gregorian_date && solarEventsMap[day.gregorian_date]) {
          const solarEvents = solarEventsMap[day.gregorian_date].filter(event => 
            event.event_type === 'equinox' || event.event_type === 'solstice'
          );
          events.push(...solarEvents);
        }

        return {
          ...day,
          solar_times: solarTime,
          events
        };
      });

      setCalendarData({
        ...calendarMonth,
        days: updatedDays
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao carregar o calendário';
      setError(errorMessage);
      if (retryCount < 3) {
        setRetryCount(count => count + 1);
      }
    } finally {
      setLoading(false);
    }
  }, [currentDate, latitude, longitude, retryCount]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return {
    calendarData,
    currentDate,
    loading,
    error,
    handlePreviousMonth: () => navigateToMonth('prev'),
    handleNextMonth: () => navigateToMonth('next')
  };
};
