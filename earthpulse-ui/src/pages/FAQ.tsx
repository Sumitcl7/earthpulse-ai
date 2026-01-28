import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { FAQS } from "../data/faqData";

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <>
      <div style={{ minHeight: "100vh", background: "#000", paddingTop: "80px" }}>
        <Navbar />

        <div style={{ maxWidth: "900px", margin: "0 auto", padding: "60px 20px" }}>
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            style={{ textAlign: "center", marginBottom: "60px" }}
          >
            <h1
              style={{
                fontSize: "clamp(40px, 6vw, 56px)",
                fontWeight: 700,
                marginBottom: "16px",
                letterSpacing: "-1px",
              }}
            >
              Frequently Asked Questions
            </h1>
            <p
              style={{
                fontSize: "18px",
                opacity: 0.7,
                maxWidth: "600px",
                margin: "0 auto",
                lineHeight: 1.6,
              }}
            >
              Everything you need to know about EarthPulse AI
            </p>
          </motion.div>

          {/* FAQ Items */}
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            {FAQS.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.05 }}
                style={{
                  background: "rgba(255,255,255,0.03)",
                  border: "1px solid rgba(255,255,255,0.08)",
                  borderRadius: "12px",
                  overflow: "hidden",
                  transition: "all 0.3s ease",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = "rgba(255,255,255,0.05)";
                  e.currentTarget.style.borderColor = "rgba(255,255,255,0.15)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = "rgba(255,255,255,0.03)";
                  e.currentTarget.style.borderColor = "rgba(255,255,255,0.08)";
                }}
              >
                {/* Question */}
                <button
                  onClick={() => toggleFAQ(index)}
                  style={{
                    width: "100%",
                    padding: "24px 28px",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    background: "transparent",
                    border: "none",
                    color: "#fff",
                    textAlign: "left",
                    cursor: "pointer",
                  }}
                >
                  <span
                    style={{
                      fontSize: "18px",
                      fontWeight: 600,
                      flex: 1,
                      paddingRight: "20px",
                    }}
                  >
                    {faq.q}
                  </span>
                  <motion.span
                    animate={{ rotate: openIndex === index ? 45 : 0 }}
                    transition={{ duration: 0.3 }}
                    style={{
                      fontSize: "28px",
                      fontWeight: 300,
                      opacity: 0.6,
                      lineHeight: 1,
                    }}
                  >
                    +
                  </motion.span>
                </button>

                {/* Answer */}
                <AnimatePresence>
                  {openIndex === index && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                      style={{ overflow: "hidden" }}
                    >
                      <div
                        style={{
                          padding: "0 28px 24px 28px",
                          fontSize: "16px",
                          lineHeight: 1.7,
                          opacity: 0.8,
                          borderTop: "1px solid rgba(255,255,255,0.05)",
                          paddingTop: "20px",
                        }}
                      >
                        {faq.a}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            ))}
          </div>

          {/* CTA Section */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            style={{
              marginTop: "80px",
              textAlign: "center",
              padding: "50px 30px",
              background: "rgba(26, 115, 232, 0.08)",
              borderRadius: "16px",
              border: "1px solid rgba(26, 115, 232, 0.2)",
            }}
          >
            <h3 style={{ fontSize: "28px", marginBottom: "16px", fontWeight: 600 }}>
              Ready to explore?
            </h3>
            <p style={{ fontSize: "16px", opacity: 0.7, marginBottom: "28px" }}>
              Start analyzing environmental data with EarthPulse AI
            </p>
            <button
              onClick={() => (window.location.href = "/dashboard")}
              style={{
                padding: "14px 32px",
                borderRadius: 999,
                background: "#1a73e8",
                color: "white",
                fontSize: "16px",
                fontWeight: 600,
                border: "none",
                cursor: "pointer",
                transition: "all 0.3s",
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
          </motion.div>
        </div>
      </div>

      <Footer />
    </>
  );
}