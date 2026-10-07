from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

from prometheus_client import make_asgi_app
from metrics import TICKETS_CREATED

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HelpDesk API")


# Endpoint для Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Контракт. Создание обращения
@app.post("/api/v1/tickets", response_model=schemas.TicketResponse)
def create_ticket(
    ticket: schemas.TicketCreate,
    db: Session = Depends(get_db)
):
    db_ticket = models.Ticket(
        client_id=ticket.client_id,
        category_code=ticket.category_code,
        description=ticket.description
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    TICKETS_CREATED.labels(
        category=ticket.category_code
    ).inc()

    return db_ticket

# API Контракт. Получение списка обращений
@app.get("/api/v1/tickets", response_model=list[schemas.TicketResponse])
def get_tickets(offset: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).offset(offset).limit(limit).all()
    return tickets