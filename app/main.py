from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import database, models, schemas, crud, auth, classifier, utils
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Grievance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    # create tables
    database.Base.metadata.create_all(bind=database.engine)

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    created = crud.create_user(db, user)
    return created

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# simplified dependency to get current user from token (production: use OAuth2PasswordBearer + more checks)
from jose import jwt, JWTError

def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    # For simplicity this function will be replaced by a real auth dependency if using OAuth2PasswordBearer
    raise HTTPException(status_code=501, detail="Implement proper token auth in production")

# Grievance submit endpoint (no auth for demo — recommend requiring auth)
@app.post("/grievances", response_model=schemas.GrievanceOut)
async def submit_grievance(
    title: str = Form(...),
    description: str = Form(...),
    user_id: int = Form(...),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    attachment_path = None
    if file:
        attachment_path = utils.save_upload_file(file)
    # call classifier
    category, score = classifier.predict_category(description)
    gr = crud.create_grievance(db, user_id=user_id, grievance=schemas.GrievanceCreate(title=title, description=description), category=category, attachment_path=attachment_path)
    return gr

@app.get("/grievances/{g_id}", response_model=schemas.GrievanceOut)
def get_grievance(g_id: int, db: Session = Depends(get_db)):
    g = crud.get_grievance(db, g_id)
    if not g:
        raise HTTPException(status_code=404, detail="Not found")
    return g

@app.get("/users/{user_id}/grievances", response_model=list[schemas.GrievanceOut])
def list_user_grievances(user_id: int, db: Session = Depends(get_db)):
    return crud.list_grievances_for_user(db, user_id)
