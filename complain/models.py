from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('DONE', 'Done'),
        ('REJECT', 'Reject'),
        ('IN_PROGRESS', 'In Progress'),
    ]
    
    COMPLAINT_TYPE_CHOICES = [
        ('general', 'General'),
        ('technical', 'Technical'),
        ('billing', 'Billing'),
        ('other', 'Other'),
    ]
    
    id = models.AutoField(primary_key=True)  
    username = models.CharField(max_length=100)
    user_id = models.BigIntegerField()
    description = models.TextField()
    complaint_type = models.CharField(max_length=50)
    file_path = models.CharField(max_length=255, blank=True, null=True)  
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    update_status_by = models.CharField(max_length=100, blank=True, null=True)
    update_date = models.CharField(blank=True, null=True, max_length=100)
    keterangan = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'bot_complaints_dev'
        ordering = ['-created_at']
        managed = False
    
    def __str__(self):
        return f"{self.username} - {self.complaint_type} - {self.status}"
