from pydantic import BaseModel
from typing import Optional


class ScrapperRequest(BaseModel):
    page:Optional[int]=None
    search_string:Optional[str]=None
    