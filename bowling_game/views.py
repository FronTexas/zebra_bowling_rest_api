# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .models import BowlingGame
from .serializers import StockSerializer

class BowlingGameView(APIView):

	def get(self, request):
		bowling_game = BowlingGame.objects.all()
		if len(bowling_game) == 0: 
			bowling_game = BowlingGame.objects.create()
		return Response({})



