from pydantic import BaseModel, EmailStr, ValidationInfo, field_validator


class RegisterForm(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    name: str

    @field_validator("confirm_password", mode="after")
    def password_match(cls, value, info: ValidationInfo):
        password = info.data.get("password")
        if not password == value:
            raise ValueError("Passwords do not match.")
        return value
