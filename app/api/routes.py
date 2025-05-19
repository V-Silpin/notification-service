from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import TypedDict, List
from db.ops import PostgresDB

router = APIRouter()
db = PostgresDB(
    host='localhost',
    database='notifications_db',
    user='postgres',
    password='postgres',
    port=5432
)

class NotificationRequest(BaseModel):
    uid: str
    body: str

class NotificationResponse(BaseModel):
    id: int
    uid: str
    body: str
    created_at: str

@router.post("/notifications", status_code=201)
async def create_notification(notification: NotificationRequest):
    try:
        # Create notifications table if not exists
        db.create_table(
            table="notifications",
            columns={
                "id": "SERIAL PRIMARY KEY",
                "uid": "VARCHAR(100) NOT NULL",
                "body": "TEXT NOT NULL",
                "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            }
        )
        
        # Insert the notification
        result = db.insert(
            table="notifications",
            data={
                "uid": notification.uid,
                "body": notification.body
            }
        )
        
        if result:
            return {"message": "Notification created successfully", "data": result}
        else:
            raise HTTPException(status_code=500, detail="Failed to create notification")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{uid}/notifications", response_model=List[NotificationResponse])
async def get_user_notifications(uid: str):
    try:
        result = db.select(
            table="notifications",
            conditions={"uid": uid},
            fields=["id", "uid", "body", "created_at"]
        )
        
        if result:
            return result
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))