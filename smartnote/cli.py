"""
CLI module for SmartNote-CLI
Command-line interface using Click
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

import click

from .database import NoteDatabase
from .ai_engine import AIEngine, AIConfig
from .tui_app import run_tui


PASS_DB = click.make_pass_decorator(NoteDatabase)


@click.group()
@click.option("--db-path", type=click.Path(), help="Custom database path")
@click.pass_context
def cli(ctx, db_path):
    """SmartNote-CLI - AI-Powered Markdown Note Manager
    
    A terminal-based intelligent note-taking application with AI-enhanced features.
    """
    ctx.ensure_object(dict)
    ctx.obj["db"] = NoteDatabase(db_path)
    ctx.obj["ai"] = AIEngine()


@cli.command()
@click.argument("title")
@click.option("--content", "-c", help="Note content")
@click.option("--file", "-f", type=click.Path(exists=True), help="Read content from file")
@click.option("--tags", "-t", help="Comma-separated tags")
@click.option("--category", "-cat", default="general", help="Note category")
@click.option("--ai", "use_ai", is_flag=True, help="Use AI to generate tags and summary")
@click.pass_context
def add(ctx, title, content, file, tags, category, use_ai):
    """Add a new note"""
    db = ctx.obj["db"]
    ai = ctx.obj["ai"]
    
    if file:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
    
    if not content:
        content = click.edit("") or ""
    
    if not content.strip():
        click.echo("Error: Note content cannot be empty", err=True)
        return
    
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    summary = None
    
    if use_ai:
        click.echo("🤖 AI is analyzing your note...")
        if not tag_list:
            tag_list = ai.generate_tags(title, content)
            click.echo(f"✨ Generated tags: {', '.join(tag_list)}")
        summary = ai.generate_summary(title, content)
        category = ai.suggest_category(title, content)
        click.echo(f"📂 Suggested category: {category}")
    
    note_id = db.create_note(
        title=title,
        content=content,
        tags=tag_list,
        category=category,
        summary=summary
    )
    
    click.echo(f"✅ Note created with ID: {note_id}")


@cli.command()
@click.option("--category", "-c", help="Filter by category")
@click.option("--tag", "-t", help="Filter by tag")
@click.option("--favorite", "-f", is_flag=True, help="Show favorites only")
@click.option("--archived", "-a", is_flag=True, help="Show archived notes")
@click.option("--limit", "-l", default=20, help="Limit results")
@click.pass_context
def list(ctx, category, tag, favorite, archived, limit):
    """List all notes"""
    db = ctx.obj["db"]
    
    notes = db.get_all_notes(
        category=category,
        tag=tag,
        favorite_only=favorite,
        archived=archived
    )
    
    if not notes:
        click.echo("No notes found.")
        return
    
    click.echo(f"\n{'ID':<6}{'Title':<30}{'Category':<12}{'Tags':<25}{'Words':<8}{'Updated'}")
    click.echo("-" * 95)
    
    for note in notes[:limit]:
        tags = ", ".join(json.loads(note["tags"]))[:22]
        fav = "★" if note["is_favorite"] else " "
        title = note["title"][:28]
        click.echo(
            f"{note['id']:<6}{fav}{title:<29}{note['category']:<12}"
            f"{tags:<25}{note['word_count']:<8}{note['updated_at'][:10]}"
        )
    
    if len(notes) > limit:
        click.echo(f"\n... and {len(notes) - limit} more notes")


@cli.command()
@click.argument("query")
@click.pass_context
def search(ctx, query):
    """Search notes by content"""
    db = ctx.obj["db"]
    
    notes = db.search_notes(query)
    
    if not notes:
        click.echo(f"No notes found for '{query}'")
        return
    
    click.echo(f"\nFound {len(notes)} note(s) matching '{query}':\n")
    
    for note in notes:
        click.echo(f"[{note['id']}] {note['title']}")
        click.echo(f"    Category: {note['category']} | Tags: {', '.join(json.loads(note['tags']))}")
        if note["summary"]:
            click.echo(f"    Summary: {note['summary'][:100]}...")
        click.echo()


@cli.command()
@click.argument("note_id", type=int)
@click.pass_context
def show(ctx, note_id):
    """Show note details"""
    db = ctx.obj["db"]
    
    note = db.get_note(note_id)
    if not note:
        click.echo(f"Note {note_id} not found", err=True)
        return
    
    click.echo(f"\n{'='*60}")
    click.echo(f"📄 {note['title']}")
    click.echo(f"{'='*60}")
    click.echo(f"Category: {note['category']}")
    click.echo(f"Tags: {', '.join(json.loads(note['tags']))}")
    click.echo(f"Words: {note['word_count']}")
    click.echo(f"Favorite: {'Yes' if note['is_favorite'] else 'No'}")
    click.echo(f"Created: {note['created_at']}")
    click.echo(f"Updated: {note['updated_at']}")
    if note["summary"]:
        click.echo(f"\nSummary: {note['summary']}")
    click.echo(f"\n{'-'*60}")
    click.echo(note["content"])
    click.echo(f"{'='*60}\n")


@cli.command()
@click.argument("note_id", type=int)
@click.option("--title", "-t", help="New title")
@click.option("--content", "-c", help="New content")
@click.option("--tags", help="New tags (comma-separated)")
@click.option("--category", "-cat", help="New category")
@click.pass_context
def edit(ctx, note_id, title, content, tags, category):
    """Edit an existing note"""
    db = ctx.obj["db"]
    
    note = db.get_note(note_id)
    if not note:
        click.echo(f"Note {note_id} not found", err=True)
        return
    
    if not content and not title and not tags and not category:
        # Interactive edit
        new_content = click.edit(note["content"])
        if new_content is not None:
            content = new_content
    
    tag_list = None
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    
    db.update_note(
        note_id=note_id,
        title=title,
        content=content,
        tags=tag_list,
        category=category
    )
    
    click.echo(f"✅ Note {note_id} updated")


@cli.command()
@click.argument("note_id", type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this note?")
@click.pass_context
def delete(ctx, note_id):
    """Delete a note"""
    db = ctx.obj["db"]
    
    if db.delete_note(note_id):
        click.echo(f"✅ Note {note_id} deleted")
    else:
        click.echo(f"Note {note_id} not found", err=True)


@cli.command()
@click.argument("note_id", type=int)
@click.pass_context
def favorite(ctx, note_id):
    """Toggle favorite status"""
    db = ctx.obj["db"]
    
    if db.toggle_favorite(note_id):
        note = db.get_note(note_id)
        status = "favorited" if note["is_favorite"] else "unfavorited"
        click.echo(f"✅ Note {note_id} {status}")
    else:
        click.echo(f"Note {note_id} not found", err=True)


@cli.command()
@click.argument("note_id", type=int)
@click.pass_context
def archive(ctx, note_id):
    """Archive/unarchive a note"""
    db = ctx.obj["db"]
    
    if db.archive_note(note_id):
        note = db.get_note(note_id)
        status = "archived" if note["is_archived"] else "unarchived"
        click.echo(f"✅ Note {note_id} {status}")
    else:
        click.echo(f"Note {note_id} not found", err=True)


@cli.command()
@click.pass_context
def stats(ctx):
    """Show database statistics"""
    db = ctx.obj["db"]
    stats = db.get_stats()
    
    click.echo("\n📊 SmartNote Statistics")
    click.echo("=" * 40)
    click.echo(f"Total Notes:     {stats['total_notes']}")
    click.echo(f"Favorite Notes:  {stats['favorite_notes']}")
    click.echo(f"Total Tags:      {stats['total_tags']}")
    click.echo(f"Total Words:     {stats['total_words']:,}")
    click.echo(f"Categories:      {stats['total_categories']}")
    click.echo("=" * 40)


@cli.command()
@click.option("--format", "fmt", type=click.Choice(["json", "markdown"]), default="markdown")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.pass_context
def export(ctx, fmt, output):
    """Export notes to file"""
    db = ctx.obj["db"]
    
    content = db.export_notes(fmt)
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
        click.echo(f"✅ Notes exported to {output}")
    else:
        click.echo(content)


@cli.command()
@click.option("--model", "-m", default="llama3.2", help="Ollama model name")
@click.option("--url", "-u", default="http://localhost:11434", help="Ollama API URL")
@click.pass_context
def config(ctx, model, url):
    """Configure AI settings"""
    config_path = Path.home() / ".smartnote" / "config.json"
    config_path.parent.mkdir(exist_ok=True)
    
    config = {
        "ai_provider": "ollama",
        "ai_model": model,
        "ai_url": url
    }
    
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    click.echo(f"✅ Configuration saved to {config_path}")
    click.echo(f"   Model: {model}")
    click.echo(f"   URL: {url}")


@cli.command()
@click.pass_context
def tags(ctx):
    """List all tags"""
    db = ctx.obj["db"]
    tags = db.get_tags()
    
    if not tags:
        click.echo("No tags found.")
        return
    
    click.echo(f"\n{'Tag':<20}{'Usage':<10}{'Created'}")
    click.echo("-" * 50)
    
    for tag in tags:
        click.echo(f"{tag['name']:<20}{tag['usage_count']:<10}{tag['created_at'][:10]}")


@cli.command()
@click.pass_context
def tui(ctx):
    """Launch interactive TUI"""
    run_tui()


@cli.command()
@click.argument("note_id", type=int)
@click.pass_context
def analyze(ctx, note_id):
    """AI analyze a note"""
    db = ctx.obj["db"]
    ai = ctx.obj["ai"]
    
    note = db.get_note(note_id)
    if not note:
        click.echo(f"Note {note_id} not found", err=True)
        return
    
    click.echo(f"\n🤖 Analyzing: {note['title']}\n")
    
    # Generate tags
    tags = ai.generate_tags(note["title"], note["content"])
    click.echo(f"🏷️  Suggested Tags: {', '.join(tags)}")
    
    # Generate summary
    summary = ai.generate_summary(note["title"], note["content"])
    click.echo(f"📝 Summary: {summary}")
    
    # Suggest category
    category = ai.suggest_category(note["title"], note["content"])
    click.echo(f"📂 Suggested Category: {category}")
    
    # Sentiment analysis
    sentiment = ai.analyze_sentiment(note["content"])
    click.echo(f"😊 Sentiment: {sentiment['sentiment']} (confidence: {sentiment['confidence']})")
    
    # Keywords
    keywords = ai.extract_keywords(note["content"])
    click.echo(f"🔑 Keywords: {', '.join(keywords)}")


def main():
    """Entry point"""
    cli()


if __name__ == "__main__":
    main()
