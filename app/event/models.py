from django.db import models


# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=48)
    image = models.ImageField(upload_to='event', null=True)
    square_image = models.ImageField(upload_to='event/square', null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class MainEvent(models.Model):
    title = models.CharField(max_length=48)
    image = models.ImageField(upload_to='mainEvent/list', max_length=500, null=True)
    detail_image = models.ImageField(upload_to='mainEvent/detail', null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)


class MainEventType(models.Model):
    name = models.CharField(max_length=50, )
    event = models.ForeignKey(
        'event.MainEvent',
        on_delete=models.CASCADE,
        related_name='event',
    )


class GoodsEventType(models.Model):
    type = models.ForeignKey(
        'event.MainEventType',
        on_delete=models.CASCADE,
        related_name='mainEvent',
    )
    goods = models.ForeignKey(
        'goods.Goods',
        on_delete=models.CASCADE,
        related_name='mainEvent',
    )
