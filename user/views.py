from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreate(viewsets.ViewSet):

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)})
        return Response(serializer.errors)
