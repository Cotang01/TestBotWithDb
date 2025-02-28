from aiogram import Router
from handlers.ikb_handler import router as ikb_router


r_ = Router()

routers = [
    ikb_router,
]

for r in routers:
    r_.include_router(r)