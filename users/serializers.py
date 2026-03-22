from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'email', 'avatar', 'created_at')
        read_only_fields = ('id', 'created_at')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': '两次密码不一致'})
        
        if not User.validate_chinese_phone(attrs['phone']):
            raise serializers.ValidationError({'phone': '手机号格式不正确'})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(serializers.Serializer):
    # 定义字段，使phone和username都是可选的
    username = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        identifier = attrs.get('phone') or attrs.get('username', '')
        password = attrs.get('password')
        
        if not identifier or not password:
            raise serializers.ValidationError('用户名/手机号和密码不能为空')
        
        user = None
        try:
            if identifier.isdigit() and len(identifier) == 11:
                user = User.objects.get(phone=identifier)
            else:
                user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名/手机号或密码错误')

        if not user.check_password(password):
            raise serializers.ValidationError('用户名/手机号或密码错误')

        if not user.is_active:
            raise serializers.ValidationError('账户已被禁用')

        # 生成token
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        data['user'] = UserSerializer(user).data
        return data
