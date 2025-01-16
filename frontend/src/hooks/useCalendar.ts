import { useState, useEffect, useCallback } from 'react';
import { CalendarMonth, CalendarDay } from '../types';
import { getSolarCalendarMonth } from '../services/api';
import { format, addMonths, subMonths } from 'date-fns';
import { ptBR } from 'date-fns/locale';

export const useCalendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [calendarData, setCalendarData] = useState<CalendarMonth | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  const fetchCalendarData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const year = currentDate.getFullYear();
      const month = currentDate.getMonth() + 1;

      console.log('Fetching calendar data for:', year, month);
      const monthData = await getSolarCalendarMonth(year, month);
      console.log('Received calendar data:', monthData);

      if (!monthData || !Array.isArray(monthData.days)) {
        throw new Error('Dados do calendário inválidos');
      }

      // Adiciona isToday para o dia atual
      const today = new Date();
      const todayStr = format(today, 'yyyy-MM-dd');

      const updatedDays = monthData.days.map((day: CalendarDay) => ({
        ...day,
        isToday: day.gregorian_date === todayStr,
        date: day.gregorian_date
      }));

      console.log('Setting calendar data with days:', updatedDays);
      setCalendarData({
        ...monthData,
        days: updatedDays
      });
      
      // Reseta o contador de tentativas em caso de sucesso
      setRetryCount(0);
      setError(null);
    } catch (err) {
      console.error('Error fetching calendar data:', err);
      
      // Incrementa o contador de tentativas
      setRetryCount(prev => prev + 1);
      
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Erro ao carregar dados do calendário');
      }
    } finally {
      setLoading(false);
    }
  }, [currentDate]);

  useEffect(() => {
    fetchCalendarData();
  }, [fetchCalendarData]);

  const navigateToMonth = useCallback((direction: 'prev' | 'next') => {
    setCurrentDate(prevDate => {
      return direction === 'next' ? addMonths(prevDate, 1) : subMonths(prevDate, 1);
    });
  }, []);

  const retry = useCallback(() => {
    if (retryCount < 3) {
      fetchCalendarData();
    }
  }, [retryCount, fetchCalendarData]);

  const currentMonthStr = format(currentDate, 'MMMM yyyy', { locale: ptBR });

  return {
    currentDate,
    currentMonthStr,
    calendarData,
    loading,
    error,
    navigateToMonth,
    retry,
    canRetry: retryCount < 3
  };
};
