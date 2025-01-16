import axios, { AxiosError } from 'axios';
import { Event, CalendarMonth, SolarDate, SolarTimeDay } from '../types';

const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // 1 segundo

// API Solar
const solarApi = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/solar',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

const sleep = (ms: number): Promise<void> => new Promise(resolve => setTimeout(resolve, ms));

const handleError = (error: unknown): never => {
  if (error instanceof AxiosError) {
    if (error.response) {
      const statusCode = error.response.status;
      const errorMessage = error.response.data?.detail || error.response.data?.error || 'Erro na requisição';
      console.error(`Erro ${statusCode}: ${errorMessage}`);
      throw new Error(errorMessage);
    } else if (error.request) {
      console.error('Sem resposta do servidor');
      throw new Error('Sem resposta do servidor');
    } else {
      console.error('Erro na configuração da requisição', error.message);
      throw new Error('Erro na configuração da requisição');
    }
  }
  throw error;
};

const retryRequest = async <T>(
  requestFn: () => Promise<T>,
  retries: number = MAX_RETRIES
): Promise<T> => {
  try {
    return await requestFn();
  } catch (error) {
    if (retries > 0) {
      await sleep(RETRY_DELAY);
      return retryRequest(requestFn, retries - 1);
    }
    throw error;
  }
};

// Cache para o calendário solar
const solarCache = new Map<string, { data: CalendarMonth; timestamp: number }>();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutos

// Funções do Calendário Solar
export const getSolarCalendarMonth = async (year: number, month: number): Promise<CalendarMonth> => {
  const cacheKey = `${year}-${month}`;
  const cachedData = solarCache.get(cacheKey);

  if (cachedData && (Date.now() - cachedData.timestamp) < CACHE_DURATION) {
    return cachedData.data;
  }

  try {
    const response = await solarApi.get<CalendarMonth>(`/calendar/?year=${year}&month=${month}`);
    const calendarData = response.data;

    solarCache.set(cacheKey, {
      data: calendarData,
      timestamp: Date.now()
    });

    return calendarData;
  } catch (error) {
    return handleError(error);
  }
};

// Funções de eventos solares
export const getSolarEvents = async (): Promise<Event[]> => {
  try {
    const response = await solarApi.get<Event[]>('/events/');
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

export const getSolarEventsByDate = async (date: string): Promise<Event[]> => {
  try {
    const response = await solarApi.get<Event[]>(`/events/?date=${date}`);
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

export const getSolarEventsByMonth = async (year: number, month: number): Promise<Event[]> => {
  try {
    const response = await solarApi.get<Event[]>(`/events/?year=${year}&month=${month}`);
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

export const getSolarEvent = async (id: number): Promise<Event> => {
  try {
    const response = await solarApi.get<Event>(`/events/${id}/`);
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

// Funções de horários solares
export const getSolarTimes = async (
  date: string,
  latitude?: number | null,
  longitude?: number | null
): Promise<SolarTimeDay[]> => {
  try {
    let url = `/solar-times/?date=${date}`;
    if (latitude != null && longitude != null) {
      url += `&latitude=${latitude}&longitude=${longitude}`;
    }

    const response = await retryRequest(() => 
      solarApi.get<SolarTimeDay[]>(url)
    );
    
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar horários solares:', error);
    return handleError(error);
  }
};

// Funções compartilhadas
export const convertDate = async (gregorianDate: string): Promise<SolarDate> => {
  try {
    const response = await solarApi.get<SolarDate>(`/convert-date/?date=${gregorianDate}`);
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};
