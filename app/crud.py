from . import models , schemas
from sqlalchemy.orm import Session

def create_user(db: Session, user: schemas.UserCreate):
    # 1. Map Schema -> Model
    db_user = models.User(
        name = user.name,
        email = user.email,
        password = user.password
    )
    # 2. Stage and Commit
    db.add(db_user)
    db.commit()

    db.refresh(db_user)
    return db_user
