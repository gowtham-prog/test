from django.db import models

# Create your models here.
class Airport(models.Model):
     City= models.CharField(max_length=64)
     Code= models.CharField(max_length=3)
     def __str__(self):
         return f"{self.City} ({self.Code})"
class Flight(models.Model):
    Origin= models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="departures")
    Destination=models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="arrivals")
    Duration=models.IntegerField()
    def __str__(self):
        return f"{ self.id} : from {self.Origin} to {self.Destination} Duration: {self.Duration}"
    def is_valid_flight(self):
        return self.Origin != self.Destination or self.Duration > 0
class Passenger(models.Model):
    first= models.CharField(max_length=64)
    last=models.CharField(max_length=64)
    flights=models.ManyToManyField(Flight,blank=True,related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"
