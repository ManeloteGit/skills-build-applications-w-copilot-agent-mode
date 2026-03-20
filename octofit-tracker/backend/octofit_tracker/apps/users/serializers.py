"""
Serializers for User API
"""

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    bmi = serializers.SerializerMethodField()
    fitness_level_display = serializers.CharField(
        source='get_fitness_level_display_es',
        read_only=True
    )
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'height_cm', 'weight_kg', 'age', 'gender', 'fitness_level',
            'fitness_level_display', 'bio', 'profile_picture', 'bmi',
            'is_active', 'created_at', 'updated_at', 'last_login'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']
    
    def get_bmi(self, obj):
        """Get BMI value"""
        return obj.get_bmi()
    
    def get_full_name(self, obj):
        """Get full name"""
        return obj.get_full_name()


class UserDetailSerializer(UserSerializer):
    """Detailed serializer for User model with additional fields"""
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirmar contraseña'
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password2', 'fitness_level'
        ]
    
    def validate(self, data):
        """Validate password confirmation"""
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError(
                {'password': 'Las contraseñas no coinciden.'}
            )
        return data
    
    def create(self, validated_data):
        """Create user with hashed password"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            fitness_level=validated_data.get('fitness_level', 'beginner')
        )
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'height_cm', 'weight_kg',
            'age', 'gender', 'fitness_level', 'bio', 'profile_picture'
        ]
