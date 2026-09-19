from fastapi import FastAPI

from app.routes.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(title="ShiftList API")

    app.include_router(auth_router)

    @app.get("/api/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
