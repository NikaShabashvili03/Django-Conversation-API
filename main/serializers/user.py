from rest_framework import serializers
from ..models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            if user.check_password(data['password']):
                return user
            else:
                raise serializers.ValidationError("Invalid credentials")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        
class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = User 
        fields = ['id', 'isOnline', 'avatar', 'firstname', 'lastname', 'email']

    def to_representation(self, instance):
         representation = super().to_representation(instance)
         if instance.avatar:
               representation['avatar'] = instance.avatar.url
         return representation