import json
import random
from pathlib import Path

class QuoteManager:
    def __init__(self, quotes_file='quotes.json'):
        self.quotes_file = quotes_file
        self.quotes = self.load_quotes()
    
    def load_quotes(self):
        """Load quotes from JSON file"""
        try:
            with open(self.quotes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.quotes_file} not found")
            return []
    
    def save_quotes(self):
        """Save quotes back to JSON file"""
        with open(self.quotes_file, 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=2)
    
    def get_random_quote(self, mark_used=True):
        """Get a random unused quote"""
        unused_quotes = [q for q in self.quotes if not q.get('used', False)]
        
        if not unused_quotes:
            # Reset all quotes if all are used
            for quote in self.quotes:
                quote['used'] = False
            unused_quotes = self.quotes
        
        quote = random.choice(unused_quotes)
        
        if mark_used:
            quote['used'] = True
            self.save_quotes()
        
        return quote
    
    def get_quote_by_id(self, quote_id):
        """Get specific quote by ID"""
        for quote in self.quotes:
            if quote['id'] == quote_id:
                return quote
        return None
    
    def add_quote(self, text, author="અજ્ઞાત", category="general"):
        """Add new quote to collection"""
        new_id = max([q['id'] for q in self.quotes]) + 1 if self.quotes else 1
        new_quote = {
            "id": new_id,
            "text": text,
            "author": author,
            "category": category,
            "used": False
        }
        self.quotes.append(new_quote)
        self.save_quotes()
        return new_quote
