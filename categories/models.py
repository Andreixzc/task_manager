from django.db import models


# models.Model = importing 'Model' model as 'models';
class Category(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="007bff")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["Name"]

    def __str__(self):
        return self.name
