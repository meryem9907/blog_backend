from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, AuthorSerializer, WritableAuthorSerializer
from .models import Author
from .permissions import IsAdminOrSelf

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MeView(generics.RetrieveAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required."}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid refresh token."}, status=400)
        return Response({"detail": "Logged out."}, status=205)
    
class DeleteUserView(generics.DestroyAPIView):
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrSelf]
    serializer_class = WritableAuthorSerializer

    def get_object(self):
        return self.request.user
    
class UpdateUserView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrSelf]
    serializer_class = WritableAuthorSerializer

    def get_object(self):
        return self.request.user
    
    def perform_update(self, serializer):
        # Ensure sensitive fields handled properly
        password = serializer.validated_data.pop("password", None)
        author = serializer.save()
        if password:
            author.set_password(password)
            author.save() 