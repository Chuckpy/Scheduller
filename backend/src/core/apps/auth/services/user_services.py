from core.models import User
from core.schemas.user_schema import (
    Token,
    UserRegisterSchema,
    UserLoginSchema,
    UserUpdateSchema,
)
from database.db import get_session
from core.models.base_mixins import BaseMixin
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends, Header
from jose import JWTError, ExpiredSignatureError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic, selectin_polymorphic


class UserController:

    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALGORITHM = "HS256"
    model = User
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "6c924ef1d5432c1864b242c769b41edbe342ffd040b066c4b69dbe673af645d0"

    def _create_access_token(self, data: dict) -> str:

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encoded_jwt

    def _verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def _find_user_by_username(self, username):

        manager_poly = with_polymorphic(BaseMixin, [User])
        db_user = (
            self.session.query(User)
            .options(selectin_polymorphic(User, [manager_poly]))
            .filter(User.username == username)
            .first()
        )

        if db_user:
            return db_user

        raise HTTPException(status_code=400, detail="Incorrect username or password")

    def _get_user_by_username(self, username):
        return (
            self.session.query(self.model)
            .filter(self.model.username == username)
            .first()
        )

    def _create_access_token(self) -> str:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        db_user = self._get_user_by_username(self.form_data.username)
        if not db_user:
            raise credentials_exception

        if not self._verify_password(
            self.form_data.hashed_password, db_user.hashed_password
        ):
            raise credentials_exception

        form_data = self.form_data.dict()
        form_data.pop("hashed_password")
        to_encode = form_data
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return Token(token_type="Bearer", access_token=encoded_jwt)

    def _get_user_by_email(self, email):
        return self.session.query(self.model).filter(self.model.email == email).first()

    def _get_user(self, token: str) -> User | None:

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("username", False)

            if username is None:
                raise credentials_exception

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Signature expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        except JWTError:
            raise credentials_exception

        user = self._find_user_by_username(username)

        return user


class UserToken(UserController):
    def __init__(
        self,
        authorization: str | None = Header(),
        session: Session = Depends(get_session),
    ):

        self.authorization = authorization.split(" ")[1]
        self.session = session

    def get_user(self):
        return super()._get_user(self.authorization)

    @property
    def user(self):
        return self.get_user()


class UserUpdate(UserController):
    def __init__(
        self,
        form_data: UserUpdateSchema,
        authorization: str | None = Header(),
        session: Session = Depends(get_session),
    ):

        self.authorization = authorization.split(" ")[1]
        self.session = session
        self.form_data = form_data

    def update_user(self):
        user = self._get_user(self.authorization)
        self.session.query(self.model).filter(
            self.model.username == user.username
        ).update(self.form_data.dict(exclude_none=True))
        return self._get_user(self.authorization)


class UserLogin(UserController):
    def __init__(
        self,
        form_data: UserLoginSchema,
        session: Session = Depends(get_session),
    ):

        self.form_data = form_data
        self.session = session

    def get_access_token(self) -> str:
        return self._create_access_token()


class UserRegister(UserController):
    def __init__(
        self,
        form_data: UserRegisterSchema,
        session: Session = Depends(get_session),
    ):

        self.form_data = form_data
        self.session = session

    def create_user(self):

        if self._get_user_by_username(
            self.form_data.username
        ) or self._get_user_by_email(self.form_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already in use",
                headers={"WWW-Authenticate": "Bearer"},
            )

        serialized_data = self.form_data.dict(exclude_none=True)
        serialized_data["hashed_password"] = self._get_password_hash(
            serialized_data["hashed_password"]
        )

        db_user = self.model(**serialized_data)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return db_user
