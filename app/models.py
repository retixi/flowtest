from django.db import models


# Create your models here.

class FlowTable(models.Model):
     city=models.CharField(max_length=30)
     cate=models.CharField(max_length=30)
     flow_data=models.FloatField()
     last_date=models.DateField()
     uni_count=models.IntegerField()
     ne_name=models.CharField(max_length=100)
     bu_peak=models.FloatField()
     bu_busy_avg=models.FloatField()
     bu_avg=models.FloatField()
     port_name=models.CharField(max_length=100)
     band_width=models.IntegerField()

class BuildLog(models.Model):
     title=models.CharField(max_length=255)
     inner=models.CharField(max_length=255)



