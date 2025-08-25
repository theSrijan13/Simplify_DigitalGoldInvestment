from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sqlite3
import uuid
from datetime import datetime
import os
import google.generativeai as genai
from contextlib import contextmanager
import re
import streamlit as st

# Initialize FastAPI
app = FastAPI(
    title="Digital Gold Investment API",
    description="Simplify Money's Digital Gold Investment Workflow with AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Database setup
DATABASE_PATH = "digital_gold.db"

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create gold_purchases table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gold_purchases (
            purchase_id TEXT PRIMARY KEY,
            user_id INTEGER,
            amount DECIMAL(10,2),
            status TEXT DEFAULT 'SUCCESS',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Pydantic models
class UserQuery(BaseModel):
    user_id: int
    query: str
    user_name: Optional[str] = "Friend"

class PurchaseRequest(BaseModel):
    user_id: int
    amount: float = 10.0
    user_name: Optional[str] = "Friend"

class LLMResponse(BaseModel):
    is_gold_related: bool
    response: str
    suggests_purchase: bool
    confidence: float

class PurchaseResponse(BaseModel):
    success: bool
    transaction_id: str
    amount: float
    message: str

# AI Integration
class GoldInvestmentAI:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def analyze_query(self, query: str, user_name: str = "Friend") -> LLMResponse:
        """Analyze if query is gold investment related and generate response"""
        
        prompt = f"""
        You are an AI assistant for Simplify Money, a digital investment platform. 
        A user named {user_name} has asked: "{query}"
        
        Your task:
        1. Determine if this query is related to gold investment, digital gold, or investment advice
        2. If YES, provide a friendly, engaging response that:
           - Educates about digital gold benefits
           - Uses a trendy, Gen-Z friendly tone with emojis
           - Encourages investment through Simplify Money
           - Ends with asking if they want to make a purchase
        3. If NO, politely redirect them to gold investment topics
        
        Format your response as JSON:
        {{
            "is_gold_related": true/false,
            "response": "your response text",
            "suggests_purchase": true/false,
            "confidence": 0.0-1.0
        }}
        
        Example good response for gold queries:
        "Heyyy {user_name}! 💫 Digital gold is the smartest way to invest rn 🌟
        ✨ Benefits:
        - Super low entry (just ₹10!)
        - Zero storage hassles 
        - 24/7 liquidity
        - Hedge against inflation 📈
        
        Pro tip: Simplify Money lets you buy instantly with zero fees! 💯
        Ready to start your gold journey? 🚀"
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                import json
                result = json.loads(json_match.group())
                return LLMResponse(**result)
            else:
                # Fallback response
                return LLMResponse(
                    is_gold_related=True,
                    response=f"Hey {user_name}! 💫 Let's talk about digital gold investment! It's a smart way to diversify your portfolio. Want to start with just ₹10?",
                    suggests_purchase=True,
                    confidence=0.8
                )
                
        except Exception as e:
            # Fallback for API issues
            return LLMResponse(
                is_gold_related=True,
                response=f"Heyyy {user_name}! 💫 Digital gold is the smartest way to invest rn 🌟\n✨ Low entry point (₹10)\n💎 Zero storage drama\n🚀 Easy liquidity\nPro Tip: Simplify Money lets you buy instantly! 💯\nWant to purchase digital gold?",
                suggests_purchase=True,
                confidence=0.9
            )

# Initialize AI and Database
ai_assistant = GoldInvestmentAI()
init_database()

# API Routes

@app.get("/")
async def root():
    return {"message": "Digital Gold Investment API - Simplify Money", "status": "active"}

@app.post("/api/v1/llm-interaction", response_model=Dict[str, Any])
async def llm_interaction(query: UserQuery):
    """
    API 1: LLM Interaction - Analyze user query and provide gold investment advice
    """
    try:
        # Analyze query with AI
        llm_response = ai_assistant.analyze_query(query.query, query.user_name or "Friend")
        
        return {
            "user_id": query.user_id,
            "original_query": query.query,
            "is_gold_related": llm_response.is_gold_related,
            "ai_response": llm_response.response,
            "suggests_purchase": llm_response.suggests_purchase,
            "confidence": llm_response.confidence,
            "next_action": "purchase" if llm_response.suggests_purchase else "continue_conversation"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM interaction failed: {str(e)}")

@app.post("/api/v1/purchase-gold", response_model=PurchaseResponse)
async def purchase_digital_gold(purchase: PurchaseRequest):
    """
    API 2: Digital Gold Purchase - Simulate gold purchase and store in database
    """
    try:
        # Validate amount
        if purchase.amount < 10:
            raise HTTPException(status_code=400, detail="Minimum investment amount is ₹10")
        
        if purchase.amount > 100000:
            raise HTTPException(status_code=400, detail="Maximum investment amount is ₹1,00,000")
        
        # Generate transaction ID
        transaction_id = f"G{uuid.uuid4().hex[:8].upper()}"
        
        # Insert purchase into database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO gold_purchases (purchase_id, user_id, amount, status, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (transaction_id, purchase.user_id, purchase.amount, 'SUCCESS', datetime.now()))
            conn.commit()
        
        # Generate success message
        success_message = f"🎉 Woohoo {purchase.user_name}! Your digital gold purchase of ₹{purchase.amount} was successful!\n✅ Transaction ID: {transaction_id}\n💎 Welcome to the gold gang! 🚀"
        
        return PurchaseResponse(
            success=True,
            transaction_id=transaction_id,
            amount=purchase.amount,
            message=success_message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Purchase failed: {str(e)}")

@app.get("/api/v1/user/{user_id}/purchases")
async def get_user_purchases(user_id: int):
    """Get all purchases for a specific user"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT purchase_id, amount, status, timestamp 
                FROM gold_purchases 
                WHERE user_id = ?
                ORDER BY timestamp DESC
            ''', (user_id,))
            
            purchases = []
            for row in cursor.fetchall():
                purchases.append({
                    "transaction_id": row["purchase_id"],
                    "amount": float(row["amount"]),
                    "status": row["status"],
                    "timestamp": row["timestamp"]
                })
            
            return {
                "user_id": user_id,
                "total_purchases": len(purchases),
                "purchases": purchases
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch purchases: {str(e)}")

@app.get("/api/v1/admin/stats")
async def get_admin_stats():
    """Admin endpoint to get platform statistics"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Total purchases
            cursor.execute("SELECT COUNT(*) as total_purchases FROM gold_purchases")
            total_purchases = cursor.fetchone()["total_purchases"]
            
            # Total amount invested
            cursor.execute("SELECT SUM(amount) as total_invested FROM gold_purchases")
            total_invested = cursor.fetchone()["total_invested"] or 0
            
            # Recent purchases
            cursor.execute('''
                SELECT purchase_id, user_id, amount, timestamp 
                FROM gold_purchases 
                ORDER BY timestamp DESC 
                LIMIT 10
            ''')
            recent_purchases = []
            for row in cursor.fetchall():
                recent_purchases.append({
                    "transaction_id": row["purchase_id"],
                    "user_id": row["user_id"],
                    "amount": float(row["amount"]),
                    "timestamp": row["timestamp"]
                })
            
            return {
                "total_purchases": total_purchases,
                "total_invested": float(total_invested),
                "recent_purchases": recent_purchases
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
