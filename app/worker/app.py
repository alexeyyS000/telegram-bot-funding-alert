from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta
from .config import WorkerSettings
from ..parser.main import parse_better_funding_rate
from db.dal.funding import FundingDAL
from db.dal.user import UserDAL
from db.client import get_session
from bot.alerts.main import funding_alert

settings = WorkerSettings()
app = Celery(
    "tasks", backend=settings.celery_result_backend, broker=settings.celery_broker_url
)

app.conf.beat_schedule = {
    "parse": {
        "task": "app.add",
        "schedule": crontab(minute="*/480"),
    },
    "sand_massage": {
        "task": "app.sand",
        "schedule": crontab(minute="*/480"),
    },
}
app.conf.timezone = "Europe/Moscow"


@app.task(name="app.add")
def add():
    with get_session() as session:
        FundingDAL(session).delete_all()
    funding_list = parse_better_funding_rate()
    for i in funding_list:
        with get_session() as session:
            FundingDAL(session).get_or_create(i, symbol=i["symbol"])


@app.task(name="app.sand")
def send():
    with get_session() as session:
        fundings = FundingDAL(session).all()
    immediate_fundings = []
    for i in fundings:
        if i.date_time - datetime.utcnow() <= timedelta(minutes=10):
            immediate_fundings.append(i)
    if immediate_fundings:
        with get_session() as session:
            users = UserDAL(session).filter(subscriber=True).all()
        users_id = []
        for i in users:
            users_id.append(i.id)
        funding_alert(users_id, immediate_fundings)

    # Fundings happen every 4 or 8 hours, so the algorithm starts 10 minutes before the funding,
    # and then checks the subsequent ones every 4 hours
