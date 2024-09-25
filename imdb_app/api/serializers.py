from rest_framework import serializers
from imdb_app.models import Watchlist, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        
class WatchlistSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='platform.name')
    # reviews = ReviewSerializer(many = True, read_only = True) 
    def create(self, validated_data):
        platform_name = validated_data.pop('platform')['name']
        platform = StreamPlatform.objects.get(name = platform_name)
        if not platform:
            raise serializers.ValidationError("platform doesn't exists")
        return Watchlist.objects.create(platform = platform, **validated_data)   
    class Meta:
        model = Watchlist
        fields = '__all__'
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchlistSerializer(many=True, read_only=True) #This variable namemust be exactly same as the related_name parameter in models.py
    class Meta:
        model = StreamPlatform
        fields = '__all__'
        
        
