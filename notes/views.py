from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Note, Folder
import json

# Отображение главной страницы
def index(request):
    return render(request, 'index.html')

# Отображение страницы заметок
def notes_page(request):
    return render(request, 'notes.html')

# Добавление новой заметки
@csrf_exempt
def add_note(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        folder_name = data.get("folder", None)
        title = data.get("title", "Без названия")
        content = data.get("content", "")

        folder = None
        if folder_name:
            folder, _ = Folder.objects.get_or_create(name=folder_name)

        note = Note.objects.create(title=title, content=content, folder=folder)
        return JsonResponse({"message": "Заметка добавлена", "id": note.id, "title": note.title, "content": note.content})

# Создание новой папки
@csrf_exempt
def create_folder(request):
    """Создает новую папку, если ее еще нет"""
    if request.method == 'POST':
        data = json.loads(request.body)
        folder_name = data.get("name")

        if not folder_name.strip():
            return JsonResponse({"error": "Название папки не может быть пустым"}, status=400)

        folder, created = Folder.objects.get_or_create(name=folder_name)

        return JsonResponse({
            "id": folder.id,
            "name": folder.name,
            "created": created
        })

# Получение всех заметок
@csrf_exempt
def get_notes(request):
    notes = list(Note.objects.values("id", "title", "content", "folder__name"))
    return JsonResponse({"notes": notes})

# Обновление заметки
@csrf_exempt
def update_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    data = json.loads(request.body)
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.save()
    return JsonResponse({"message": "Заметка обновлена"})

# ✅ Исправленное удаление заметки
@csrf_exempt
def delete_note(request, note_id):
    if request.method == "DELETE":
        note = get_object_or_404(Note, id=note_id)
        note.delete()
        return JsonResponse({"message": f"Заметка {note_id} удалена"})
    return JsonResponse({"error": "Неверный метод"}, status=400)
