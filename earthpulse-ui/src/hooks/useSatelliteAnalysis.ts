import { useState } from 'react';
import { getNDVI, type NDVIResult } from '../services/api';

export function useSatelliteAnalysis() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<NDVIResult | null>(null);

  const analyze = async (latitude: number, longitude: number) => {
    setLoading(true);
    try {
      const data = await getNDVI(latitude, longitude);
      setResult(data);
    } catch (error) {
      console.error('Error analyzing satellite data:', error);
    } finally {
      setLoading(false);
    }
  };

  return { result, loading, analyze };
}