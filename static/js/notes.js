document.addEventListener("DOMContentLoaded", loadNotes);

function openEditor() {
    document.getElementById("noteEditor").style.display = "flex";
}

function closeEditor() {
    if (confirm("Сохранить заметку перед закрытием?")) {
        saveNote();
    }
    document.getElementById("noteEditor").style.display = "none";
}

function saveNote() {
    let title = document.getElementById("noteTitle").value;
    let content = document.getElementById("noteContent").value;
    if (title.trim() === "" || content.trim() === "") return;

    fetch("/add_note/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title: title, content: content})
    }).then(() => {
        document.getElementById("noteTitle").value = "";
        document.getElementById("noteContent").value = "";
        closeEditor();
        loadNotes();
    });
}

function loadNotes() {
    fetch("/get_notes/").then(response => response.json()).then(data => {
        let notesList = document.getElementById("notesList");
        notesList.innerHTML = "";
        data.notes.forEach(note => {
            let noteElement = document.createElement("div");
            noteElement.classList.add("note-item");
            noteElement.innerHTML = `
                <div class="note-title">${note.title}</div>
                <div class="note-content">${truncateText(note.content, 3)}</div>
                <div class="note-buttons">
                    <button class="edit-button" onclick="editNote(${note.id})">Редактировать</button>
                    <button class="delete-button" onclick="deleteNote(${note.id})">Удалить</button>
                </div>
            `;
            notesList.appendChild(noteElement);
        });
    });
}

function deleteNote(noteId) {
    if (confirm("Вы уверены, что хотите удалить эту заметку?")) {
        fetch(`/delete_note/${noteId}/`, {
            method: "DELETE",
            headers: {"Content-Type": "application/json"}
        }).then(() => loadNotes());
    }
}

function truncateText(text, lines) {
    return text.split(" ").slice(0, lines * 5).join(" ") + "...";
}
