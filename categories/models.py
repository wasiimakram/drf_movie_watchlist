from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    created_at = models.DateField(auto_now_add=True)

    # --- Meta Configuration ---
    class Meta:
        # Fixes the plural spelling in the Django Admin dashboard (avoids 'Categorys')
        verbose_name_plural = 'Categories'
        
        # Automatically sorts query results alphabetically by name (A to Z)  
        ordering = ['name']

    # --- Custom Save Logic ---
    def save(self, *args, **kwargs):
        # This save will override the default save method to add slug
        # Only generate a slug if it doesn't already exist (prevents broken URLs if renamed later)  
        if not self.slug:
            # Converts the name string into a URL-friendly slug (e.g., "Sci-Fi & Fantasy" -> "sci-fi-fantasy")  
            self.slug = slugify(self.name)
            
        # Call the original built-in Django save method to finalize saving to the database  
        super().save(*args, **kwargs)

    # --- String Representation for Admin Panel ---
    def __str__(self):
        # Returns the actual name string instead of a generic '<Category: Category object (1)>' in the admin panel
        return self.name