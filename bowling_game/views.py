# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .models import BowlingGame
from .serializers import FrameSerializer

class BowlingGameView(APIView):

	def get(self, request):
		bowling_game = self.get_bowling_game_if_exist_instantiate_new_one_otherwise()
		serializer = FrameSerializer(bowling_game.get_frames(), many = True)
		return Response(serializer.data)

	def get_bowling_game_if_exist_instantiate_new_one_otherwise(self):
		if len(BowlingGame.objects.all()) == 0: 
			return BowlingGame.objects.create()
		else: 
			return BowlingGame.objects.all()[0]