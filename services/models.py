from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import uuid

class Provider(models.Model):
    name = models.CharField(max_length = 500, blank = True, null = True)

    def __str__(self):
        return f"{self.name}"

class Routes(models.Model):
    route =  models.CharField(max_length = 200, blank = True, null = True)
    provider = models.ForeignKey(Provider, on_delete= models.CASCADE)

    def __str__(self):
        return f"{self.route}"

    
class Bus(models.Model):
    name = models.CharField(max_length = 200, blank = True, null = True)
    provider = models.ForeignKey(Provider, on_delete= models.CASCADE)
    source = models.CharField(max_length=200, blank = True, null = True)
    destination = models.CharField(max_length=200, blank = True, null = True) 
    route = models.ManyToManyField(Routes)
    date_of_journey = models.DateTimeField()

    def __str__(self):
        return f"{self.name}"
    
class Seats(models.Model):
    bus = models.ForeignKey(Bus, on_delete= models.CASCADE)
    total_seats = models.IntegerField(default=0)
    booked_seats = models.IntegerField(default=0)
    available_seats = models.IntegerField(default=0)
    blocked_seats = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
       
        calculated_available_seats = self.total_seats - self.blocked_seats - self.booked_seats
        if calculated_available_seats < 0:
            raise ValidationError(
                "The sum of blocked_seats and booked_seats exceeds total_seats."
            )
        self.available_seats = calculated_available_seats
        
        super().save(*args, **kwargs)

class Block(models.Model):
    block_id = models.UUIDField(default=uuid.uuid4, editable=False)
    seats_bus = models.ForeignKey(Seats, on_delete=models.CASCADE)
    blocked_seats = models.IntegerField()
    

class Book(models.Model):
    book_id = models.UUIDField(default=uuid.uuid4, editable=False)
    seats_bus = models.ForeignKey(Seats, on_delete=models.CASCADE)
    booked_seats = models.IntegerField()
    

@receiver(post_delete, sender=Book)
def update_seats_on_book_delete(sender, instance, **kwargs):
    seats = instance.seats_bus
    seats.booked_seats -= instance.booked_seats
    seats.save()

@receiver(post_save, sender=Book)
def update_seats_on_book_save(sender, instance, created, **kwargs):
    if created:
        seats = instance.seats_bus
        seats.booked_seats += instance.booked_seats
        seats.save()

@receiver(post_delete, sender=Block)
def update_seats_on_block_delete(sender, instance, **kwargs):
    seats = instance.seats_bus
    seats.blocked_seats -= instance.blocked_seats
    seats.save()

@receiver(post_save, sender=Block)
def update_seats_on_block_save(sender, instance, created, **kwargs):
    if created:
        seats = instance.seats_bus
        seats.blocked_seats += instance.blocked_seats
        seats.save()