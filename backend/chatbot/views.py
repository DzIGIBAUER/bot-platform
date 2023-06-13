from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from langchain.schema import messages_from_dict

from .models import Chatbot
from .serializers import ChatbotSerializer, ChatbotInputSerializer

from common import utils

class ChatbotViewset(viewsets.ModelViewSet):
    queryset = Chatbot.objects.all()
    serializer_class = ChatbotSerializer
    authentication_classes = [TokenAuthentication]

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        queryset = super().filter_queryset(queryset)
        return queryset.filter(user=self.request.user)

    def get_object(self) -> Chatbot:
        return super().get_object()
    
    @action(detail=True, methods=['post'])
    def generate_response(self, request: Request, pk: str | None = None) -> Response:
        serializer = ChatbotInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        chatbot = self.get_object()

        #print(serializer.validated_data)
        
        messages = messages_from_dict(
            [{"type": msg_data.pop("type"), "data": msg_data} for msg_data in serializer.validated_data.get("history", [])]
        )

        # Serializer guarantees that either `input`, `audio_url` or 'audio' exists. 
        input = serializer.validated_data.get("input")
        if not input:
            if serializer.validated_data.get("audio_url"):
                with utils.audio_file_from_url(serializer.validated_data["audio_url"]) as audio_file:
                    input = utils.transcribe_audio(file=audio_file)
            else:
                    input = utils.transcribe_audio(file=serializer.validated_data["audio"])


    
        return Response(chatbot.generate_response(input=input, user=serializer.validated_data.get('user'), history=messages))