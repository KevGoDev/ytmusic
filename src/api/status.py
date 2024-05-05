from flask import Blueprint

from api import success_json
from utils.database import db_scope

bp = Blueprint("api", __name__, url_prefix="/api/")


@bp.get("/status")
def get_status():
    with db_scope() as db:
        return success_json(data={"status": "ok"})
