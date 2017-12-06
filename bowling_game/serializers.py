from rest_framework import serializers 
from .models import Frame

class FrameSerializer(serializers.ModelSerializer):
	class Meta: 
		model = Frame
		fields = ('first_throw_score', 'second_throw_score', 'third_throw_score', 'total_score')
