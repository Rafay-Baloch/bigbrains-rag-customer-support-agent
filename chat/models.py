from django.db import models

class KnowledgeBase(models.Model):
    CATEGORY_CHOICES = [
        ('course', 'Course'),
        ('internship', 'Internship'),
        ('policy', 'Policy'),
        ('resource', 'Learning Resource'),
        ('service', 'Service & Product'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    source_url = models.URLField(max_length=500, blank=True, null=True)
    content = models.TextField()
    keywords = models.CharField(max_length=500, help_text="Comma-separated keywords")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.category.upper()}] {self.title}"