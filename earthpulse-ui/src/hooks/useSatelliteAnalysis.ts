import { useState } from 'react';
import { getNDVI, NDVIResult } from '../services/api';

export const useSatelliteAnalysis = () => {
  const [loading, setLoading] = useState(false);

  const analyzeNDVI = async (latitude: number, longitude: number): Promise<NDVIResult | null> => {
    try {
      setLoading(true);
      const result = await getNDVI(latitude, longitude);
      return result;
    } catch (err) {
      console.error('Error analyzing NDVI:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { analyzeNDVI, loading };
};