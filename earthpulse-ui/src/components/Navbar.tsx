import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { motion } from "framer-motion";

export default function Navbar() {
  const [solid, setSolid] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setSolid(window.scrollY > 80);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Dashboard always has solid navbar
  const isAlwaysSolid = location.pathname === "/dashboard";

  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      style={{
        position: "fixed",
        top: 0,
        width: "100%",
        padding: "18px 40px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        background: solid || isAlwaysSolid ? "rgba(0,0,0,0.85)" : "transparent",
        backdropFilter: solid || isAlwaysSolid ? "blur(16px)" : "none",
        borderBottom: solid || isAlwaysSolid ? "1px solid rgba(255,255,255,0.1)" : "none",
        transition: "all 0.3s ease",
        zIndex: 1000,
      }}
    >
      <strong
        style={{
          fontSize: "18px",
          letterSpacing: "0.5px",
          cursor: "pointer",
        }}
        onClick={() => navigate("/")}
      >
        EarthPulse AI
      </strong>

      <div style={{ display: "flex", gap: 32, alignItems: "center" }}>
  <span
    onClick={() => navigate("/")}
    style={{ cursor: "pointer", opacity: 0.85, fontSize: "14px" }}
  >
    Overview
  </span>
  <span
    onClick={() => navigate("/faq")}
    style={{ cursor: "pointer", opacity: 0.85, fontSize: "14px" }}
  >
    FAQ
  </span>
        <button
          onClick={() => navigate("/dashboard")}
          style={{
            background: "#1a73e8",
            color: "white",
            padding: "10px 22px",
            borderRadius: 24,
            fontSize: "14px",
            fontWeight: 600,
            transition: "all 0.2s",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "#1765cc";
            e.currentTarget.style.transform = "translateY(-2px)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "#1a73e8";
            e.currentTarget.style.transform = "translateY(0)";
          }}
        >
          Try Dashboard
        </button>
      </div>
    </motion.nav>
  );
}