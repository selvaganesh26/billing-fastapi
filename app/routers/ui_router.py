from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter(tags=["UI"])

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


@router.get("/", response_class=HTMLResponse)
def billing_page():
    """Serve billing page"""
    with open(TEMPLATE_DIR / "billing.html", "r") as f:
        return f.read()


@router.get("/purchases", response_class=HTMLResponse)
def purchases_page():
    """Serve purchase history page"""
    with open(TEMPLATE_DIR / "purchases.html", "r") as f:
        return f.read()
