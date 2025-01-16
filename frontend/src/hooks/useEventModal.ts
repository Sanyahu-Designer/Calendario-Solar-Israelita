import { useState } from 'react';
import { Event } from '../types';

export const useEventModal = () => {
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleEventSelect = (event: Event) => {
    setSelectedEvent(event);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedEvent(null);
  };

  return {
    selectedEvent,
    isModalOpen,
    handleEventSelect,
    handleCloseModal
  };
};
