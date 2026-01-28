import { useNavigate, useLocation } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        height: '60px',
        background: 'rgba(0, 0, 0, 0.3)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 40px',
        zIndex: 1000,
      }}
    >
      <div
        onClick={() => navigate('/')}
        style={{
          fontSize: '24px',
          fontWeight: 700,
          cursor: 'pointer',
          color: 'white',
        }}
      >
         EarthPulse AI
      </div>

      <div style={{ display: 'flex', gap: '32px', alignItems: 'center' }}>
        <a
          onClick={() => navigate('/')}
          style={{
            color: isActive('/') ? 'white' : 'rgba(255,255,255,0.7)',
            textDecoration: 'none',
            fontSize: '15px',
            fontWeight: isActive('/') ? 600 : 400,
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.color = 'white';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.color = isActive('/') ? 'white' : 'rgba(255,255,255,0.7)';
          }}
        >
          Overview
        </a>
        <a
          onClick={() => navigate('/dashboard')}
          style={{
            color: isActive('/dashboard') ? 'white' : 'rgba(255,255,255,0.7)',
            textDecoration: 'none',
            fontSize: '15px',
            fontWeight: isActive('/dashboard') ? 600 : 400,
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.color = 'white';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.color = isActive('/dashboard') ? 'white' : 'rgba(255,255,255,0.7)';
          }}
        >
          Dashboard
        </a>
        <a
          onClick={() => navigate('/news')}
          style={{
            color: isActive('/news') ? 'white' : 'rgba(255,255,255,0.7)',
            textDecoration: 'none',
            fontSize: '15px',
            fontWeight: isActive('/news') ? 600 : 400,
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.color = 'white';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.color = isActive('/news') ? 'white' : 'rgba(255,255,255,0.7)';
          }}
        >
          News
        </a>
        <a
          onClick={() => navigate('/faq')}
          style={{
            color: isActive('/faq') ? 'white' : 'rgba(255,255,255,0.7)',
            textDecoration: 'none',
            fontSize: '15px',
            fontWeight: isActive('/faq') ? 600 : 400,
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.color = 'white';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.color = isActive('/faq') ? 'white' : 'rgba(255,255,255,0.7)';
          }}
        >
          FAQ
        </a>

        <button
          onClick={() => navigate('/dashboard')}
          style={{
            padding: '12px 28px',
            background: '#1a73e8',
            border: 'none',
            borderRadius: '24px',
            color: 'white',
            fontSize: '15px',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'all 0.2s',
            boxShadow: '0 4px 12px rgba(26, 115, 232, 0.3)',
            textTransform: 'uppercase',
            letterSpacing: '0.5px',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#1557b0';
            e.currentTarget.style.transform = 'translateY(-2px)';
            e.currentTarget.style.boxShadow = '0 6px 16px rgba(26, 115, 232, 0.4)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = '#1a73e8';
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 4px 12px rgba(26, 115, 232, 0.3)';
          }}
        >
           Dashboard
        </button>
      </div>
    </nav>
  );
}