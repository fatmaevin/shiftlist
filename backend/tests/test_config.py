from app.config import Settings


def test_settings_reads_database_url_from_environment(monkeypatch):
    database_url = "postgresql+psycopg:///shiftlist_test"
    jwt_secret = "test-secret-that-is-at-least-32-characters"

    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.setenv("JWT_SECRET", jwt_secret)

    settings = Settings(_env_file=None)

    assert settings.database_url == database_url
    assert settings.jwt_secret == jwt_secret
