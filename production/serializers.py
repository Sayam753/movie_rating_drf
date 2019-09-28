from rest_framework import serializers
from django.contrib.auth import get_user_model
from production.models import ProfileOfProduction, ProfileOfActor, ProfileOfDirector, ProfileOfUser
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_no=validated_data['phone_no'],
            birth_date=validated_data['birth_date'],
            biography=validated_data['biography'],
            grp=validated_data['grp'],
        )
        user.set_password(validated_data['password'])
        if validated_data['grp'] == 'a':
            p = ProfileOfProduction.objects.create(user=user)
        elif validated_data['grp'] == 'b':
            p = ProfileOfActor.objects.create(user=user)
        elif validated_data['grp'] == 'c':
            p = ProfileOfDirector.objects.create(user=user)
        else:
            p = ProfileOfUser.objects.create(user=user)
        p.save()
        user.save()
        return user

    class Meta:
        model = UserModel
        fields = ("id", "email", 'password', "username", 'first_name', 'last_name',
                  'phone_no', 'birth_date', 'biography', 'grp',)


class ProfileOfProductionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = 'ProfileOfProduction-detail'

    class Meta:
        model = ProfileOfProduction
        fields = ('user', )


class ProfileOfActorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = 'ProfileOfActor-detail'

    class Meta:
        model = ProfileOfActor
        fields = ('user', 'max_rating', 'min_rating')
        # fields = ('user', )


class ProfileOfDirectorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = 'ProfileOfDirector-detail'

    class Meta:
        model = ProfileOfDirector
        fields = ('user', 'max_rating', 'min_rating')
        # fields = ('user', )


class ProfileOfUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = 'ProfileOfUser-detail'

    class Meta:
        model = ProfileOfUser
        fields = ('user', 'max_rating', 'min_rating', 'get_avg_rating')
        # fields = ('user', )

