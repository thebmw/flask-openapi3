# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/6/6 14:05

from typing import Optional

from pydantic import BaseModel, Field

from flask_openapi3 import APIBlueprint, OpenAPI
from flask_openapi3.models import Tag, Info
from flask_openapi3.models.security import HTTPBearer

info = Info(title='book API', version='1.0.0')
securitySchemes = {"jwt": HTTPBearer(bearerFormat="JWT")}

app = OpenAPI(__name__, info=info, securitySchemes=securitySchemes)

security = [{"jwt": []}]
api = APIBlueprint('/book', __name__, url_prefix='/api', abp_security=security)

tag = Tag(name='book', description="图书")


class BookData(BaseModel):
    age: Optional[int] = Field(..., ge=2, le=4, description='年龄')
    author: str = Field(None, min_length=2, max_length=4, description='作者')


class Path(BaseModel):
    bid: int = Field(..., description='图书id')


@api.post('/book', tags=[tag])
def create_book(body: BookData):
    assert body.age == 3
    return {"code": 0, "message": "ok"}


@api.put('/book/<int:bid>', tags=[tag])
def update_book(path: Path, body: BookData):
    assert path.bid == 1
    assert body.age == 3
    return {"code": 0, "message": "ok"}


# register api
app.register_api(api)

if __name__ == '__main__':
    app.run(debug=True)
