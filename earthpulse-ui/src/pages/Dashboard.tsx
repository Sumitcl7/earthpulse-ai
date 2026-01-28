import { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import Navbar from '../components/Navbar';
import { motion } from 'framer-motion';

mapboxgl.accessToken = 'pk.eyJ1Ijoic3VtZGV2czEiLCJhIjoiY21oNTV5dHg4MDNsMDJycjBhY3NjcWVlciJ9.zj7lBK4wXxHLD8ChLJxztA';

const EVENT_COLORS: any = {
  wildfire: '#ef4444',
  flood: '#3b82f6',
  deforestation: '#22c55e',
  drought: '#f59e0b',
};

export default function Dashboard() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const markersRef = useRef<mapboxgl.Marker[]>([]);
  
  const [events, setEvents] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [selectedEvent, setSelectedEvent] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [verifying, setVerifying] = useState<number | null>(null);

  // Fetch events
  useEffect(() => {
    console.log(' Fetching events from API...');
    
    fetch('http://127.0.0.1:8000/api/events')
      .then(res => {
        console.log('📡 Response status:', res.status);
        return res.json();
      })
      .then(data => {
        console.log(' Events loaded:', data);
        console.log(' Number of events:', data.length);
        setEvents(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(' Error loading events:', err);
        setLoading(false);
      });
    
    fetch('http://127.0.0.1:8000/api/stats')
      .then(res => res.json())
      .then(data => {
        console.log(' Stats loaded:', data);
        setStats(data);
      })
      .catch(err => console.error('Error loading stats:', err));
  }, []);

  // Verify event function
  const verifyEvent = async (eventId: number) => {
    setVerifying(eventId);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/events/${eventId}/verify`, {
        method: 'POST',
      });
      const result = await response.json();
      console.log('Verification started:', result);
      
      setTimeout(() => {
        fetch('http://127.0.0.1:8000/api/events')
          .then(res => res.json())
          .then(data => {
            setEvents(data);
            const updatedEvent = data.find((e: any) => e.id === eventId);
            if (updatedEvent) {
              setSelectedEvent(updatedEvent);
            }
            setVerifying(null);
          });
      }, 8000);
    } catch (err) {
      console.error('Error verifying event:', err);
      setVerifying(null);
    }
  };

  // Initialize map
  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/satellite-streets-v12',
      center: [0, 20],
      zoom: 2,
    });

    map.current.addControl(new mapboxgl.NavigationControl(), 'top-right');
  }, []);

  // Add markers
  useEffect(() => {
    if (!map.current || loading || events.length === 0) return;

    markersRef.current.forEach(m => m.remove());
    markersRef.current = [];

    events.forEach((event) => {
      const el = document.createElement('div');
      el.style.width = '24px';
      el.style.height = '24px';
      el.style.borderRadius = '50%';
      el.style.backgroundColor = EVENT_COLORS[event.event_type] || '#999';
      el.style.border = '3px solid white';
      el.style.cursor = 'pointer';
      el.style.boxShadow = '0 4px 12px rgba(0,0,0,0.5)';
      el.style.transition = 'transform 0.2s';
      
      if (event.is_verified) {
        el.style.border = '3px solid #22c55e';
        el.style.boxShadow = '0 0 20px rgba(34, 197, 94, 0.6)';
      }
      
      el.addEventListener('mouseenter', () => {
        el.style.transform = 'scale(1.3)';
      });
      el.addEventListener('mouseleave', () => {
        el.style.transform = 'scale(1)';
      });

      const marker = new mapboxgl.Marker(el)
        .setLngLat([event.location.longitude, event.location.latitude])
        .addTo(map.current!);

      el.addEventListener('click', () => {
        setSelectedEvent(event);
        map.current?.flyTo({
          center: [event.location.longitude, event.location.latitude],
          zoom: 8,
          duration: 2000,
        });
      });

      markersRef.current.push(marker);
    });

    console.log(` Added ${markersRef.current.length} markers to map`);
  }, [events, loading]);

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar />

      <div style={{ flex: 1, display: 'flex', marginTop: '60px' }}>
        <div ref={mapContainer} style={{ flex: 1 }} />

        <motion.div
          initial={{ x: 100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          style={{
            width: '400px',
            background: 'rgba(10, 10, 15, 0.95)',
            backdropFilter: 'blur(20px)',
            borderLeft: '1px solid rgba(255,255,255,0.1)',
            padding: '30px',
            overflowY: 'auto',
          }}
        >
          {loading ? (
            <div>Loading...</div>
          ) : (
            <>
              <h2 style={{ fontSize: '24px', marginBottom: '20px', fontWeight: 600 }}>
                {selectedEvent ? selectedEvent.title : 'Global Events'}
              </h2>

              {!selectedEvent && stats && (
                <>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '20px' }}>
                    <div style={{ padding: '16px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                      <div style={{ fontSize: '13px', opacity: 0.6 }}>TOTAL</div>
                      <div style={{ fontSize: '28px', fontWeight: 700 }}>{stats.total_events}</div>
                    </div>
                    <div style={{ padding: '16px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                      <div style={{ fontSize: '13px', opacity: 0.6 }}>VERIFIED</div>
                      <div style={{ fontSize: '28px', fontWeight: 700, color: '#22c55e' }}>{stats.verified_events}</div>
                    </div>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginBottom: '24px' }}>
                    <div style={{ padding: '10px', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '6px', borderLeft: '3px solid #ef4444' }}>
                      <div style={{ fontSize: '12px', opacity: 0.7 }}>🔥 Wildfires</div>
                      <div style={{ fontSize: '20px', fontWeight: 600 }}>{stats.events_by_type.wildfire}</div>
                    </div>
                    <div style={{ padding: '10px', background: 'rgba(59, 130, 246, 0.1)', borderRadius: '6px', borderLeft: '3px solid #3b82f6' }}>
                      <div style={{ fontSize: '12px', opacity: 0.7 }}>💧 Floods</div>
                      <div style={{ fontSize: '20px', fontWeight: 600 }}>{stats.events_by_type.flood}</div>
                    </div>
                    <div style={{ padding: '10px', background: 'rgba(34, 197, 94, 0.1)', borderRadius: '6px', borderLeft: '3px solid #22c55e' }}>
                      <div style={{ fontSize: '12px', opacity: 0.7 }}>🌳 Deforest</div>
                      <div style={{ fontSize: '20px', fontWeight: 600 }}>{stats.events_by_type.deforestation}</div>
                    </div>
                    <div style={{ padding: '10px', background: 'rgba(245, 158, 11, 0.1)', borderRadius: '6px', borderLeft: '3px solid #f59e0b' }}>
                      <div style={{ fontSize: '12px', opacity: 0.7 }}>☀️ Droughts</div>
                      <div style={{ fontSize: '20px', fontWeight: 600 }}>{stats.events_by_type.drought}</div>
                    </div>
                  </div>

                  <h3 style={{ fontSize: '16px', marginBottom: '16px' }}>Recent Events</h3>
                  {events.slice(0, 5).map((event) => (
                    <div
                      key={event.id}
                      onClick={() => setSelectedEvent(event)}
                      style={{
                        padding: '14px',
                        background: 'rgba(255,255,255,0.03)',
                        borderRadius: '8px',
                        marginBottom: '12px',
                        borderLeft: `3px solid ${EVENT_COLORS[event.event_type]}`,
                        cursor: 'pointer',
                        transition: 'all 0.2s',
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.background = 'rgba(255,255,255,0.08)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.background = 'rgba(255,255,255,0.03)';
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                        <div style={{ fontSize: '14px', fontWeight: 500 }}>{event.title}</div>
                        {event.is_verified && <span style={{ fontSize: '16px' }}>✅</span>}
                      </div>
                      <div style={{ fontSize: '12px', opacity: 0.5 }}>
                        {event.location.name} • {new Date(event.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  ))}
                </>
              )}

              {selectedEvent && (
                <div>
                  <p style={{ fontSize: '14px', opacity: 0.7, marginBottom: '16px' }}>{selectedEvent.description}</p>

                  <div style={{ padding: '16px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', marginBottom: '12px' }}>
                    <div style={{ fontSize: '13px', opacity: 0.6 }}>TYPE</div>
                    <div style={{ fontSize: '16px', textTransform: 'capitalize', marginTop: '4px' }}>{selectedEvent.event_type}</div>
                  </div>

                  <div style={{ padding: '16px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', marginBottom: '12px' }}>
                    <div style={{ fontSize: '13px', opacity: 0.6 }}>SEVERITY</div>
                    <div style={{ 
                      fontSize: '16px', 
                      textTransform: 'uppercase',
                      marginTop: '4px',
                      color: selectedEvent.severity === 'critical' ? '#ef4444' : selectedEvent.severity === 'high' ? '#f59e0b' : '#22c55e'
                    }}>
                      {selectedEvent.severity}
                    </div>
                  </div>

                  <div style={{ padding: '16px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', marginBottom: '12px' }}>
                    <div style={{ fontSize: '13px', opacity: 0.6 }}>LOCATION</div>
                    <div style={{ fontSize: '14px', marginTop: '4px' }}>
                      {selectedEvent.location.name}<br/>
                      <span style={{ opacity: 0.5, fontSize: '12px' }}>
                        {selectedEvent.location.latitude.toFixed(4)}, {selectedEvent.location.longitude.toFixed(4)}
                      </span>
                    </div>
                  </div>

                  <div style={{ 
                    padding: '16px', 
                    background: selectedEvent.is_verified ? 'rgba(34, 197, 94, 0.1)' : 'rgba(245, 158, 11, 0.1)', 
                    borderRadius: '8px', 
                    marginBottom: '16px',
                    borderLeft: `3px solid ${selectedEvent.is_verified ? '#22c55e' : '#f59e0b'}`
                  }}>
                    <div style={{ fontSize: '13px', opacity: 0.6 }}>VERIFICATION</div>
                    <div style={{ fontSize: '16px', marginTop: '4px' }}>
                      {selectedEvent.is_verified ? (
                        <>
                           Verified
                          {selectedEvent.verification_score && (
                            <span style={{ marginLeft: '8px', opacity: 0.7, fontSize: '14px' }}>
                              ({(selectedEvent.verification_score * 100).toFixed(0)}% confidence)
                            </span>
                          )}
                        </>
                      ) : (
                        ' Not Verified'
                      )}
                    </div>
                  </div>

                  {!selectedEvent.is_verified && (
                    <button
                      onClick={() => verifyEvent(selectedEvent.id)}
                      disabled={verifying === selectedEvent.id}
                      style={{
                        width: '100%',
                        padding: '14px',
                        background: verifying === selectedEvent.id 
                          ? 'rgba(100,100,100,0.3)' 
                          : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        border: 'none',
                        borderRadius: '8px',
                        color: 'white',
                        cursor: verifying === selectedEvent.id ? 'wait' : 'pointer',
                        fontSize: '15px',
                        fontWeight: 600,
                        marginBottom: '12px',
                        transition: 'all 0.2s',
                      }}
                    >
                      {verifying === selectedEvent.id ? ' Analyzing Satellite Data...' : ' Verify with Satellite Data'}
                    </button>
                  )}

                  <button
                    onClick={() => setSelectedEvent(null)}
                    style={{
                      width: '100%',
                      padding: '12px',
                      background: 'rgba(255,255,255,0.1)',
                      border: '1px solid rgba(255,255,255,0.2)',
                      borderRadius: '8px',
                      color: 'white',
                      cursor: 'pointer',
                      fontSize: '14px',
                      fontWeight: 500,
                      transition: 'all 0.2s',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = 'rgba(255,255,255,0.15)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'rgba(255,255,255,0.1)';
                    }}
                  >
                    ← Back to List
                  </button>
                </div>
              )}
            </>
          )}
        </motion.div>
      </div>
    </div>
  );
}