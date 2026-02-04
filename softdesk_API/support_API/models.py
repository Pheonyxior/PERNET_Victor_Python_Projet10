from django.db import models
from authentication.models import User

class Project(models.Model):
    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(max_length=2048,
                                          blank=True)
    contributors = models.ManyToManyField(User, verbose_name="list of contributors")
    time_created = models.fields.DateTimeField(auto_now_add=True)

class Issue(models.Model):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    STATUS = (
        (OPEN, 'Ouverte'),
        (CLOSED, 'Fermée'),
    )
    
    MAJOR = 'MAJOR'
    MINOR = 'MINOR'
    PRIORITY = (
        (MAJOR, 'Majeur'),
        (MINOR, 'Mineur'),
    )

    BUG = 'BUG'
    TASK = 'TASK'
    UPGRADE = 'UPGRADE'
    TAGS = (
        (BUG, 'Bug'),
        (TASK, 'Tâche'),
        (UPGRADE, 'Amélioration'),
    )

    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(max_length=2048,
                                          blank=True)
    current_status = models.fields.CharField(max_length=128, choices=STATUS, verbose_name="Statut")
    priority = models.fields.CharField(max_length=128, choices=PRIORITY, verbose_name="Priorité")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.fields.CharField(max_length=128, choices=TAGS, verbose_name="Balise")
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    time_created = models.fields.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    content = models.fields.TextField(max_length=2048)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    time_created = models.fields.DateTimeField(auto_now_add=True)