from pydantic import BaseModel


class Config(BaseModel):
    discord_webhook_url: str | None = None
