from django.urls import path
from .views import index, notes_page, add_note, get_notes, update_note, delete_note, create_folder

urlpatterns = [
    path('', index, name='index'),
    path('notes/', notes_page, name='notes_page'),
    path('add_note/', add_note, name='add_note'),
    path('get_notes/', get_notes, name='get_notes'),
    path('update_note/<int:note_id>/', update_note, name='update_note'),
    path('delete_note/<int:note_id>/', delete_note, name='delete_note'),
    path('create_folder/', create_folder, name='create_folder'),
]
