from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db

router = APIRouter()

@router.get("/")
def get_forest_data(db: Session = Depends(get_db)):
    """Get forest data"""
    return {"message": "Forest data endpoint", "status": "working"}

@router.get("/test")
def test_forest():
    """Test endpoint"""
    return {"test": "forest router working"}