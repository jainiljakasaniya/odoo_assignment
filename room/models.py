from django.db import models

class Sessions(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def __str__(self):
        return self.name
    
class Tags(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Rooms(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    tag_id = models.ForeignKey(Tags,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Booking(models.Model):
    id=models.AutoField(primary_key=True)
    room_id = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    date = models.IntegerField()
    start_time = models.CharField(max_length=5)
    end_time = models.CharField(max_length=5)
    # session_id = md
    session_id = models.ForeignKey(Sessions,on_delete=models.CASCADE)
    