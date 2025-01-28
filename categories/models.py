from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ["title"]
        
    def __str__(self):
            return self.title
