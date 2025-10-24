from django.db import models

class Driver(models.Model): 
    # simple authentication
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    car_registration_number = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255, unique=False)
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username
  
class DailyLog(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    date = models.DateField() 
    
    class Meta:
        unique_together = ('driver', 'date') 
        
    def __str__(self):
        return f"Log for {self.driver.user.username} on {self.date}"
    
STATUS_CHOICES = (
    ('OFF', 'Off Duty'),
    ('SB', 'Sleeper Berth'),
    ('DR', 'Driving'),
    ('ON', 'On Duty (Not Driving)'),
)

class StatusChange(models.Model):
    log = models.ForeignKey(DailyLog, on_delete=models.CASCADE, related_name='status_changes')
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField() # When the status changed
    location = models.CharField(max_length=255, help_text="Current location, potentially GPS coordinates")
    remarks = models.TextField(blank=True) # to update maybe the kind of taks at hand say, onloading/ offloading etc
    
    class Meta:
        # Order by time
        ordering = ['timestamp'] 
        
    def __str__(self):
        return f"{self.status} at {self.timestamp.time()} for {self.log.driver.user.username}"
    
