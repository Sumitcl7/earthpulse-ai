import { useState } from 'react';
import Navbar from '../components/Navbar';
import { motion } from 'framer-motion';

export default function News() {
  const [news, setNews] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('wildfire OR flood OR deforestation');

  const fetchNews = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/news/scrape?query=${encodeURIComponent(query)}&max_results=20`
      );
      const data = await response.json();
      setNews(data.news);
    } catch (err) {
      console.error('Error fetching news:', err);
    } finally {
      setLoading(false);
    }
  };

  const importAsEvent = async (index: number) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/news/import/${index}`, {
        method: 'POST',
      });
      const result = await response.json();
      alert(`✅ News imported as event #${result.event_id}\n\nGo to Dashboard to see it!`);
    } catch (err) {
      console.error('Error importing news:', err);
      alert('❌ Error importing news');
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#0a0a0f', color: 'white' }}>
      <Navbar />
      
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '100px 20px 40px' }}>
        <motion.div initial={{ y: -20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
          <h1 style={{ fontSize: '48px', marginBottom: '16px', fontWeight: 700 }}>
             Environmental News
          </h1>
          <p style={{ fontSize: '18px', opacity: 0.7, marginBottom: '40px' }}>
            Simulated environmental news feed for demonstration purposes
          </p>

          <div style={{ display: 'flex', gap: '12px', marginBottom: '40px' }}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search news (e.g., wildfire OR flood)"
              style={{
                flex: 1,
                padding: '14px 20px',
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '12px',
                color: 'white',
                fontSize: '16px',
              }}
            />
            <button
              onClick={fetchNews}
              disabled={loading}
              style={{
                padding: '14px 32px',
                background: loading 
                  ? 'rgba(100,100,100,0.3)' 
                  : '#1a73e8',
                border: 'none',
                borderRadius: '12px',
                color: 'white',
                fontSize: '16px',
                fontWeight: 600,
                cursor: loading ? 'wait' : 'pointer',
                transition: 'all 0.2s',
              }}
            >
              {loading ? ' Loading...' : ' Search News'}
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '20px' }}>
            {news.map((item, index) => (
              <motion.div
                key={index}
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: index * 0.05 }}
                style={{
                  padding: '24px',
                  background: 'rgba(255,255,255,0.03)',
                  borderRadius: '12px',
                  border: '1px solid rgba(255,255,255,0.1)',
                  transition: 'all 0.2s',
                  position: 'relative',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(255,255,255,0.06)';
                  e.currentTarget.style.transform = 'translateY(-4px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(255,255,255,0.03)';
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
              >
                <div style={{
                  position: 'absolute',
                  top: '12px',
                  right: '12px',
                  padding: '4px 12px',
                  background: item.event_type === 'wildfire' ? '#ef4444' :
                              item.event_type === 'flood' ? '#3b82f6' :
                              item.event_type === 'deforestation' ? '#22c55e' : '#f59e0b',
                  borderRadius: '6px',
                  fontSize: '11px',
                  fontWeight: 600,
                  textTransform: 'uppercase',
                }}>
                  {item.event_type}
                </div>

                <h3 style={{ fontSize: '18px', marginBottom: '12px', fontWeight: 600, paddingRight: '100px' }}>
                  {item.title}
                </h3>
                <p style={{ fontSize: '14px', opacity: 0.7, marginBottom: '16px', lineHeight: '1.6' }}>
                  {item.description}
                </p>

                <div style={{ fontSize: '12px', opacity: 0.5, marginBottom: '16px' }}>
                  📍 {item.location?.name} • 📅 {new Date(item.published_at).toLocaleDateString()}
                </div>

                <div style={{ fontSize: '12px', opacity: 0.4, marginBottom: '16px', fontStyle: 'italic' }}>
                  Source: {item.source}
                </div>

                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    onClick={() => importAsEvent(index)}
                    style={{
                      flex: 1,
                      padding: '10px 16px',
                      background: 'rgba(34, 197, 94, 0.2)',
                      border: '1px solid #22c55e',
                      borderRadius: '8px',
                      color: '#22c55e',
                      fontSize: '13px',
                      fontWeight: 600,
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = 'rgba(34, 197, 94, 0.3)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'rgba(34, 197, 94, 0.2)';
                    }}
                  >
                    ➕ Import as Event
                  </button>
                </div>
              </motion.div>
            ))}
          </div>

          {news.length === 0 && !loading && (
            <div style={{ textAlign: 'center', padding: '60px 20px', opacity: 0.5 }}>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}></div>
              <p style={{ fontSize: '18px' }}>Click "Search News" to load environmental news</p>
              <p style={{ fontSize: '14px', marginTop: '8px', opacity: 0.6 }}>
                (Demo news for illustration purposes)
              </p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}