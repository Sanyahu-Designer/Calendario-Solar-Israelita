import { useState, useEffect, useRef } from 'react';
import type { SolarTimes, SolarTimeDay } from '../types';
import { getSolarTimes } from '../services/api';
import { AxiosError } from 'axios';

export const useSolarTimes = (date?: Date | string) => {
  const [solarTimes, setSolarTimes] = useState<SolarTimes | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const lastRequestRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (lastRequestRef.current) {
      lastRequestRef.current.abort();
    }

    if (!date) {
      setSolarTimes(null);
      setLoading(false);
      return;
    }

    let isMounted = true;
    const controller = new AbortController();
    lastRequestRef.current = controller;

    const fetchSolarTimes = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const selectedDate = date instanceof Date ? date : new Date(date);
        const year = selectedDate.getFullYear();
        const month = selectedDate.getMonth() + 1;
        
        const response: SolarTimeDay[] = await getSolarTimes(`${year}-${month.toString().padStart(2, '0')}`);
        
        if (isMounted) {
          // Converte a lista de dias em um objeto indexado por data
          const timesMap = response.reduce((acc: SolarTimes, day) => {
            acc[day.date] = day;
            return acc;
          }, {});
          
          setSolarTimes(timesMap);
        }
      } catch (err) {
        if (isMounted && !(err instanceof DOMException && err.name === 'AbortError')) {
          const errorMessage = err instanceof AxiosError 
            ? err.response?.data?.message || 'Erro ao buscar horários solares'
            : 'Erro ao buscar horários solares';
          setError(errorMessage);
          console.error(err);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchSolarTimes();

    return () => {
      isMounted = false;
      controller.abort();
      lastRequestRef.current = null;
    };
  }, [date]);

  return { solarTimes, loading, error };
};
