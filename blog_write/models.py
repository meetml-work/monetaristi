from django.db import models
from django.utils import timezone 
from datetime import timedelta 
#from django.core.validators import MinLengthValidator, MaxLengthValidator
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.conf import settings


# Create your models here.

# Base model with timestamp fields
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    class Meta:
        abstract = True

# Your Tag model
class Tag(TimestampedModel):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption

# Your Author model
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

# Your Articles model
class Articles(TimestampedModel):
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=250, null=True)
    image = models.ImageField(upload_to="images")
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField()
    #content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="articles")
    tags = models.ManyToManyField(Tag)
    
    def save(self, *args, **kwargs):
        if len(self.excerpt) >= 170:
            self.excerpt = self.excerpt[:170]+"..."
        super().save(*args, **kwargs)
        
    
    class Meta:
        verbose_name = "Article"
        
      
class Biography(models.Model):
    ContentBiography = models.TextField()
    
    class Meta:
        verbose_name_plural = "Biography"
  

class VerifiedUser(models.Model):
    user = models.CharField(primary_key=True, max_length = 100)

    def __str__(self):
        return self.user
  

class ClickLog(models.Model):
    ip_address = models.CharField(max_length=50)
    url = models.CharField(max_length=2048)
    timestamp = models.DateTimeField(auto_now_add=True)
    click_by_type = models.CharField(max_length=100, help_text="Type of click: Article, Template, etc.")
    
    