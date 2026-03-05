import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.fields.SmallIntegerField()
    can_be_contacted = models.fields.BooleanField()
    can_data_be_shared = models.fields.BooleanField()


class Project(models.Model):
    BACKEND = 'BACKEND'
    FRONTEND = 'FRONTEND'
    IOS = 'IOS'
    ANDROID = 'ANDROID'
    TYPES = (
        (BACKEND, 'Back-end'),
        (FRONTEND, 'Front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    )

    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(max_length=2048,
                                          blank=True)
    author = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE, verbose_name="Autheur")
    contributors = models.ManyToManyField(
        User, through='Contributor', related_name="project_contributor", verbose_name="Contributeurs")
    type = models.fields.CharField(max_length=128, choices=TYPES, verbose_name="Type")
    time_created = models.fields.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Contributor.objects.get_or_create(user=self.author, project=self)

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE,
                             related_name='contributor')
    project = models.ForeignKey(to=Project,
                                on_delete=models.CASCADE,
                                related_name='project')
    time_created = models.fields.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project', )

    def __str__(self) -> str:
        return "Contributor: " + str(self.user) + "of project " \
            + str(self.project)


class Issue(models.Model):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    STATUS = (
        (OPEN, 'Ouverte'),
        (CLOSED, 'Fermée'),
    )
    
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRIORITY = (
        (LOW, 'Mineur'),
        (MEDIUM, 'Normale'),
        (HIGH, 'Majeur'),
    )

    BUG = 'BUG'
    TASK = 'TASK'
    UPGRADE = 'UPGRADE'
    TAGS = (
        (BUG, 'Bug'),
        (TASK, 'Tâche'),
        (UPGRADE, 'Amélioration'),
    )

    TO_DO = 'TO_DO'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'
    PROGRESSION = (
        (TO_DO, 'À faire'),
        (IN_PROGRESS, 'En cours'),
        (FINISHED, 'Terminé'),
    )

    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(max_length=2048,
                                          blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author", verbose_name="Autheur")
    
    current_status = models.fields.CharField(max_length=128, choices=STATUS, verbose_name="Statut")
    priority = models.fields.CharField(max_length=128, choices=PRIORITY, verbose_name="Priorité")
    tag = models.fields.CharField(max_length=128, choices=TAGS, verbose_name="Balise")
    progression = models.fields.CharField(max_length=128, choices=PROGRESSION, verbose_name="Progression")
    
    project = models.ForeignKey(Project,on_delete=models.CASCADE)

    contributor_assigned = models.ForeignKey(
        User, limit_choices_to={'contributor__project': models.F('project_contributor')}, 
        related_name="contributor_assigned", verbose_name="assigner au contributeur", 
        null=True, on_delete=models.SET_NULL)

    time_created = models.fields.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    content = models.fields.TextField(max_length=2048)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    time_created = models.fields.DateTimeField(auto_now_add=True)