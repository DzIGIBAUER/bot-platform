import uuid
from django.contrib.auth import get_user_model
from django.db import models

from langchain.schema import BaseMessage

User = get_user_model()

class Chatbot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Name", max_length=30)
    voice_name = models.CharField("Voice name", max_length=20)
    behaviour = models.TextField("Behaviour")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} ({self.user.get_username()})"
    
    def generate_response(self, input: str, user: str | None = None, history: list[BaseMessage] | None = None):
        from common.langchain_utils import generate_response

        return generate_response(self, input, history=history, user=user)
