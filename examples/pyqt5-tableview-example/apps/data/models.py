import sys
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Make sure you have django installed")
    sys.exit()


# Your models go here
class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.FloatField()
    star = models.IntegerField()

