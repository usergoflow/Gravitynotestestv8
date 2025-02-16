from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        """Проверка, существует ли уже папка с таким именем"""
        if Folder.objects.filter(name=self.name).exists():
            raise ValueError("Папка с таким названием уже существует!")
        super().save(*args, **kwargs)


class Note(models.Model):
    """Модель для хранения заметок"""
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="notes", null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
