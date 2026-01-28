import { useEffect, useState } from 'react';

export default function TestAPI() {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/events')
      .then(res => res.json())
      .then(data => {
        console.log('✅ Got events:', data);
        setEvents(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('❌ Error:', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: '40px', background: '#0a0a0f', color: 'white', minHeight: '100vh' }}>
      <h1>🧪 API Connection Test</h1>
      
      {loading && <p>Loading...</p>}
      {error && <div style={{ color: 'red' }}>❌ Error: {error}</div>}
      
      {events.length > 0 && (
        <div>
          <h2>✅ Connected! Found {events.length} events:</h2>
          {events.map(event => (
            <div key={event.id} style={{ 
              padding: '15px', 
              margin: '10px 0', 
              background: '#1a1a1f',
              borderRadius: '8px',
              borderLeft: '4px solid #4ade80'
            }}>
              <h3>{event.title}</h3>
              <p>Type: {event.event_type} | Severity: {event.severity}</p>
              <p>Location: {event.location.name} ({event.location.latitude}, {event.location.longitude})</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
