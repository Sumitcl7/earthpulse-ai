#  EarthPulse AI

**Environmental Event Monitoring System with Real-Time Satellite Analysis**

Monitor wildfires, floods, deforestation, and droughts worldwide using AI-powered satellite imagery analysis from Google Earth Engine.

---

##  Features

-  **Interactive Global Map** - Real-time visualization of environmental events
-  **Satellite Verification** - Verify events using Google Earth Engine data
  - NDVI analysis for vegetation health
  - Thermal detection for wildfires
  - Water body detection for floods
-  **News Scraping** - Import environmental news automatically
-  **Statistics Dashboard** - Track events by type and severity
-  **Event Verification** - AI-powered confidence scoring

---

##  Tech Stack

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

##  Installation

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

##  API Endpoints

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

##  Screenshots
**Landing**
<img width="1919" height="1078" alt="image" src="https://github.com/user-attachments/assets/157fb05d-1e37-4b1a-8c5a-94ad69aeba7c" />

**Dashboard**
<img width="1919" height="1079" alt="Screenshot 2026-02-12 221138" src="https://github.com/user-attachments/assets/30212288-f251-4d86-88c2-7310a91582bd" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/1f1ab3c6-c36b-4b4e-8c16-0f2d0241b47a" />

**News**
<img width="1919" height="1077" alt="image" src="https://github.com/user-attachments/assets/5605ca3d-e043-4b28-82f6-16089ef156f6" />

**FAQ**
<img width="1919" height="933" alt="image" src="https://github.com/user-attachments/assets/2f83bf70-eb02-4436-aed7-38d2a52155ea" />





---

##  Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

##  License

MIT License - feel free to use this project for learning or commercial purposes.

---

##  Author

 **@Sumitcl7**

---

##  Acknowledgments

- Google Earth Engine for satellite data
- Mapbox for mapping infrastructure
- OpenStreetMap contributors

## Important 
Currently the GEE pipline is getting issues due to Payment issues and some technical backend glitches.So, the backend is currently running on 160 sample data.
I am still fixing things and working on that,But good news is News SCraper pipeline is working perfectly.The full project working will be Live for next month till then you are free to contribute and help


