from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .serializers import ClientSignupSerializer, LoginSerializer
# from .permissions import IsPatientUser, IsDoctorUser


class ClientSignupView(generics.GenericAPIView):
    serializer_class = ClientSignupSerializer

    def post(self, request, *args, **kwargs):
            data = {}
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                data['status'] = True
                data.update({"message": "Registration done successfully",
                    "user": serializer.data,
                    #"token": Token.objects.get(user=user).key,
                })
                return Response(data)
            data['status'] = False
            data.update(serializer.errors)
            return Response({"message":"A user with that email already exists."
                            ,"user":data})


class CustomAuthToken(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            # 'is_patient': user.is_patient,
            # 'age': user.age,
            "message": "Login done successfully",
        })

class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from .serializers import ChangePasswordSerializer
# from rest_framework.permissions import IsAuthenticated   

# class ChangePasswordView(generics.UpdateAPIView):

#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)