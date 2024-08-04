from fastapi import FastAPI
from pathlib import Path, PurePath
from typing import Optional


def routers(app: Optional[FastAPI] = None):
    """
    Dynamic load routers
    """
    router_path = Path.cwd().joinpath("routers")
    routers = [
        f"{item.stem}"
        for item in Path(router_path).iterdir()
        if item.is_file()
        and item.suffix == ".py"
        and not item.stem.startswith("_init_")
    ]
    exec(f"from routers import {', '.join(routers)}")
    if app:
        for router in routers:
            app.include_router(eval(f"{router}.router"))
