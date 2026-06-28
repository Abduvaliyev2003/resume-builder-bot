from aiogram import Router

from .handlers.menu import router as menu_router
from .handlers.create import router as create_router
from .handlers.list import router as list_router
from .handlers.detail import router as detail_router
from .handlers.edit import router as edit_router
from .handlers.delete import router as delete_router
from .handlers.export import router as export_router

router = Router(name="resume")

router.include_router(menu_router)
router.include_router(list_router)
router.include_router(create_router)
router.include_router(detail_router)
router.include_router(edit_router)
router.include_router(delete_router)
router.include_router(export_router)