import { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import Navbar from "../components/Navbar";
import { motion } from "framer-motion";

// 🔑 Replace with your Mapbox token
mapboxgl.accessToken = "pk.eyJ1Ijoic3VtZGV2czEiLCJhIjoiY21oNTV5dHg4MDNsMDJycjBhY3NjcWVlciJ9.zj7lBK4wXxHLD8ChLJxztA";

export default function Dashboard() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [year, setYear] = useState(2024);

  useEffect(() => {
    if (!mapContainer.current) return;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/satellite-streets-v12",
      center: [-61.5, -8.5], // Amazon Rainforest
      zoom: 4.5,
      pitch: 45,
    });

    map.current.addControl(new mapboxgl.NavigationControl(), "top-right");

    return () => {
      map.current?.remove();
    };
  }, []);

  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      <Navbar />

      <div style={{ flex: 1, display: "flex", marginTop: "60px" }}>
        {/* Map Container */}
        <div ref={mapContainer} style={{ flex: 1 }} />

        {/* Right Panel */}
        <motion.div
          initial={{ x: 100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.6 }}
          style={{
            width: "400px",
            background: "rgba(10, 10, 15, 0.95)",
            backdropFilter: "blur(20px)",
            borderLeft: "1px solid rgba(255,255,255,0.1)",
            padding: "30px",
            overflowY: "auto",
          }}
        >
          <h2 style={{ fontSize: "24px", marginBottom: "20px", fontWeight: 600 }}>
            Amazon Rainforest
          </h2>

          <div
            style={{
              padding: "16px",
              background: "rgba(255,255,255,0.05)",
              borderRadius: "8px",
              marginBottom: "24px",
            }}
          >
            <div style={{ fontSize: "13px", opacity: 0.6, marginBottom: "8px" }}>
              NDVI INDEX
            </div>
            <div style={{ fontSize: "32px", fontWeight: 700, color: "#4ade80" }}>
              0.68
            </div>
            <div style={{ fontSize: "12px", opacity: 0.5 }}>
              Moderate vegetation health
            </div>
          </div>

          <h3 style={{ fontSize: "16px", marginBottom: "16px", opacity: 0.9 }}>
            Recent Updates
          </h3>

          {[
            { title: "Deforestation Alert", date: "2 days ago", severity: "high" },
            { title: "Vegetation Recovery", date: "1 week ago", severity: "low" },
            { title: "Fire Detection", date: "2 weeks ago", severity: "critical" },
          ].map((item, i) => (
            <div
              key={i}
              style={{
                padding: "14px",
                background: "rgba(255,255,255,0.03)",
                borderRadius: "8px",
                marginBottom: "12px",
                borderLeft: `3px solid ${
                  item.severity === "critical"
                    ? "#ef4444"
                    : item.severity === "high"
                    ? "#f59e0b"
                    : "#22c55e"
                }`,
              }}
            >
              <div style={{ fontSize: "14px", fontWeight: 500 }}>{item.title}</div>
              <div style={{ fontSize: "12px", opacity: 0.5, marginTop: "4px" }}>
                {item.date}
              </div>
            </div>
          ))}
        </motion.div>
      </div>

      {/* Timeline Scrubber */}
      <motion.div
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        style={{
          position: "absolute",
          bottom: 30,
          left: "50%",
          transform: "translateX(-50%)",
          width: "calc(100% - 480px)",
          maxWidth: "800px",
          background: "rgba(0,0,0,0.85)",
          backdropFilter: "blur(20px)",
          padding: "20px 30px",
          borderRadius: "16px",
          border: "1px solid rgba(255,255,255,0.1)",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "12px",
          }}
        >
          <span style={{ fontSize: "13px", opacity: 0.6 }}>TIMELINE</span>
          <span style={{ fontSize: "16px", fontWeight: 600 }}>{year}</span>
        </div>

        <input
          type="range"
          min="2015"
          max="2024"
          value={year}
          onChange={(e) => setYear(Number(e.target.value))}
          style={{
            width: "100%",
            accentColor: "#1a73e8",
            cursor: "pointer",
          }}
        />

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginTop: "8px",
            fontSize: "11px",
            opacity: 0.4,
          }}
        >
          <span>2015</span>
          <span>2024</span>
        </div>
      </motion.div>
    </div>
  );
}