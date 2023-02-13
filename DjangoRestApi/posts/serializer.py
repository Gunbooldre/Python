from rest_framework import serializers
from .models import Posts


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = "__all__"
    # title = serializers.CharField(max_length=255)
    # content = serializers.CharField()
    # time_created = serializers.DateTimeField(read_only=True)
    # time_update = serializers.DateTimeField(read_only=True)
    # is_published = serializers.BooleanField(default=True)
    # category_id = serializers.CharField()

    # def create(self, validated_data):
    #     return Posts.objects.create(**validated_data)

    # def update(self, instance,validated_data):
    #     instance.title = validated_data.get('title',instance.title)
    #     instance.content = validated_data.get('content',instance.content)
    #     instance.time_created = validated_data.get('time_created',instance.time_created)
    #     instance.time_update = validated_data.get('time_update',instance.time_update)
    #     instance.is_published = validated_data.get('is_published',instance.is_published)
    #     instance.category_id = validated_data.get('category_id',instance.category_id)
    #     instance.save()
    #     return instance

