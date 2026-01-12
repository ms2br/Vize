from fastapi import APIRouter, HTTPException
from core.recommender import recommend_for_user, all_users

router = APIRouter(
    prefix="/api",
    tags=["Recommendation"]
)

@router.get("/recommend/{user_id}")
def recommend(user_id: int):
    if user_id not in all_users:
        raise HTTPException(
            status_code=404,
            detail="Geçersiz kullanıcı ID"
        )

    return {
        "user_id": user_id,
        "recommendations": recommend_for_user(user_id)
    }
