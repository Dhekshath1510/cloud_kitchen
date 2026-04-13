import uuid
from sqlalchemy.orm import Session
from app.repository.user_repository import UserRepository
from app.models.domain import User, Role
from app.schemas.domain import NewUserDto, UserLoginDto, AuthResponse
from app.core.security import get_password_hash, verify_password, create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(self, dto: NewUserDto) -> User:
        # Check if user already exists
        if self.user_repo.get_by_email(dto.emailId):
            raise ValueError("Email already configured")
        if self.user_repo.get_by_username(dto.userName):
            raise ValueError("Username already taken")

        # Create new user
        new_user = User(
            user_id=str(uuid.uuid4()),
            user_name=dto.userName,
            email=dto.emailId,
            password=get_password_hash(dto.password),
            role=dto.role
        )
        return self.user_repo.create(new_user)

    def authenticate_user(self, dto: UserLoginDto) -> str:
        user = self.user_repo.get_by_username(dto.userName)
        if not user:
            raise ValueError("Invalid username or password")
        
        if not verify_password(dto.password, user.password):
            raise ValueError("Invalid username or password")
            
        if user.role != dto.role:
            raise ValueError("Invalid role specified for this user")

        # Create token
        access_token = create_access_token(data={"sub": user.user_name, "role": user.role.value})
        return access_token
