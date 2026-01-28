// src/services/api.ts
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Location {
  latitude: number;
  longitude: number;
  name?: string;
  country?: string;
}

export interface Event {
  id: number;
  event_type: 'wildfire' | 'flood' | 'deforestation' | 'drought';
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  location: Location;
  source_url: string | null;
  published_at: string;
  is_verified: boolean;
  verification_status: string;
  verification_score: number | null;
  created_at: string;
}

export interface Stats {
  total_events: number;
  verified_events: number;
  verification_rate: number;
  events_by_type: {
    wildfire: number;
    flood: number;
    deforestation: number;
    drought: number;
  };
}

export interface NDVIResult {
  ndvi_mean: number | null;
  location: Location;
  interpretation: string;
  data_type: string;
  image_count?: number;
}

export const getStats = async (): Promise<Stats> => {
  const response = await api.get('/api/stats');
  return response.data;
};

export const getEvents = async (): Promise<Event[]> => {
  const response = await api.get('/api/events');
  return response.data;
};

export const getNDVI = async (
  latitude: number,
  longitude: number,
  radius_km: number = 10
): Promise<NDVIResult> => {
  const response = await api.get('/api/satellite/ndvi', {
    params: { latitude, longitude, radius_km },
  });
  return response.data;
};

export default api;