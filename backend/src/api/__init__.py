from dataclasses import dataclass
from typing import Optional

from flask import Response, jsonify


@dataclass
class APIResponse:
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None


def success_response(
    message: Optional[str] = None, data: Optional[dict] = None
) -> APIResponse:
    return APIResponse(success=True, message=message, data=data)


def success_json(
    message: Optional[str] = None, data: Optional[dict] = None
) -> tuple[Response, int]:
    return jsonify(success_response(message, data)), 200


def error_response(message: str) -> APIResponse:
    return APIResponse(success=False, message=message)


def error_json(message, status_code: int = 400) -> tuple[Response, int]:
    return jsonify(error_response(message)), status_code
