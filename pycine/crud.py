from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas

#region -------------- CRUD USERS --------------

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user == None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user == None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

def check_for_existing_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def del_users(db: Session, id: int = 0):
    user = get_user(db=db, user_id=id)
    if user == None:
        raise HTTPException(status_code=404, detail="Usuário não existe")
    db.delete(user)
    db.commit()
    return user

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#endregion

#region -------------- CRUD FAVORITES --------------

def get_favorite_movies(db: Session, email: str):
    user = get_user_by_email(db, email)
    return db.query(models.Favorites).filter(models.Favorites.idUser == user.id).all()

def get_favorite_movies_with_idMovie(db: Session, idUser: int, idMovie: int):
    user = get_user(db, idUser)
    return db.query(models.Favorites).filter(models.Favorites.idUser == user.id, models.Favorites.idMovie == idMovie).first()

def favorite_movies(db: Session, idUser: int, idMovie: int):
    check_if_favorite_exists(db=db, idUser=idUser, idMovie=idMovie)
    user = get_user(db, idUser)
    db_favorite = models.Favorites(idUser=user.id, idMovie=idMovie)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def delete_favorite_movie(db: Session, idUser: int, idMovie: int):
    favoriteMovie = get_favorite_movies_with_idMovie(db=db, idUser=idUser, idMovie=idMovie)
    if favoriteMovie == None:
        raise HTTPException(status_code=404, detail="Filme ou usuário não encontrado nos favoritos.")
    db.delete(favoriteMovie)
    db.commit()
    return favoriteMovie

def check_if_favorite_exists(db: Session, idUser: int, idMovie: int):
    favoriteExist = get_favorite_movies_with_idMovie(db=db, idUser=idUser, idMovie=idMovie)
    if favoriteExist != None:
        raise HTTPException(status_code=409, detail="O usuário já possui este filme em seus favoritos.")

#endregion

#region -------------- CRUD PEOPLE --------------

def get_favorite_people(db: Session, email: str):
    user = get_user_by_email(db, email)
    return db.query(models.FavoritePeople).filter(models.FavoritePeople.idUser == user.id).all()

def get_favorite_person_with_idPerson(db: Session, idUser: int, idPerson: int):
    user = get_user(db, idUser)
    return db.query(models.FavoritePeople).filter(models.FavoritePeople.idUser == user.id, models.FavoritePeople.idPerson == idPerson).first()

def favorite_person(db: Session, idUser: int, idPerson: int):
    check_if_favorite_person_exists(db=db, idUser=idUser, idPerson=idPerson)
    user = get_user(db, idUser)
    db_favorite = models.FavoritePeople(idUser=user.id, idPerson=idPerson)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def delete_favorite_person(db: Session, idUser: int, idPerson: int):
    favoritePerson = get_favorite_person_with_idPerson(db=db, idUser=idUser, idPerson=idPerson)
    if favoritePerson == None:
        raise HTTPException(status_code=404, detail="Ator ou usuário não encontrado nos favoritos.")
    db.delete(favoritePerson)
    db.commit()
    return favoritePerson

def check_if_favorite_person_exists(db: Session, idUser: int, idPerson: int):
    favoriteExist = get_favorite_person_with_idPerson(db=db, idUser=idUser, idPerson=idPerson)
    if favoriteExist != None:
        raise HTTPException(status_code=409, detail="O usuário já possui este ator em seus favoritos.")
#endregion