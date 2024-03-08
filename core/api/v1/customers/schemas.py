from ninja import Schema


class LogInSchema(Schema):
    phone: str


class LogOutSchema(Schema):
    message: str


class ConfirmInSchema(Schema):
    phone: str
    code: str


class ConfirmOutSchema(Schema):
    phone: str
    token: str
