from rest_framework import serializers

from testApp.models import TestModel, TestSubModel


class TestModelSerializer(serializers.ModelSerializer):
    sub_model_name = serializers.ReadOnlyField(source='sub_model.name')

    class Meta:
        model = TestModel
        fields = '__all__'

    def validate_age(self, value):
        if value is None:
            raise serializers.ValidationError("Age cannot be null.")
        return value

    def validate_name(self, value):
        if value is None:
            raise serializers.ValidationError("Name cannot be null.")
        return value

    def validate(self, data):
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        custom_data = {
            'id': data.get('id'),
            'name': data.get('name'),
            'age': data.get('age'),
            'sub_model': data.get('sub_model'),
            'sub_model_name': data.get('sub_model_name'),
            'additional_info': "come from to_representation",
        }
        return custom_data


class TestSubModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSubModel
        fields = '__all__'
