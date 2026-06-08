"""
Database module for SmartNote-CLI
Handles SQLite operations for notes, tags, and metadata
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class NoteDatabase:
    """SQLite database manager for notes"""
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            config_dir = Path.home() / ".smartnote"
            config_dir.mkdir(exist_ok=True)
            db_path = config_dir / "notes.db"
        
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()
    
    def _init_tables(self):
        """Initialize database tables"""
        cursor = self.conn.cursor()
        
        # Notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT DEFAULT '[]',
                category TEXT DEFAULT 'general',
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                word_count INTEGER DEFAULT 0,
                is_favorite INTEGER DEFAULT 0,
                is_archived INTEGER DEFAULT 0
            )
        """)
        
        # Tags table for efficient tag management
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#6366f1',
                usage_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Note-Tag relationship table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS note_tags (
                note_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
                PRIMARY KEY (note_id, tag_id)
            )
        """)
        
        # Note: FTS5 triggers can cause issues with some SQLite versions
        # Using simple FTS5 without triggers for better compatibility
        try:
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
                    title, content, content_rowid=rowid
                )
            """)
        except sqlite3.OperationalError:
            pass  # FTS5 may not be available
        
        self.conn.commit()
    
    def create_note(self, title: str, content: str, tags: List[str] = None,
                    category: str = "general", summary: str = None) -> int:
        """Create a new note"""
        cursor = self.conn.cursor()
        word_count = len(content.split())
        tags_json = json.dumps(tags or [])
        
        cursor.execute("""
            INSERT INTO notes (title, content, tags, category, summary, word_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, content, tags_json, category, summary, word_count))
        
        note_id = cursor.lastrowid
        
        # Add tags
        if tags:
            for tag in tags:
                self._add_tag(tag)
                self._link_tag_to_note(note_id, tag)
        
        self.conn.commit()
        return note_id
    
    def _add_tag(self, tag_name: str):
        """Add a tag if it doesn't exist"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO tags (name) VALUES (?)
        """, (tag_name,))
        cursor.execute("""
            UPDATE tags SET usage_count = usage_count + 1 WHERE name = ?
        """, (tag_name,))
        self.conn.commit()
    
    def _link_tag_to_note(self, note_id: int, tag_name: str):
        """Link a tag to a note"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
        tag_id = cursor.fetchone()[0]
        cursor.execute("""
            INSERT OR IGNORE INTO note_tags (note_id, tag_id) VALUES (?, ?)
        """, (note_id, tag_id))
        self.conn.commit()
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """Get a single note by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def get_all_notes(self, category: str = None, tag: str = None,
                      favorite_only: bool = False, archived: bool = False) -> List[Dict]:
        """Get all notes with optional filtering"""
        cursor = self.conn.cursor()
        query = "SELECT * FROM notes WHERE is_archived = ?"
        params = [1 if archived else 0]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if favorite_only:
            query += " AND is_favorite = 1"
        
        if tag:
            query += " AND tags LIKE ?"
            params.append(f'%"{tag}"%')
        
        query += " ORDER BY updated_at DESC"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def search_notes(self, query: str) -> List[Dict]:
        """Search notes using LIKE search (FTS5 fallback)"""
        cursor = self.conn.cursor()
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT * FROM notes
            WHERE (title LIKE ? OR content LIKE ?) AND is_archived = 0
            ORDER BY updated_at DESC
        """, (search_term, search_term))
        return [dict(row) for row in cursor.fetchall()]
    
    def update_note(self, note_id: int, title: str = None, content: str = None,
                    tags: List[str] = None, category: str = None,
                    summary: str = None) -> bool:
        """Update an existing note"""
        cursor = self.conn.cursor()
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        
        if content is not None:
            updates.append("content = ?")
            params.append(content)
            updates.append("word_count = ?")
            params.append(len(content.split()))
        
        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))
        
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        
        if summary is not None:
            updates.append("summary = ?")
            params.append(summary)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(note_id)
        
        query = f"UPDATE notes SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM note_tags WHERE note_id = ?", (note_id,))
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def toggle_favorite(self, note_id: int) -> bool:
        """Toggle favorite status"""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE notes SET is_favorite = CASE WHEN is_favorite = 1 THEN 0 ELSE 1 END WHERE id = ?", (note_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def archive_note(self, note_id: int) -> bool:
        """Archive/unarchive a note"""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE notes SET is_archived = CASE WHEN is_archived = 1 THEN 0 ELSE 1 END WHERE id = ?", (note_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM notes ORDER BY category")
        return [row[0] for row in cursor.fetchall()]
    
    def get_tags(self) -> List[Dict]:
        """Get all tags with usage counts"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tags ORDER BY usage_count DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        cursor = self.conn.cursor()
        stats = {}
        
        cursor.execute("SELECT COUNT(*) FROM notes WHERE is_archived = 0")
        stats['total_notes'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM notes WHERE is_favorite = 1")
        stats['favorite_notes'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tags")
        stats['total_tags'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(word_count) FROM notes")
        stats['total_words'] = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(DISTINCT category) FROM notes")
        stats['total_categories'] = cursor.fetchone()[0]
        
        return stats
    
    def export_notes(self, format_type: str = "json") -> str:
        """Export all notes to JSON or Markdown"""
        notes = self.get_all_notes()
        
        if format_type == "json":
            return json.dumps(notes, indent=2, default=str)
        elif format_type == "markdown":
            md_content = "# SmartNote Export\n\n"
            for note in notes:
                md_content += f"## {note['title']}\n\n"
                md_content += f"**Category:** {note['category']}  \n"
                md_content += f"**Tags:** {', '.join(json.loads(note['tags']))}  \n"
                md_content += f"**Created:** {note['created_at']}  \n\n"
                md_content += f"{note['content']}\n\n"
                md_content += "---\n\n"
            return md_content
        
        return ""
    
    def close(self):
        """Close database connection"""
        self.conn.close()
