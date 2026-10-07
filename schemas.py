from pydantic import BaseModel

# Шаблон того, что ждем от клиента 
class TicketCreate(BaseModel):
    client_id: str
    category_code: str
    description: str

# Шаблон того, что отдаем обратно 
class TicketResponse(BaseModel):
    id: str
    status: str

    class Config:
        from_attributes = True # преобразовывать данные из БД в JSON
     