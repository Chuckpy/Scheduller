from pydantic import BaseModel, EmailStr, validator, Field
from typing import Dict


class UserBaseSchema(BaseModel):
    username: str


class UserLoginSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


class UserRegisterSchema(UserLoginSchema):

    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        orm_mode = True

    @property
    def full_name(self):
        return " ".join([self.first_name, self.last_name])

    """
    Workaround for serializing properties with pydantic until
    https://github.com/samuelcolvin/pydantic/issues/935
    is solved
    """

    @classmethod
    def get_properties(cls):
        return [
            prop for prop in cls.__dict__ if isinstance(cls.__dict__[prop], property)
        ]

    def dict(
        self,
        *,
        include=None,
        exclude=None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> dict:
        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        props = self.get_properties()

        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        if props:
            attribs.update({prop: getattr(self, prop) for prop in props})
        return attribs


class UserSchema(UserBaseSchema):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True

    @property
    def full_name(self):
        return " ".join([self.first_name, self.last_name])

    """
    Workaround for serializing properties with pydantic until
    https://github.com/samuelcolvin/pydantic/issues/935
    is solved
    """

    @classmethod
    def get_properties(cls):
        return [
            prop for prop in cls.__dict__ if isinstance(cls.__dict__[prop], property)
        ]

    def dict(
        self,
        *,
        include=None,
        exclude=None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> dict:
        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        props = self.get_properties()

        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        if props:
            attribs.update({prop: getattr(self, prop) for prop in props})
        return attribs


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None

    @property
    def full_name(self):
        return " ".join([self.first_name, self.last_name])

    """
    Workaround for serializing properties with pydantic until
    https://github.com/samuelcolvin/pydantic/issues/935
    is solved
    """

    @classmethod
    def get_properties(cls):
        return [
            prop for prop in cls.__dict__ if isinstance(cls.__dict__[prop], property)
        ]

    def dict(
        self,
        *,
        include=None,
        exclude=None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> dict:
        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        props = self.get_properties()

        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        if props:
            attribs.update({prop: getattr(self, prop) for prop in props})
        return attribs


class Token(BaseModel):
    token_type: str
    access_token: str
