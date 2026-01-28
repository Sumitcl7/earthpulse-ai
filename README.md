# 🌍 EarthPulse AI

**Environmental Event Monitoring System with Real-Time Satellite Analysis**

Monitor wildfires, floods, deforestation, and droughts worldwide using AI-powered satellite imagery analysis from Google Earth Engine.

---

## 🚀 Features

- 🗺️ **Interactive Global Map** - Real-time visualization of environmental events
- 🛰️ **Satellite Verification** - Verify events using Google Earth Engine data
  - NDVI analysis for vegetation health
  - Thermal detection for wildfires
  - Water body detection for floods
- 📰 **News Scraping** - Import environmental news automatically
- 📊 **Statistics Dashboard** - Track events by type and severity
- ✅ **Event Verification** - AI-powered confidence scoring

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Database ORM
- **Google Earth Engine** - Satellite imagery analysis
- **SQLite** - Database

### Frontend
- **React** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Mapbox GL** - Interactive mapping
- **Framer Motion** - Smooth animations
- **Vite** - Fast build tool

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Earth Engine account

### Backend Setup

\\\ash
cd earthpulse-backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your Google Earth Engine credentials
# Place earthpulse-472111-*.json in project root

# Run server
uvicorn app.main:app --reload
\\\

Backend runs on: http://localhost:8000

### Frontend Setup

\\\ash
cd earthpulse-ui

# Install dependencies
npm install

# Run development server
npm run dev
\\\

Frontend runs on: http://localhost:5173

---

## 🌐 API Endpoints

### Events
- \GET /api/events\ - Get all events
- \POST /api/events/create\ - Create new event
- \POST /api/events/{id}/verify\ - Verify event with satellite data

### Satellite Analysis
- \GET /api/satellite/ndvi\ - Get NDVI data
- \GET /api/satellite/wildfire\ - Detect wildfires
- \GET /api/satellite/water\ - Detect water bodies

### News
- \GET /api/news/scrape\ - Scrape environmental news
- \POST /api/news/import/{index}\ - Import news as event

### Authentication
- \POST /api/auth/register\ - Register new user
- \POST /api/auth/login\ - Login user
- \GET /api/auth/me\ - Get current user

---

## 📸 Screenshots

[Add screenshots here]

---

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes.

---

## 👨‍💻 Author

Built with ❤️ by **@Sumitcl7**

---

## 🙏 Acknowledgments

- Google Earth Engine for satellite data
- Mapbox for mapping infrastructure
- OpenStreetMap contributors
