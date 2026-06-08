"""
Unit tests for database module
"""

import os
import tempfile
import pytest
from smartnote.database import NoteDatabase


class TestNoteDatabase:
    """Test cases for NoteDatabase"""
    
    @pytest.fixture
    def db(self):
        """Create temporary database"""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        database = NoteDatabase(path)
        yield database
        database.close()
        os.unlink(path)
    
    def test_create_note(self, db):
        """Test creating a note"""
        note_id = db.create_note(
            title="Test Note",
            content="This is a test note content",
            tags=["test", "demo"],
            category="testing"
        )
        assert note_id > 0
        
        note = db.get_note(note_id)
        assert note["title"] == "Test Note"
        assert note["category"] == "testing"
    
    def test_get_all_notes(self, db):
        """Test retrieving all notes"""
        db.create_note("Note 1", "Content 1")
        db.create_note("Note 2", "Content 2")
        
        notes = db.get_all_notes()
        assert len(notes) == 2
    
    def test_search_notes(self, db):
        """Test searching notes"""
        db.create_note("Python Guide", "Learn Python programming")
        db.create_note("Rust Tips", "Rust programming tips")
        
        results = db.search_notes("Python")
        assert len(results) == 1
        assert results[0]["title"] == "Python Guide"
    
    def test_update_note(self, db):
        """Test updating a note"""
        note_id = db.create_note("Original", "Original content")
        
        db.update_note(note_id, title="Updated")
        note = db.get_note(note_id)
        assert note["title"] == "Updated"
    
    def test_delete_note(self, db):
        """Test deleting a note"""
        note_id = db.create_note("To Delete", "Content")
        assert db.delete_note(note_id)
        assert db.get_note(note_id) is None
    
    def test_toggle_favorite(self, db):
        """Test toggling favorite status"""
        note_id = db.create_note("Favorite", "Content")
        
        db.toggle_favorite(note_id)
        note = db.get_note(note_id)
        assert note["is_favorite"] == 1
    
    def test_archive_note(self, db):
        """Test archiving a note"""
        note_id = db.create_note("Archive", "Content")
        
        db.archive_note(note_id)
        note = db.get_note(note_id)
        assert note["is_archived"] == 1
    
    def test_get_stats(self, db):
        """Test getting statistics"""
        db.create_note("Note 1", "Content one two three")
        db.create_note("Note 2", "Content four five six")
        
        stats = db.get_stats()
        assert stats["total_notes"] == 2
        assert stats["total_words"] >= 6
    
    def test_export_notes(self, db):
        """Test exporting notes"""
        db.create_note("Export", "Export content")
        
        json_export = db.export_notes("json")
        assert "Export" in json_export
        
        md_export = db.export_notes("markdown")
        assert "# SmartNote Export" in md_export
