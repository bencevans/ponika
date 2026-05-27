from ponika.models import BaseModel


class UploadFileResponse(BaseModel):
    path: str


class DeleteResponse(BaseModel):
    id: str
