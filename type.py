from pydantic import BaseModel


class CheckResult(BaseModel):
    translated_percent: str
    approved_percent: str
    words_to_translate: str
    is_there_a_job: bool
