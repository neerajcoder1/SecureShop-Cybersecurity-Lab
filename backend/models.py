from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordReset(BaseModel):
    username: str
    email: str

class ProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class TicketUpdate(BaseModel):
    status: str
    message: str

class Checkout(BaseModel):
    product_id: int
    quantity: int
    total_price: float

class EmailUpdate(BaseModel):
    email: EmailStr
    csrf_token: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int

class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    status: str

class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=500)

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str]

class Challenge(BaseModel):
    id: int
    title: str
    description: str
    hint: str
    difficulty: str
    xp: int = 50
    completed: bool = False

class LabConfig(BaseModel):
    id: str
    name: str
    description: str
    category: str
    difficulty: str
    xp_available: int
    challenges_count: int
    completed_challenges: int = 0
    progress_percentage: int = 0
    status: str = "Online"

class ChallengeSubmit(BaseModel):
    lab_id: str
    challenge_id: int
    flag: str

class ChallengeResponse(BaseModel):
    success: bool
    message: str
    xp_awarded: int = 0
    badge_awarded: Optional[str] = None
