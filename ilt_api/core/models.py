from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class MementoCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000, unique=True, null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    mementoCategory = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="A MementoCategory can't reference itself",
    )

    def __str__(self):
        return (
            "#" + str(self.id) + " - " + self.name + " (u=" + self.user.username + ")"
        )

    # Prevent self-referencing
    def save(self, *args, **kwargs):
        if self.mementoCategory and self.mementoCategory.id == self.id:
            raise ValidationError("A MementoCategory can't reference itself!")
        return super(MementoCategory, self).save(*args, **kwargs)

    class Meta:
        db_table = "ilt_memento_category"
        verbose_name_plural = "memento categories"


class Memento(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000, unique=True, null=True, blank=True)
    mementoCategory = models.ForeignKey(to=MementoCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ilt_memento"
