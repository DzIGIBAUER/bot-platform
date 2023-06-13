from typing import OrderedDict
from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from .models import Chatbot

class ChatbotSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Chatbot
        fields = ["id", "name", "voice_name", "behaviour", "user"]
        read_only_fields = ["user"]



class MessageSerializer(serializers.Serializer):
    VALID_TYPES = ["HUMAN", "AI"]
    
    type = serializers.CharField()
    content = serializers.CharField()

    def validate_type(self, value: str) -> str:
        if value.upper() not in self.VALID_TYPES:
            raise serializers.ValidationError(f"Message sender must be on of {self.VALID_TYPES}, got '{value}'")

        return value.lower()

    def validate_type(self, value: str) -> str:
        return value.lower()

class ChatbotInputSerializer(serializers.Serializer):
    input = serializers.CharField(required=False)
    audio_url = serializers.URLField(required=False)
    audio = serializers.FileField(required=False)
    user = serializers.CharField(required=False)
    history = MessageSerializer(many=True, required=False)

    def validate(self, attrs: dict):
        at_least_one_of = {"input", "audio_url", "audio"}
        
        interserction = at_least_one_of & set(attrs.keys())

        if not interserction:
            raise serializers.ValidationError(f"Either one of following fields required: {', '.join(at_least_one_of)}.")
        
        if len(interserction) > 1:
            raise serializers.ValidationError(f"Fields ({', '.join(interserction)}) can't coexist.")

        return super().validate(attrs)

    def validate_audio(self, value: UploadedFile) -> UploadedFile:
        
        if value.content_type.split("/")[0] != "audio":
            raise serializers.ValidationError(f"Audio file content_type must be 'audio/*', but got {value.content_type}")

        return value

    def validate_history(self, history: OrderedDict) -> OrderedDict:
        # set maximum messages allowed
        return history