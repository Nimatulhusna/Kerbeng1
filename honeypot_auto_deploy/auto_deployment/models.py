from django.db import models


class Device(models.Model):
    ip_address = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    ssh_port = models.IntegerField(default=22)

    VENDOR_CHOICES = (
        ('mikrotik', 'Mikrotik'),
        ('cisco', 'Cisco')
    )
    vendor = models.CharField(max_length=255, choices=VENDOR_CHOICES)

    def __str__(self):
        return "{}. {}".format(self.id, self.ip_address)  # type: ignore


class Log(models.Model):
    target = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.DateTimeField(null=True)
    messages = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.target, self.action, self.status)
