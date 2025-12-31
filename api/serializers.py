from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'username', 'phone', 'first_name', 'last_name', 'type', 'default_lang', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UpdateUserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ItemVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVendor
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    vendor_items = ItemVendorSerializer(many=True, read_only=True)
    class Meta:
        model = Vendor
        fields = '__all__'


class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name_fr', 'image', 'name_ar', 'price1', 'price2', 'price3', 'livraison', 'is_big_steak', 'type', 'type_class']


class ItemVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVendor
        fields = '__all__'


class ItemVendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVendor
        fields = ['id', 'image', 'nom', 'prix' ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'type', 'first_name', 'last_name', ]


class ItemCommandeSerializer(serializers.ModelSerializer):
    vendor = VendorDetailSerializer(read_only=True)
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(), source='vendor', write_only=True
    )
    item = ItemVendorDetailSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=ItemVendor.objects.all(), source='item', write_only=True
    )

    class Meta:
        model = ItemCommande
        fields = [
            'id', 'commande', 'vendor', 'vendor_id',
            'number', 'item', 'item_id'
        ]

class CommandeSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    items = ItemCommandeSerializer(many=True, read_only=True)

    class Meta:
        model = Commande
        fields = [
            'id', 'title', 'code', 'prix', 'date', 'status', 'location', 'livraison', 'capture',
            'phone', 'user', 'items'
        ]

    def create(self, validated_data):
        user = self.context['user'] 
        return Commande.objects.create(user=user, **validated_data)