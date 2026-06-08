"""
Unit tests for AI engine module
"""

import pytest
from smartnote.ai_engine import AIEngine, AIConfig


class TestAIEngine:
    """Test cases for AIEngine"""
    
    @pytest.fixture
    def ai(self):
        """Create AI engine instance"""
        return AIEngine()
    
    def test_fallback_tags(self, ai):
        """Test fallback tag generation"""
        tags = ai._fallback_tags("Python Tutorial", "Learn Python programming", 5)
        assert isinstance(tags, list)
        assert len(tags) <= 5
        assert "python" in tags
    
    def test_fallback_summary(self, ai):
        """Test fallback summary generation"""
        content = "This is a test. It has multiple sentences. Here is another one."
        summary = ai._fallback_summary(content, 50)
        assert len(summary) <= 50
        assert "test" in summary.lower()
    
    def test_fallback_category(self, ai):
        """Test fallback category classification"""
        category = ai._fallback_category("Code Review", "Check the function implementation")
        assert category in ["development", "project", "reference", "general"]
    
    def test_fallback_sentiment(self, ai):
        """Test fallback sentiment analysis"""
        result = ai._fallback_sentiment("This is great and amazing!")
        assert "sentiment" in result
        assert "confidence" in result
        assert result["sentiment"] == "positive"
    
    def test_fallback_keywords(self, ai):
        """Test fallback keyword extraction"""
        keywords = ai._fallback_keywords("Python programming tutorial for beginners", 5)
        assert isinstance(keywords, list)
        assert len(keywords) <= 5
        assert "python" in keywords
    
    def test_is_available_without_service(self, ai):
        """Test availability check without service"""
        result = ai.is_available()
        assert isinstance(result, bool)
    
    def test_generate_tags_fallback(self, ai):
        """Test tag generation with fallback"""
        tags = ai.generate_tags("Python Code", "def hello(): print('world')", 3)
        assert isinstance(tags, list)
        assert len(tags) <= 3
    
    def test_generate_summary_fallback(self, ai):
        """Test summary generation with fallback"""
        summary = ai.generate_summary("Title", "This is content. More content here.")
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_suggest_category_fallback(self, ai):
        """Test category suggestion with fallback"""
        category = ai.suggest_category("Meeting Notes", "Discussed project timeline")
        assert isinstance(category, str)
        assert len(category) > 0
