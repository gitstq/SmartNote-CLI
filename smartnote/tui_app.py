"""
TUI Application for SmartNote-CLI
Built with Textual for a rich terminal interface
"""

import json
from datetime import datetime
from typing import Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import (
    Header, Footer, Static, Input, TextArea, DataTable,
    ListView, ListItem, Label, Button, Markdown, TabbedContent, TabPane
)
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import ModalScreen

from .database import NoteDatabase
from .ai_engine import AIEngine, AIConfig


class ConfirmDialog(ModalScreen[bool]):
    """Confirmation dialog"""
    
    def __init__(self, message: str, *args, **kwargs):
        self.message = message
        super().__init__(*args, **kwargs)
    
    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Label(self.message, id="dialog-message")
            with Horizontal(id="dialog-buttons"):
                yield Button("Confirm", variant="error", id="confirm")
                yield Button("Cancel", variant="primary", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            self.dismiss(True)
        else:
            self.dismiss(False)


class NoteEditor(ModalScreen[dict]):
    """Note editor modal"""
    
    def __init__(self, note: Optional[dict] = None, *args, **kwargs):
        self.note = note
        super().__init__(*args, **kwargs)
    
    def compose(self) -> ComposeResult:
        with Container(id="editor"):
            yield Label("Note Editor", id="editor-title")
            yield Input(
                placeholder="Note title...",
                value=self.note["title"] if self.note else "",
                id="title-input"
            )
            yield Input(
                placeholder="Tags (comma separated)...",
                value=", ".join(json.loads(self.note["tags"])) if self.note else "",
                id="tags-input"
            )
            yield TextArea(
                text=self.note["content"] if self.note else "",
                id="content-input"
            )
            with Horizontal(id="editor-buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("AI Assist", variant="primary", id="ai-assist")
                yield Button("Cancel", variant="default", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            title = self.query_one("#title-input", Input).value
            content = self.query_one("#content-input", TextArea).text
            tags_str = self.query_one("#tags-input", Input).value
            tags = [t.strip() for t in tags_str.split(",") if t.strip()]
            
            self.dismiss({
                "title": title,
                "content": content,
                "tags": tags
            })
        elif event.button.id == "ai-assist":
            self._ai_assist()
        else:
            self.dismiss(None)
    
    def _ai_assist(self):
        """Use AI to generate tags and summary"""
        title = self.query_one("#title-input", Input).value
        content = self.query_one("#content-input", TextArea).text
        
        if not content.strip():
            return
        
        ai = AIEngine()
        tags = ai.generate_tags(title, content)
        
        tags_input = self.query_one("#tags-input", Input)
        tags_input.value = ", ".join(tags)


class SmartNoteApp(App):
    """Main SmartNote TUI Application"""
    
    CSS = """
    Screen { align: center middle; }
    
    #dialog {
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }
    
    #dialog-message {
        text-align: center;
        margin-bottom: 1;
    }
    
    #dialog-buttons {
        align: center middle;
        height: auto;
    }
    
    #editor {
        width: 80;
        height: 40;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }
    
    #editor-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    
    #editor-buttons {
        align: center middle;
        height: auto;
        margin-top: 1;
    }
    
    #title-input, #tags-input {
        margin-bottom: 1;
    }
    
    #content-input {
        height: 20;
    }
    
    .note-list-item {
        padding: 0 1;
        height: 3;
    }
    
    .note-title {
        text-style: bold;
    }
    
    .note-meta {
        color: $text-muted;
    }
    
    #sidebar {
        width: 25%;
        border-right: solid $primary;
    }
    
    #main-content {
        width: 75%;
    }
    
    #search-box {
        dock: top;
        height: 3;
        padding: 0 1;
    }
    
    #stats-bar {
        dock: bottom;
        height: 1;
        background: $surface-darken-1;
        color: $text-muted;
        content-align: center middle;
    }
    
    .category-item {
        padding: 0 1;
        height: 1;
    }
    
    DataTable {
        height: 100%;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("n", "new_note", "New Note", show=True),
        Binding("e", "edit_note", "Edit", show=True),
        Binding("d", "delete_note", "Delete", show=True),
        Binding("f", "toggle_favorite", "Favorite", show=True),
        Binding("a", "archive_note", "Archive", show=True),
        Binding("s", "search", "Search", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("ctrl+e", "export", "Export", show=True),
    ]
    
    selected_note_id = reactive(None)
    current_filter = reactive("all")
    search_query = reactive("")
    
    def __init__(self):
        self.db = NoteDatabase()
        self.ai = AIEngine()
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Horizontal():
            # Sidebar
            with Vertical(id="sidebar"):
                yield Label("Categories", classes="sidebar-header")
                yield ListView(
                    ListItem(Label("All Notes"), id="cat-all"),
                    ListItem(Label("Favorites"), id="cat-fav"),
                    ListItem(Label("Archived"), id="cat-arch"),
                    id="category-list"
                )
                yield Label("Tags", classes="sidebar-header")
                yield ListView(id="tag-list")
            
            # Main content
            with Vertical(id="main-content"):
                yield Input(placeholder="Search notes...", id="search-box")
                yield DataTable(id="notes-table")
                yield Static(id="stats-bar")
        
        yield Footer()
    
    def on_mount(self):
        """Initialize on mount"""
        self._setup_table()
        self._load_notes()
        self._load_tags()
        self._update_stats()
    
    def _setup_table(self):
        """Setup the notes table"""
        table = self.query_one("#notes-table", DataTable)
        table.add_columns("ID", "Title", "Category", "Tags", "Updated", "Words")
        table.cursor_type = "row"
        table.zebra_stripes = True
    
    def _load_notes(self):
        """Load notes into table"""
        table = self.query_one("#notes-table", DataTable)
        table.clear()
        
        if self.search_query:
            notes = self.db.search_notes(self.search_query)
        elif self.current_filter == "fav":
            notes = self.db.get_all_notes(favorite_only=True)
        elif self.current_filter == "arch":
            notes = self.db.get_all_notes(archived=True)
        else:
            notes = self.db.get_all_notes()
        
        for note in notes:
            tags = ", ".join(json.loads(note["tags"]))[:30]
            fav_icon = "★" if note["is_favorite"] else ""
            title = f"{fav_icon} {note['title']}" if fav_icon else note["title"]
            
            table.add_row(
                str(note["id"]),
                title,
                note["category"],
                tags,
                note["updated_at"][:10],
                str(note["word_count"])
            )
    
    def _load_tags(self):
        """Load tags into sidebar"""
        tag_list = self.query_one("#tag-list", ListView)
        tag_list.clear()
        
        tags = self.db.get_tags()
        for tag in tags[:20]:  # Show top 20 tags
            tag_list.append(ListItem(
                Label(f"{tag['name']} ({tag['usage_count']})"),
                id=f"tag-{tag['name']}"
            ))
    
    def _update_stats(self):
        """Update statistics bar"""
        stats = self.db.get_stats()
        stats_bar = self.query_one("#stats-bar", Static)
        stats_bar.update(
            f"Total: {stats['total_notes']} | "
            f"Favorites: {stats['favorite_notes']} | "
            f"Tags: {stats['total_tags']} | "
            f"Words: {stats['total_words']} | "
            f"Categories: {stats['total_categories']}"
        )
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        """Handle row selection"""
        table = self.query_one("#notes-table", DataTable)
        row = table.get_row(event.row_key)
        if row:
            self.selected_note_id = int(row[0])
    
    def on_input_changed(self, event: Input.Changed):
        """Handle search input"""
        if event.input.id == "search-box":
            self.search_query = event.value
            self._load_notes()
    
    def on_list_view_selected(self, event: ListView.Selected):
        """Handle category/tag selection"""
        item_id = event.item.id
        if item_id == "cat-all":
            self.current_filter = "all"
        elif item_id == "cat-fav":
            self.current_filter = "fav"
        elif item_id == "cat-arch":
            self.current_filter = "arch"
        elif item_id and item_id.startswith("tag-"):
            tag = item_id.replace("tag-", "")
            # Filter by tag
            pass
        
        self._load_notes()
    
    def action_new_note(self):
        """Create new note"""
        def on_result(result):
            if result:
                summary = self.ai.generate_summary(result["title"], result["content"])
                category = self.ai.suggest_category(result["title"], result["content"])
                
                self.db.create_note(
                    title=result["title"],
                    content=result["content"],
                    tags=result["tags"],
                    category=category,
                    summary=summary
                )
                self._load_notes()
                self._load_tags()
                self._update_stats()
        
        self.push_screen(NoteEditor(), on_result)
    
    def action_edit_note(self):
        """Edit selected note"""
        if not self.selected_note_id:
            return
        
        note = self.db.get_note(self.selected_note_id)
        if not note:
            return
        
        def on_result(result):
            if result:
                self.db.update_note(
                    note_id=self.selected_note_id,
                    title=result["title"],
                    content=result["content"],
                    tags=result["tags"]
                )
                self._load_notes()
                self._load_tags()
        
        self.push_screen(NoteEditor(note=note), on_result)
    
    def action_delete_note(self):
        """Delete selected note"""
        if not self.selected_note_id:
            return
        
        def on_result(confirmed):
            if confirmed:
                self.db.delete_note(self.selected_note_id)
                self.selected_note_id = None
                self._load_notes()
                self._load_tags()
                self._update_stats()
        
        self.push_screen(
            ConfirmDialog("Are you sure you want to delete this note?"),
            on_result
        )
    
    def action_toggle_favorite(self):
        """Toggle favorite status"""
        if self.selected_note_id:
            self.db.toggle_favorite(self.selected_note_id)
            self._load_notes()
    
    def action_archive_note(self):
        """Archive/unarchive note"""
        if self.selected_note_id:
            self.db.archive_note(self.selected_note_id)
            self._load_notes()
            self._update_stats()
    
    def action_search(self):
        """Focus search box"""
        self.query_one("#search-box", Input).focus()
    
    def action_refresh(self):
        """Refresh data"""
        self._load_notes()
        self._load_tags()
        self._update_stats()
    
    def action_export(self):
        """Export notes"""
        import os
        export_path = os.path.expanduser("~/smartnote_export.md")
        content = self.db.export_notes("markdown")
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(content)
        self.notify(f"Notes exported to {export_path}")
    
    def on_unmount(self):
        """Cleanup"""
        self.db.close()


def run_tui():
    """Run the TUI application"""
    app = SmartNoteApp()
    app.run()
