"""
AI Engine module for SmartNote-CLI
Provides intelligent features: auto-tagging, summarization, and content analysis
Supports both local Ollama and remote API models
"""

import re
import json
import urllib.request
import urllib.error
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class AIConfig:
    """AI engine configuration"""
    provider: str = "ollama"  # ollama, openai, anthropic
    model: str = "llama3.2"
    api_url: str = "http://localhost:11434"
    api_key: Optional[str] = None
    timeout: int = 30
    max_tokens: int = 500


class AIEngine:
    """AI-powered content analysis engine"""
    
    # Common technical and general tags for fallback
    COMMON_TAGS = [
        "python", "javascript", "typescript", "rust", "go", "java",
        "react", "vue", "angular", "node", "docker", "kubernetes",
        "api", "database", "frontend", "backend", "devops", "testing",
        "security", "performance", "architecture", "design", "tutorial",
        "bugfix", "feature", "refactor", "documentation", "meeting",
        "idea", "research", "learning", "project", "personal"
    ]
    
    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or AIConfig()
        self._available = None
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        if self._available is not None:
            return self._available
        
        if self.config.provider == "ollama":
            try:
                req = urllib.request.Request(
                    f"{self.config.api_url}/api/tags",
                    method="GET"
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    self._available = response.status == 200
                    return self._available
            except Exception:
                self._available = False
                return False
        
        self._available = bool(self.config.api_key)
        return self._available
    
    def _call_ollama(self, prompt: str, system: str = None) -> str:
        """Call Ollama API"""
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": self.config.max_tokens
            }
        }
        
        if system:
            payload["system"] = system
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.config.api_url}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "")
    
    def generate_tags(self, title: str, content: str, max_tags: int = 5) -> List[str]:
        """Generate relevant tags for a note"""
        if not self.is_available():
            return self._fallback_tags(title, content, max_tags)
        
        try:
            prompt = f"""Given this note title and content, generate {max_tags} relevant tags.
Tags should be lowercase, single words or short phrases (max 2 words).
Return ONLY a JSON array of strings.

Title: {title}
Content: {content[:1000]}

Tags:"""
            
            system = "You are a helpful assistant that generates relevant tags for notes. Always return valid JSON array."
            response = self._call_ollama(prompt, system)
            
            # Extract JSON array from response
            json_match = re.search(r'\[.*?\]', response, re.DOTALL)
            if json_match:
                tags = json.loads(json_match.group())
                return [t.lower().strip() for t in tags[:max_tags]]
            
            return self._fallback_tags(title, content, max_tags)
        
        except Exception:
            return self._fallback_tags(title, content, max_tags)
    
    def generate_summary(self, title: str, content: str, max_length: int = 150) -> str:
        """Generate a concise summary of note content"""
        if not self.is_available():
            return self._fallback_summary(content, max_length)
        
        try:
            prompt = f"""Summarize the following note in {max_length} characters or less.
Be concise and capture the key points.

Title: {title}
Content: {content[:2000]}

Summary:"""
            
            system = "You are a helpful assistant that creates concise summaries."
            response = self._call_ollama(prompt, system)
            
            summary = response.strip()
            if len(summary) > max_length:
                summary = summary[:max_length].rsplit(" ", 1)[0] + "..."
            
            return summary
        
        except Exception:
            return self._fallback_summary(content, max_length)
    
    def suggest_category(self, title: str, content: str) -> str:
        """Suggest a category for the note"""
        categories = [
            "development", "design", "research", "meeting",
            "learning", "personal", "project", "reference"
        ]
        
        if not self.is_available():
            return self._fallback_category(title, content)
        
        try:
            prompt = f"""Classify this note into one category from: {', '.join(categories)}.
Return ONLY the category name.

Title: {title}
Content: {content[:1000]}

Category:"""
            
            system = f"You classify notes into categories. Choose from: {', '.join(categories)}"
            response = self._call_ollama(prompt, system)
            
            category = response.strip().lower()
            if category in categories:
                return category
            
            return self._fallback_category(title, content)
        
        except Exception:
            return self._fallback_category(title, content)
    
    def analyze_sentiment(self, content: str) -> Dict:
        """Analyze sentiment of note content"""
        if not self.is_available():
            return self._fallback_sentiment(content)
        
        try:
            prompt = f"""Analyze the sentiment of this text.
Return ONLY a JSON object with keys: sentiment (positive/neutral/negative), confidence (0-1), keywords (array of important words).

Text: {content[:1000]}

Analysis:"""
            
            system = "You analyze text sentiment. Always return valid JSON."
            response = self._call_ollama(prompt, system)
            
            json_match = re.search(r'\{.*?\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return self._fallback_sentiment(content)
        
        except Exception:
            return self._fallback_sentiment(content)
    
    def extract_keywords(self, content: str, max_keywords: int = 10) -> List[str]:
        """Extract key terms from content"""
        if not self.is_available():
            return self._fallback_keywords(content, max_keywords)
        
        try:
            prompt = f"""Extract {max_keywords} important keywords from this text.
Return ONLY a JSON array of strings.

Text: {content[:1500]}

Keywords:"""
            
            system = "You extract keywords from text. Always return valid JSON array."
            response = self._call_ollama(prompt, system)
            
            json_match = re.search(r'\[.*?\]', response, re.DOTALL)
            if json_match:
                keywords = json.loads(json_match.group())
                return [k.lower().strip() for k in keywords[:max_keywords]]
            
            return self._fallback_keywords(content, max_keywords)
        
        except Exception:
            return self._fallback_keywords(content, max_keywords)
    
    # Fallback methods when AI is unavailable
    def _fallback_tags(self, title: str, content: str, max_tags: int) -> List[str]:
        """Generate tags using keyword matching"""
        text = (title + " " + content).lower()
        tags = []
        
        for tag in self.COMMON_TAGS:
            if tag in text and tag not in tags:
                tags.append(tag)
        
        # Add generic tags based on content length
        if len(content) > 1000:
            tags.append("detailed")
        if "TODO" in content or "todo" in content:
            tags.append("todo")
        if "http" in content:
            tags.append("reference")
        
        return tags[:max_tags] or ["general"]
    
    def _fallback_summary(self, content: str, max_length: int) -> str:
        """Generate summary by taking first sentences"""
        sentences = content.split(".")
        summary = ""
        for sentence in sentences:
            if len(summary) + len(sentence) < max_length:
                summary += sentence + "."
            else:
                break
        
        if not summary:
            summary = content[:max_length].rsplit(" ", 1)[0] + "..."
        
        return summary.strip()
    
    def _fallback_category(self, title: str, content: str) -> str:
        """Categorize based on keyword matching"""
        text = (title + " " + content).lower()
        
        category_keywords = {
            "development": ["code", "program", "function", "api", "bug", "debug", "git"],
            "design": ["ui", "ux", "interface", "mockup", "prototype", "figma"],
            "research": ["study", "analysis", "investigate", "paper", "survey"],
            "meeting": ["meeting", "discuss", "agenda", "minutes", "call"],
            "learning": ["learn", "tutorial", "course", "book", "study"],
            "personal": ["idea", "thought", "plan", "goal", "diary"],
            "project": ["project", "milestone", "task", "deliverable", "timeline"],
            "reference": ["doc", "link", "resource", "cheatsheet", "guide"]
        }
        
        scores = {cat: 0 for cat in category_keywords}
        for category, keywords in category_keywords.items():
            for kw in keywords:
                scores[category] += text.count(kw)
        
        best_category = max(scores, key=scores.get)
        return best_category if scores[best_category] > 0 else "general"
    
    def _fallback_sentiment(self, content: str) -> Dict:
        """Simple sentiment analysis"""
        positive_words = ["good", "great", "excellent", "amazing", "love", "best",
                         "awesome", "fantastic", "perfect", "happy", "success"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "error",
                         "fail", "bug", "issue", "problem", "broken", "sad"]
        
        text = content.lower()
        pos_count = sum(text.count(w) for w in positive_words)
        neg_count = sum(text.count(w) for w in negative_words)
        
        if pos_count > neg_count:
            sentiment = "positive"
            confidence = min(0.5 + (pos_count - neg_count) * 0.1, 0.95)
        elif neg_count > pos_count:
            sentiment = "negative"
            confidence = min(0.5 + (neg_count - pos_count) * 0.1, 0.95)
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 2),
            "keywords": self._fallback_keywords(content, 5)
        }
    
    def _fallback_keywords(self, content: str, max_keywords: int) -> List[str]:
        """Extract keywords by frequency"""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        stop_words = {"this", "that", "with", "from", "they", "have", "were",
                      "been", "their", "said", "each", "which", "will", "about"}
        
        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:max_keywords]]
