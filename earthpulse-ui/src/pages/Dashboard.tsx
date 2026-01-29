import { useEffect, useState } from 'react';
import Map, { Marker, Popup } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from '../components/Navbar';
import { API_URL } from '../config';

const MAPBOX_TOKEN = 'pk.eyJ1Ijoic3VtaXRjbDciLCJhIjoiY200a2pvbXJ0MGF4bjJxcHlrM2g0cnVpOSJ9.8mjUxVmZJTF_KyTvq5xKyw';

interface Event {
  id: number;
  title: string;
  description: string;
  event_type: string;
  severity: string;
  location: {
    name: string;
    latitude: number;
    longitude: number;
  };
  is_verified: boolean;
  verification_score: number | null;
  created_at: string;
}

interface Stats {
  total_events: number;
  verified_events: number;
  unverified_events: number;
  events_by_type: {
    wildfire: number;
    flood: number;
    deforestation: number;
    drought: number;
  };
  events_by_severity: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
}

const eventTypeColors = {
  wildfire: '#ff4444',
  flood: '#4444ff',
  deforestation: '#44ff44',
  drought: '#ffaa00'
};

const severityColors = {
  critical: '#ff0000',
  high: '#ff6600',
  medium: '#ffaa00',
  low: '#ffff00'
};

export default function Dashboard() {
  const [events, setEvents] = useState<Event[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [loading, setLoading] = useState(true);
  const [verifying, setVerifying] = useState<number | null>(null);

  const [viewState, setViewState] = useState({
    longitude: 0,
    latitude: 20,
    zoom: 2
  });

  useEffect(() => {
    fetchEvents();
    fetchStats();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await fetch(`${API_URL}/api/events`);
      const data = await response.json();
      setEvents(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching events:', error);
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_URL}/api/stats`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const verifyEvent = async (eventId: number) => {
    setVerifying(eventId);
    try {
      const response = await fetch(`${API_URL}/api/events/${eventId}/verify`, {
        method: 'POST',
      });
      const data = await response.json();
      console.log('Verification result:', data);
      
      setTimeout(() => {
        fetchEvents();
        setVerifying(null);
      }, 10000);
    } catch (error) {
      console.error('Error verifying event:', error);
      setVerifying(null);
    }
  };

  return (
    <div style={{ height: '100vh', background: '#0a0a0f', color: 'white', overflow: 'hidden' }}>
      <Navbar />
      
      <div style={{ display: 'flex', height: 'calc(100vh - 70px)', marginTop: '70px' }}>
        {/* Sidebar */}
        <motion.div
          initial={{ x: -300 }}
          animate={{ x: 0 }}
          style={{
            width: '350px',
            background: 'rgba(20, 20, 30, 0.95)',
            backdropFilter: 'blur(10px)',
            borderRight: '1px solid rgba(255, 255, 255, 0.1)',
            overflowY: 'auto',
            padding: '20px'
          }}
        >
          <h2 style={{ fontSize: '24px', marginBottom: '20px' }}> Statistics</h2>
          
          {stats && (
            <div style={{ marginBottom: '30px' }}>
              <div style={{
                padding: '20px',
                background: 'rgba(102, 126, 234, 0.1)',
                borderRadius: '12px',
                marginBottom: '15px'
              }}>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#667eea' }}>
                  {stats.total_events}
                </div>
                <div style={{ opacity: 0.7 }}>Total Events</div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '20px' }}>
                <div style={{ padding: '15px', background: 'rgba(76, 175, 80, 0.1)', borderRadius: '8px' }}>
                  <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#4CAF50' }}>
                    {stats.verified_events}
                  </div>
                  <div style={{ fontSize: '12px', opacity: 0.7 }}>Verified</div>
                </div>
                <div style={{ padding: '15px', background: 'rgba(255, 152, 0, 0.1)', borderRadius: '8px' }}>
                  <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#FF9800' }}>
                    {stats.unverified_events}
                  </div>
                  <div style={{ fontSize: '12px', opacity: 0.7 }}>Unverified</div>
                </div>
              </div>

              <h3 style={{ fontSize: '16px', marginBottom: '10px', marginTop: '20px' }}>By Type</h3>
              {Object.entries(stats.events_by_type).map(([type, count]) => (
                <div key={type} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  padding: '8px 12px',
                  background: 'rgba(255, 255, 255, 0.03)',
                  borderRadius: '6px',
                  marginBottom: '6px'
                }}>
                  <span style={{ textTransform: 'capitalize' }}>
                    {type === 'wildfire' && '🔥'}
                    {type === 'flood' && '💧'}
                    {type === 'deforestation' && '🌳'}
                    {type === 'drought' && '☀️'}
                    {' '}{type}
                  </span>
                  <span style={{ fontWeight: 'bold' }}>{count}</span>
                </div>
              ))}
            </div>
          )}

          <h2 style={{ fontSize: '20px', marginTop: '30px', marginBottom: '15px' }}>🌍 Recent Events</h2>
          
          {loading ? (
            <div style={{ textAlign: 'center', padding: '40px' }}>Loading...</div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {events.map((event) => (
                <motion.div
                  key={event.id}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => {
                    setSelectedEvent(event);
                    setViewState({
                      longitude: event.location.longitude,
                      latitude: event.location.latitude,
                      zoom: 8
                    });
                  }}
                  style={{
                    padding: '15px',
                    background: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    border: `2px solid ${eventTypeColors[event.event_type as keyof typeof eventTypeColors]}`,
                    transition: 'all 0.3s'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>{event.title}</div>
                      <div style={{ fontSize: '12px', opacity: 0.7 }}>{event.location.name}</div>
                    </div>
                    <div style={{
                      padding: '4px 10px',
                      borderRadius: '12px',
                      fontSize: '10px',
                      fontWeight: 'bold',
                      background: severityColors[event.severity as keyof typeof severityColors],
                      color: '#000'
                    }}>
                      {event.severity.toUpperCase()}
                    </div>
                  </div>
                  
                  {event.is_verified && (
                    <div style={{
                      marginTop: '8px',
                      fontSize: '11px',
                      color: '#4CAF50',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px'
                    }}>
                      ✓ Verified
                      {event.verification_score && (
                        <span style={{ opacity: 0.7 }}>
                          ({Math.round(event.verification_score * 100)}%)
                        </span>
                      )}
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Map */}
        <div style={{ flex: 1, position: 'relative' }}>
          <Map
            {...viewState}
            onMove={(evt) => setViewState(evt.viewState)}
            mapboxAccessToken={MAPBOX_TOKEN}
            style={{ width: '100%', height: '100%' }}
            mapStyle="mapbox://styles/mapbox/dark-v11"
          >
            {events.map((event) => (
              <Marker
                key={event.id}
                longitude={event.location.longitude}
                latitude={event.location.latitude}
                anchor="bottom"
                onClick={(e) => {
                  e.originalEvent.stopPropagation();
                  setSelectedEvent(event);
                }}
              >
                <div style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '50%',
                  background: eventTypeColors[event.event_type as keyof typeof eventTypeColors],
                  border: '3px solid white',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '20px',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
                  animation: event.is_verified ? 'none' : 'pulse 2s infinite'
                }}>
                  {event.event_type === 'wildfire' && '🔥'}
                  {event.event_type === 'flood' && '💧'}
                  {event.event_type === 'deforestation' && '🌳'}
                  {event.event_type === 'drought' && '☀️'}
                </div>
              </Marker>
            ))}

            <AnimatePresence>
              {selectedEvent && (
                <Popup
                  longitude={selectedEvent.location.longitude}
                  latitude={selectedEvent.location.latitude}
                  anchor="top"
                  onClose={() => setSelectedEvent(null)}
                  closeOnClick={false}
                >
                  <div style={{
                    padding: '15px',
                    minWidth: '280px',
                    background: '#1a1a2e',
                    color: 'white',
                    borderRadius: '8px'
                  }}>
                    <h3 style={{ margin: '0 0 10px 0', fontSize: '16px' }}>{selectedEvent.title}</h3>
                    <p style={{ margin: '0 0 10px 0', fontSize: '13px', opacity: 0.8 }}>
                      {selectedEvent.description}
                    </p>
                    
                    <div style={{ display: 'flex', gap: '8px', marginBottom: '10px', flexWrap: 'wrap' }}>
                      <span style={{
                        padding: '4px 10px',
                        borderRadius: '12px',
                        fontSize: '11px',
                        background: eventTypeColors[selectedEvent.event_type as keyof typeof eventTypeColors],
                        color: 'white'
                      }}>
                        {selectedEvent.event_type}
                      </span>
                      <span style={{
                        padding: '4px 10px',
                        borderRadius: '12px',
                        fontSize: '11px',
                        background: severityColors[selectedEvent.severity as keyof typeof severityColors],
                        color: '#000'
                      }}>
                        {selectedEvent.severity}
                      </span>
                    </div>

                    <div style={{ fontSize: '12px', opacity: 0.7, marginBottom: '10px' }}>
                       {selectedEvent.location.name}
                    </div>

                    {selectedEvent.is_verified ? (
                      <div style={{
                        padding: '8px',
                        background: 'rgba(76, 175, 80, 0.2)',
                        borderRadius: '6px',
                        fontSize: '12px',
                        color: '#4CAF50'
                      }}>
                        ✓ Verified by Satellite
                        {selectedEvent.verification_score && (
                          <div style={{ marginTop: '4px' }}>
                            Confidence: {Math.round(selectedEvent.verification_score * 100)}%
                          </div>
                        )}
                      </div>
                    ) : (
                      <button
                        onClick={() => verifyEvent(selectedEvent.id)}
                        disabled={verifying === selectedEvent.id}
                        style={{
                          width: '100%',
                          padding: '10px',
                          background: verifying === selectedEvent.id ? '#555' : '#667eea',
                          border: 'none',
                          borderRadius: '6px',
                          color: 'white',
                          cursor: verifying === selectedEvent.id ? 'not-allowed' : 'pointer',
                          fontSize: '12px',
                          fontWeight: 'bold'
                        }}
                      >
                        {verifying === selectedEvent.id ? ' Analyzing...' : ' Verify with Satellite Data'}
                      </button>
                    )}
                  </div>
                </Popup>
              )}
            </AnimatePresence>
          </Map>

          <style>{`
            @keyframes pulse {
              0%, 100% { transform: scale(1); opacity: 1; }
              50% { transform: scale(1.1); opacity: 0.8; }
            }
          `}</style>
        </div>
      </div>
    </div>
  );
}