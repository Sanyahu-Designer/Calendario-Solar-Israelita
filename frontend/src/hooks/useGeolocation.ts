import { useState, useEffect, useCallback } from 'react';

interface GeolocationState {
  latitude: number | null;
  longitude: number | null;
  error: string | null;
  loading: boolean;
}

const STORAGE_KEY = 'solar_calendar_location';

const getStoredLocation = () => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const { latitude, longitude } = JSON.parse(stored);
      return { latitude, longitude };
    }
  } catch (error) {
    console.error('Error reading stored location:', error);
  }
  return null;
};

const storeLocation = (latitude: number, longitude: number) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ latitude, longitude }));
  } catch (error) {
    console.error('Error storing location:', error);
  }
};

export const useGeolocation = () => {
  const [state, setState] = useState<GeolocationState>(() => {
    const stored = getStoredLocation();
    return {
      latitude: stored?.latitude || null,
      longitude: stored?.longitude || null,
      error: null,
      loading: !stored
    };
  });

  const requestGeolocation = useCallback(() => {
    // Se já temos a localização, não precisamos pedir novamente
    if (state.latitude && state.longitude) {
      setState(prev => ({ ...prev, loading: false }));
      return;
    }

    setState(prev => ({ ...prev, loading: true, error: null }));

    if (!navigator.geolocation) {
      setState(prev => ({
        ...prev,
        error: 'Geolocalização não é suportada pelo seu navegador. Por favor, tente usar um navegador mais moderno.',
        loading: false
      }));
      return;
    }

    const handleSuccess = (position: GeolocationPosition) => {
      const { latitude, longitude } = position.coords;
      storeLocation(latitude, longitude);
      setState({
        latitude,
        longitude,
        error: null,
        loading: false
      });
    };

    const handleError = (error: GeolocationPositionError) => {
      let errorMessage = 'Erro ao obter sua localização.';
      
      switch (error.code) {
        case error.PERMISSION_DENIED:
          errorMessage = 'Você precisa permitir o acesso à sua localização para que possamos calcular os horários solares corretamente.';
          break;
        case error.POSITION_UNAVAILABLE:
          errorMessage = 'Não foi possível determinar sua localização. Por favor, verifique se o GPS está ativado.';
          break;
        case error.TIMEOUT:
          errorMessage = 'O tempo para obter sua localização expirou. Por favor, tente novamente.';
          break;
      }
      
      // Se temos uma localização armazenada, usamos ela mesmo com erro
      const stored = getStoredLocation();
      if (stored) {
        setState({
          latitude: stored.latitude,
          longitude: stored.longitude,
          error: null,
          loading: false
        });
        return;
      }

      setState(prev => ({
        ...prev,
        error: errorMessage,
        loading: false
      }));
    };

    navigator.geolocation.getCurrentPosition(
      handleSuccess,
      handleError,
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 30 * 60 * 1000 // Aceita posições de até 30 minutos atrás
      }
    );
  }, [state.latitude, state.longitude]);

  useEffect(() => {
    requestGeolocation();
  }, [requestGeolocation]);

  return {
    latitude: state.latitude,
    longitude: state.longitude,
    error: state.error,
    loading: state.loading,
    requestGeolocation
  };
};
