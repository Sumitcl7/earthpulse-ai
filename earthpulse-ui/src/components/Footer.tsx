import { motion } from "framer-motion";

export default function Footer() {
  return (
    <footer
      style={{
        padding: "50px 40px",
        textAlign: "center",
        background: "#000",
        borderTop: "1px solid rgba(255,255,255,0.05)",
      }}
    >
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <p style={{ fontSize: "13px", opacity: 0.5, marginBottom: "8px" }}>
          © 2025 EarthPulse AI · All rights reserved.
        </p>
        <p style={{ fontSize: "12px", opacity: 0.3 }}>
          Powered by Satellite Data & AI
        </p>
      </motion.div>
    </footer>
  );
}