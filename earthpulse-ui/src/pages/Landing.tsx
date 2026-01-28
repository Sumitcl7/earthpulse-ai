import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <>
      {/* Hero Section */}
      <div style={{ position: "relative", height: "100vh", overflow: "hidden" }}>
        <Navbar />

        {/* Background Video */}
        <video
          autoPlay
          muted
          loop
          playsInline
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            zIndex: 1,
          }}
        >
          <source src="/hero.mp4" type="video/mp4" />
        </video>

        {/* Gradient Overlay */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background:
              "linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.85))",
            zIndex: 2,
          }}
        />

        {/* Hero Content */}
        <div
          style={{
            position: "relative",
            zIndex: 3,
            height: "100%",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            textAlign: "center",
            padding: "0 20px",
          }}
        >
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            style={{
              fontSize: "clamp(48px, 8vw, 72px)",
              fontWeight: 700,
              marginBottom: "20px",
              letterSpacing: "-1px",
            }}
          >
            EarthPulse AI
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            style={{
              fontSize: "clamp(16px, 2vw, 20px)",
              opacity: 0.85,
              maxWidth: "650px",
              lineHeight: 1.6,
              marginBottom: "40px",
            }}
          >
            Planet-scale environmental intelligence powered by satellite data.
            Monitor deforestation, track climate change, and analyze Earth's health
            in real-time.
          </motion.p>

          <motion.button
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate("/dashboard")}
            style={{
              padding: "16px 36px",
              borderRadius: 999,
              background: "#1a73e8",
              color: "white",
              fontSize: "16px",
              fontWeight: 600,
              boxShadow: "0 8px 24px rgba(26, 115, 232, 0.3)",
              transition: "all 0.3s ease",
            }}
          >
            EXPLORE DASHBOARD
          </motion.button>
        </div>
      </div>

      {/* Features Section */}
      <section
        style={{
          padding: "100px 40px",
          background: "linear-gradient(to bottom, #000, #0a0a0a)",
        }}
      >
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          style={{
            maxWidth: "1200px",
            margin: "0 auto",
            textAlign: "center",
          }}
        >
          <h2
            style={{
              fontSize: "clamp(32px, 5vw, 48px)",
              marginBottom: "60px",
              fontWeight: 600,
            }}
          >
            Satellite-Powered Insights
          </h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
              gap: "40px",
            }}
          >
            {[
              {
                title: "NDVI Analysis",
                desc: "Track vegetation health and deforestation patterns over time",
              },
              {
                title: "Real-Time Monitoring",
                desc: "Live satellite data from NASA and ESA missions",
              },
              {
                title: "AI-Powered Insights",
                desc: "Machine learning models predict environmental changes",
              },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: i * 0.2 }}
                viewport={{ once: true }}
                style={{
                  padding: "30px",
                  background: "rgba(255,255,255,0.03)",
                  borderRadius: "12px",
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <h3 style={{ fontSize: "22px", marginBottom: "12px" }}>
                  {feature.title}
                </h3>
                <p style={{ opacity: 0.7, fontSize: "15px", lineHeight: 1.6 }}>
                  {feature.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </section>

      <Footer />
    </>
  );
}