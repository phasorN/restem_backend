from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):

	title = models.CharField(max_length = 200)
	description = models.TextField(blank = True)
	amount = models.PositiveIntegerField()
	date = models.DateField()
	user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

	def __str__(self):
		return self.title

	def new(self):
		return self.amount