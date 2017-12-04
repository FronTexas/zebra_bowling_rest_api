# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Frames(models.Model):
	first_throw = models.CharField()
	second_throw = models.CharField()
	total_score = models.CharField()

	def __str__(self):
		return {'first_throw': self.first_throw, 'second_throw': self.second_throw, 'total_score': self.total_score}
