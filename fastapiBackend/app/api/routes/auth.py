from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.domain import NewUserDto, UserLoginDto, AuthResponse, ExceptionResponse
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Auth"])

@router.post("/register")
def register(dto: NewUserDto, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    try:
        user = auth_service.register_user(dto)
        return {"success": "User registered successfully", "userId": user.user_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/logout")
def logout():
    return {"success": True}

@router.post("/login", response_model=AuthResponse)
def login(dto: UserLoginDto, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    try:
        token = auth_service.authenticate_user(dto)
        # Note: we will return empty string for refreshToken for now, or you can supply it similarly
        return AuthResponse(accessToken=token, refreshToken="", role=dto.role)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

# Added for FastAPI Swagger UI compatibility
@router.post("/login_swagger", include_in_schema=False)
def login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user_repo = auth_service.user_repo
    user = user_repo.get_by_username(form_data.username)
    if not user:
         raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # We map form_data to UserLoginDto. Note role must be handled. Assuming USER for swagger.
    from app.models.domain import Role
    try:
        token = auth_service.authenticate_user(UserLoginDto(userName=user.user_name, password=form_data.password, role=user.role))
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
