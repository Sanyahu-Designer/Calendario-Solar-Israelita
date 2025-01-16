export type EventType = 'festival' | 'historical' | 'sabbath' | 'new_month' | 'equinox' | 'solstice' | 'tekufah';

export interface EventTypeNew {
  id: number;
  name: string;
  slug: string;
  color: string;
  icon: string;
}

export interface BiblicalReference {
  id: number;
  book: string;
  chapter: number;
  verse: string;
  text: string;
}

export interface SolarDate {
  gregorian_date: string;
  solar_day: number;
  solar_month: string;
  is_extra_day: boolean;
  extra_day_number?: number;
}

export interface Event {
  id: number;
  title: string;
  description: string;
  gregorian_date: string;
  solar_date: SolarDate;
  event_type: EventType;
  event_type_new: EventTypeNew;
  is_holy_day: boolean;
  sunset_start: boolean;
  biblical_references: BiblicalReference[];
}

export interface CalendarDay {
  gregorian_date: string;
  solar_date: SolarDate;
  is_current_month: boolean;
  events: Event[];
  isToday?: boolean;
  solar_times?: SolarTimeDay;
}

export interface CalendarMonth {
  year: number;
  month: number;
  days: CalendarDay[];
}

export interface Festival {
  id: number;
  name: string;
  description: string;
  start_date: string;
  end_date: string;
  is_holy_day: boolean;
}

export interface SolarTimeDay {
  date: string;
  sunrise: string;
  sunset: string;
  dawn: string;
  dusk: string;
  solar_noon: string;
  day_length: string;
  timezone: string;
  season_type?: 'equinox' | 'solstice' | null;
  season_time?: string;
}

export type SolarTimes = Record<string, SolarTimeDay>;
