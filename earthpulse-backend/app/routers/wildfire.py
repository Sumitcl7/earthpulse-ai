from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db

router = APIRouter()

@router.get("/")
def get_wildfire_data(db: Session = Depends(get_db)):
    """Get wildfire data"""
    return {"message": "Wildfire data endpoint", "status": "working"}

@router.get("/test")
def test_wildfire():
    """Test endpoint"""
    return {"test": "wildfire router working"}