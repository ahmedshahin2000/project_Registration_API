from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import User, Client

class UserSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(source='patient.uploadimage.image')
    class Meta:
        model=User
        fields=['email', 'username', 'phone']


class ClientSignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"}, write_only=True)
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['email', 'username', 'password', 'password2', 'phone']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def save(self, **kwargs):
        user=User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            phone=self.validated_data['phone'],
            # age=self.validated_data['age']     
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        # user.is_patient=True
        user.save()
        Client.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Access denied: This credentials does not meet any of our records, please make sure you have entered the right credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['email'] = email
        return attrs