# import streamlit as st
# import sqlite3
# import json
# import pandas as pd
# from datetime import datetime
# import time
# import re
# import google.generativeai as genai
# from typing import Dict, Any, Optional
# import os

# # Page configuration
# st.set_page_config(
#     page_title="Simplify Money - Digital Gold Investment",
#     page_icon="🪙",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .main-header {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 2rem;
#         border-radius: 10px;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
    
#     .chat-container {
#         background: #f8f9fa;
#         border-radius: 10px;
#         padding: 1rem;
#         max-height: 400px;
#         overflow-y: auto;
#         border: 2px solid #e0e0e0;
#     }
    
#     .user-message {
#         background: linear-gradient(135deg, #667eea, #764ba2);
#         color: white;
#         padding: 10px;
#         border-radius: 10px;
#         margin: 5px 0;
#         text-align: right;
#     }
    
#     .bot-message {
#         background: #e9ecef;
#         color: #333;
#         padding: 10px;
#         border-radius: 10px;
#         margin: 5px 0;
#         border-left: 4px solid #667eea;
#     }
    
#     .gold-price {
#         background: linear-gradient(135deg, #ffd700, #ffed4a);
#         color: #333;
#         padding: 15px;
#         border-radius: 10px;
#         text-align: center;
#         font-weight: bold;
#         font-size: 1.1rem;
#         margin-bottom: 1rem;
#     }
    
#     .success-message {
#         background: linear-gradient(135deg, #28a745, #20c997);
#         color: white;
#         padding: 20px;
#         border-radius: 10px;
#         text-align: center;
#         margin: 1rem 0;
#     }
    
#     .api-status {
#         background: #d4edda;
#         color: #155724;
#         padding: 10px;
#         border-radius: 5px;
#         margin: 5px 0;
#     }
    
#     .ai-powered {
#         background: linear-gradient(135deg, #ff6b6b, #feca57);
#         color: white;
#         padding: 8px 12px;
#         border-radius: 15px;
#         font-size: 0.8rem;
#         font-weight: bold;
#         margin: 5px 0;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Initialize Gemini 2.5 Flash
# @st.cache_resource
# def initialize_gemini():
#     """Initialize Gemini 2.5 Flash model"""
#     try:
#         # Get API key from Streamlit secrets or environment
#         api_key = st.secrets.get("GEMINI_API_KEY")
        
#         if not api_key:
#             st.warning("⚠️ Gemini API key not found. Using fallback responses.")
#             return None
        
#         genai.configure(api_key=api_key)
#         model = genai.GenerativeModel('gemini-2.0-flash-exp')
#         return model
#     except Exception as e:
#         st.error(f"Error initializing Gemini: {str(e)}")
#         return None

# # Database setup
# @st.cache_resource
# def init_database():
#     """Initialize SQLite database"""
#     conn = sqlite3.connect('gold_investment.db', check_same_thread=False)
#     cursor = conn.cursor()
    
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS purchases (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL,
#             phone TEXT NOT NULL,
#             amount REAL NOT NULL,
#             gold_weight REAL NOT NULL,
#             purchase_date TEXT NOT NULL,
#             status TEXT DEFAULT 'Completed'
#         )
#     ''')
    
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS chat_history (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_query TEXT NOT NULL,
#             bot_response TEXT NOT NULL,
#             timestamp TEXT NOT NULL,
#             model_used TEXT DEFAULT 'gemini-2.0-flash'
#         )
#     ''')
    
#     conn.commit()
#     return conn

# # Initialize components
# conn = init_database()
# gemini_model = initialize_gemini()

# def get_current_gold_price() -> float:
#     """Get current gold price (simulated with slight variations)"""
#     base_price = 6250  # ₹ per gram
#     # Add small random variation to simulate market movements
#     import random
#     variation = random.uniform(-50, 50)
#     return round(base_price + variation, 2)

# def get_gold_investment_prompt(user_query: str, gold_price: float) -> str:
#     """Create a specialized prompt for Gemini about gold investments"""
    
#     prompt = f"""
#     You are Kuber AI, a fun and engaging digital gold investment assistant for Simplify Money app. 

#     PERSONALITY TRAITS:
#     - Use trendy language like "bestie", "no cap", "fire", "slay", etc.
#     - Be enthusiastic and supportive about digital gold investments
#     - Use emojis liberally (💫, 🔥, 💸, ✨, 💯, 🚀, etc.)
#     - Sound like a helpful millennial/Gen-Z friend

#     CONTEXT:
#     - Current gold price: ₹{gold_price} per gram
#     - Platform: Simplify Money digital gold investment
#     - Minimum investment: ₹10
#     - Users can buy/sell digital gold instantly
#     - 100% pure 24k gold backing
#     - Zero storage hassles

#     KEY SELLING POINTS:
#     1. Start with just ₹10 (super accessible!)
#     2. No physical storage worries 
#     3. 24k pure gold backing
#     4. Instant buy/sell liquidity
#     5. Convert to physical gold anytime
#     6. Regulated and secure platform

#     INSTRUCTIONS:
#     - Answer the user's question about digital gold investment
#     - Always be positive and encouraging about gold investment
#     - Include relevant facts about digital gold benefits
#     - End with a purchase nudge encouraging them to start investing
#     - Keep response under 150 words
#     - Match the enthusiastic "bestie" tone

#     USER QUESTION: "{user_query}"

#     Respond as Kuber AI:
#     """
#     return prompt

# def get_gemini_response(user_query: str, gold_price: float) -> str:
#     """Get response from Gemini 2.5 Flash"""
#     try:
#         if not gemini_model:
#             return get_fallback_response(user_query)
        
#         prompt = get_gold_investment_prompt(user_query, gold_price)
        
#         # Generate response with Gemini 2.5 Flash
#         response = gemini_model.generate_content(prompt)
        
#         if response and response.text:
#             # Add purchase nudge if not already present
#             ai_response = response.text.strip()
#             if "purchase" not in ai_response.lower() and "invest" in ai_response.lower():
#                 ai_response += "\n\nReady to start your digital gold journey? You can purchase digital gold right here on Simplify Money! 🚀✨"
            
#             return ai_response
#         else:
#             return get_fallback_response(user_query)
            
#     except Exception as e:
#         st.error(f"Gemini API Error: {str(e)}")
#         return get_fallback_response(user_query)

# def get_fallback_response(user_query: str) -> str:
#     """Fallback responses when Gemini is not available"""
#     query = user_query.lower()
    
#     fallback_responses = {
#         'digital gold': "Heyyy bestie! 💫 Digital gold is legit the coolest way to invest right now - no cap! 🔥 It's 24k pure gold that you can buy online without physically storing it. Zero storage drama, maximum gains! 🔒",
#         'invest': "Digital gold is the smartest way to start! 💯 You can begin with just ₹10 - how fire is that? Most investment options require big bucks, but digital gold said 'we're democratic here!' 💸",
#         'price': f"Current gold price is ₹{get_current_gold_price()} per gram! 📈 Digital gold prices are updated real-time with no hidden charges! 💯",
#         'safe': "Absolutely safe, bestie! 🔒 Digital gold on Simplify Money is backed by actual 24k gold in secure vaults. It's insured, audited, and totally legit! 💯",
#         'minimum': "You can start with just ₹10! 💸 That's like a coffee, bestie! Perfect for beginners who want to start investing without breaking the bank! 🌟"
#     }
    
#     for keyword, response in fallback_responses.items():
#         if keyword in query:
#             return response + "\n\nReady to start your gold investment journey? Purchase digital gold right here! 🚀✨"
    
#     return "Hey bestie! 💫 I'm your digital gold investment assistant! Ask me about gold prices, safety, minimum investment, or how to get started! Let's make your money slay! 💸✨"

# # API 1: Gold Investment Q&A Assistant with Gemini 2.5 Flash
# def process_gold_query(user_query: str) -> Dict[str, Any]:
#     """API 1: Process user query about gold investments using Gemini 2.5 Flash"""
    
#     # Simulate API processing
#     time.sleep(0.5)
    
#     try:
#         gold_price = get_current_gold_price()
        
#         # Get AI response from Gemini 2.5 Flash
#         if gemini_model:
#             response = get_gemini_response(user_query, gold_price)
#             model_used = "gemini-2.0-flash"
#         else:
#             response = get_fallback_response(user_query)
#             model_used = "fallback"
        
#         # Store in database
#         cursor = conn.cursor()
#         cursor.execute('''
#             INSERT INTO chat_history (user_query, bot_response, timestamp, model_used)
#             VALUES (?, ?, ?, ?)
#         ''', (user_query, response, datetime.now().isoformat(), model_used))
#         conn.commit()
        
#         return {
#             'response': response,
#             'nudge': True,
#             'status': 'success',
#             'model_used': model_used,
#             'gold_price': gold_price
#         }
        
#     except Exception as e:
#         return {
#             'response': f"Sorry bestie! Something went wrong. Please try again! 💫",
#             'nudge': False,
#             'status': 'error',
#             'error': str(e)
#         }

# # API 2: Digital Gold Purchase System (Enhanced)
# def process_gold_purchase(user_data: Dict[str, Any]) -> Dict[str, Any]:
#     """API 2: Process digital gold purchase with enhanced validation"""
    
#     # Simulate API processing
#     time.sleep(1)
    
#     try:
#         # Validate input
#         required_fields = ['name', 'email', 'phone', 'amount', 'gold_weight']
#         for field in required_fields:
#             if field not in user_data or not user_data[field]:
#                 return {
#                     'success': False,
#                     'error': f'Missing required field: {field}',
#                     'status': 'error'
#                 }
        
#         # Enhanced validation
#         if user_data['amount'] < 10:
#             return {
#                 'success': False,
#                 'error': 'Minimum investment amount is ₹10 bestie! 💸',
#                 'status': 'error'
#             }
        
#         # Email validation
#         email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#         if not re.match(email_pattern, user_data['email']):
#             return {
#                 'success': False,
#                 'error': 'Please enter a valid email address! 📧',
#                 'status': 'error'
#             }
        
#         # Phone validation
#         phone_pattern = r'^[6-9]\d{9}$'
#         clean_phone = re.sub(r'[^\d]', '', user_data['phone'])
#         if not re.match(phone_pattern, clean_phone):
#             return {
#                 'success': False,
#                 'error': 'Please enter a valid 10-digit Indian phone number! 📱',
#                 'status': 'error'
#             }
        
#         # Insert purchase into database
#         cursor = conn.cursor()
#         cursor.execute('''
#             INSERT INTO purchases (name, email, phone, amount, gold_weight, purchase_date, status)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         ''', (
#             user_data['name'].strip(),
#             user_data['email'].strip(),
#             clean_phone,
#             round(user_data['amount'], 2),
#             round(user_data['gold_weight'], 6),
#             datetime.now().isoformat(),
#             'Completed'
#         ))
        
#         purchase_id = cursor.lastrowid
#         conn.commit()
        
#         # Generate success message with AI flair
#         success_message = f"🎉 Yasss bestie! Your digital gold purchase is complete! You're now a gold investor - how fire is that! 💫"
        
#         return {
#             'success': True,
#             'purchase_id': purchase_id,
#             'success_message': success_message,
#             'purchase_details': {
#                 'id': purchase_id,
#                 'name': user_data['name'],
#                 'amount': round(user_data['amount'], 2),
#                 'gold_weight': round(user_data['gold_weight'], 6),
#                 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                 'status': 'Completed'
#             },
#             'status': 'success'
#         }
        
#     except Exception as e:
#         return {
#             'success': False,
#             'error': f'Oops! Something went wrong bestie: {str(e)} 💔',
#             'status': 'error'
#         }

# def get_all_purchases() -> pd.DataFrame:
#     """Get all purchases from database"""
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM purchases ORDER BY id DESC')
    
#     columns = ['ID', 'Name', 'Email', 'Phone', 'Amount (₹)', 'Gold Weight (g)', 'Date', 'Status']
#     data = cursor.fetchall()
    
#     if data:
#         df = pd.DataFrame(data, columns=columns)
#         # Format date and numbers
#         df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d %H:%M')
#         df['Amount (₹)'] = df['Amount (₹)'].round(2)
#         df['Gold Weight (g)'] = df['Gold Weight (g)'].round(6)
#         return df
#     else:
#         return pd.DataFrame(columns=columns)

# def get_chat_history() -> list:
#     """Get chat history from database"""
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT user_query, bot_response, timestamp, model_used 
#         FROM chat_history 
#         ORDER BY id DESC LIMIT 20
#     ''')
#     return cursor.fetchall()

# # Main Streamlit App
# def main():
#     # Header
#     st.markdown("""
#     <div class="main-header">
#         <h1>🪙 Simplify Money</h1>
#         <p>Digital Gold Investment Platform</p>
#         <div class="ai-powered">🤖 Powered by Gemini 2.0 Flash</div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Sidebar
#     st.sidebar.title("🔧 System Status")
    
#     # API Status with model info
#     if gemini_model:
#         st.sidebar.markdown("""
#         <div class="api-status">
#             <strong>🤖 AI Model:</strong> Gemini 2.0 Flash ✅ Active
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         st.sidebar.markdown("""
#         <div style="background: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; margin: 5px 0;">
#             <strong>🤖 AI Model:</strong> Fallback Mode ⚠️
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.sidebar.markdown("""
#     <div class="api-status">
#         <strong>API 1:</strong> Gold Q&A Assistant ✅ Active
#     </div>
#     <div class="api-status">
#         <strong>API 2:</strong> Purchase System ✅ Active  
#     </div>
#     <div class="api-status">
#         <strong>Database:</strong> SQLite ✅ Connected
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Current gold price
#     current_gold_price = get_current_gold_price()
#     st.sidebar.markdown(f"""
#     <div class="gold-price">
#         🏆 Live Gold Price<br>₹{current_gold_price} per gram
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Configuration section
#     with st.sidebar.expander("⚙️ Configuration"):
#         st.info("💡 To use Gemini 2.0 Flash, add your API key in Streamlit secrets or environment variables as 'GEMINI_API_KEY'")
        
#         if st.button("🔄 Refresh AI Model"):
#             st.cache_resource.clear()
#             st.rerun()
    
#     # Main content - two columns
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
#         st.header("💬 AI Gold Investment Assistant")
        
#         # Show AI model status
#         if gemini_model:
#             st.success("🤖 Gemini 2.0 Flash Active - Enhanced AI responses!")
#         else:
#             st.warning("⚠️ Using fallback responses. Add GEMINI_API_KEY for AI-powered chat.")
        
#         # Chat interface
#         if 'chat_messages' not in st.session_state:
#             st.session_state.chat_messages = [
#                 {"type": "bot", "message": "Hey bestie! 💫 I'm Kuber AI powered by Gemini 2.0 Flash! I'm here to help you with digital gold investments. Ask me anything! 🚀"}
#             ]
        
#         # Display chat messages
#         chat_container = st.container()
#         with chat_container:
#             for msg in st.session_state.chat_messages:
#                 if msg["type"] == "user":
#                     st.markdown(f"""
#                     <div class="user-message">
#                         <strong>You:</strong> {msg["message"]}
#                     </div>
#                     """, unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"""
#                     <div class="bot-message">
#                         <strong>Kuber AI:</strong> {msg["message"]}
#                     </div>
#                     """, unsafe_allow_html=True)
        
#         # User input
#         with st.form("chat_form"):
#             user_input = st.text_input("Ask about gold investments...", key="user_input")
#             col_send, col_examples = st.columns([1, 1])
            
#             with col_send:
#                 submitted = st.form_submit_button("Send 🚀", use_container_width=True)
            
#             with col_examples:
#                 if st.form_submit_button("💡 Example Questions", use_container_width=True):
#                     examples = [
#                         "What is digital gold?",
#                         "How safe is gold investment?", 
#                         "What's the minimum investment?",
#                         "Why should I invest in gold now?",
#                         "How do I start investing?"
#                     ]
#                     st.info("Try asking: " + " | ".join(examples))
            
#             if submitted and user_input.strip():
#                 # Add user message
#                 st.session_state.chat_messages.append({"type": "user", "message": user_input})
                
#                 # Process query using API 1 with Gemini 2.0 Flash
#                 with st.spinner("🤖 Kuber AI is thinking with Gemini 2.0 Flash..."):
#                     response = process_gold_query(user_input)
                
#                 # Add bot response with model info
#                 bot_message = response["response"]
#                 if response.get("model_used") == "gemini-2.0-flash":
#                     bot_message += "\n\n*✨ Response generated by Gemini 2.0 Flash*"
                
#                 st.session_state.chat_messages.append({"type": "bot", "message": bot_message})
                
#                 # Rerun to update chat
#                 st.rerun()
    
#     with col2:
#         st.header("🛒 Digital Gold Purchase")
        
#         # Purchase form with enhanced UX
#         with st.form("purchase_form"):
#             st.subheader("Complete Your Profile")
            
#             col_name, col_email = st.columns(2)
#             with col_name:
#                 name = st.text_input("Full Name*", placeholder="Enter your full name")
#             with col_email:
#                 email = st.text_input("Email*", placeholder="name@example.com")
            
#             phone = st.text_input("Phone Number*", placeholder="+91 98765 43210")
            
#             st.subheader("Investment Details")
            
#             investment_type = st.selectbox(
#                 "Investment Type", 
#                 ["By Amount (₹)", "By Weight (grams)"],
#                 help="Choose whether to invest by rupee amount or gold weight"
#             )
            
#             if investment_type == "By Amount (₹)":
#                 investment_value = st.number_input(
#                     "Investment Amount (₹)*", 
#                     min_value=10.0, 
#                     value=100.0, 
#                     step=10.0,
#                     help="Minimum investment is ₹10"
#                 )
#                 gold_weight = investment_value / current_gold_price
                
#                 st.success(f"""
#                 **💎 Purchase Summary:**
                
#                 **Amount:** ₹{investment_value:,.2f}  
#                 **Gold Weight:** {gold_weight:.6f} grams  
#                 **Rate:** ₹{current_gold_price:,.2f} per gram  
#                 **Platform Fee:** ₹0 (Free! 🎉)
#                 """)
#             else:
#                 gold_weight = st.number_input(
#                     "Gold Weight (grams)*", 
#                     min_value=0.001, 
#                     value=0.016, 
#                     step=0.001, 
#                     format="%.6f",
#                     help="Minimum 0.001 grams"
#                 )
#                 investment_value = gold_weight * current_gold_price
                
#                 st.success(f"""
#                 **💎 Purchase Summary:**
                
#                 **Gold Weight:** {gold_weight:.6f} grams  
#                 **Amount:** ₹{investment_value:,.2f}  
#                 **Rate:** ₹{current_gold_price:,.2f} per gram  
#                 **Platform Fee:** ₹0 (Free! 🎉)
#                 """)
            
#             # Terms checkbox
#             terms_accepted = st.checkbox(
#                 "I agree to the terms and conditions for digital gold investment 📜",
#                 help="You must accept terms to proceed"
#             )
            
#             submitted = st.form_submit_button(
#                 "💎 Purchase Digital Gold", 
#                 use_container_width=True,
#                 disabled=not terms_accepted
#             )
            
#             if submitted:
#                 # Validate form
#                 if not all([name, email, phone]):
#                     st.error("Please fill in all required fields! 📝")
#                 elif investment_value < 10:
#                     st.error("Minimum investment amount is ₹10 bestie! 💸")
#                 elif not terms_accepted:
#                     st.error("Please accept terms and conditions! 📜")
#                 else:
#                     # Process purchase using API 2
#                     with st.spinner("🔄 Processing your gold purchase..."):
#                         purchase_data = {
#                             'name': name,
#                             'email': email,
#                             'phone': phone,
#                             'amount': investment_value,
#                             'gold_weight': gold_weight
#                         }
                        
#                         result = process_gold_purchase(purchase_data)
                        
#                         if result['success']:
#                             st.balloons()  # Celebration effect!
                            
#                             st.markdown(f"""
#                             <div class="success-message">
#                                 <h3>{result['success_message']}</h3>
#                                 <p><strong>🆔 Purchase ID:</strong> #{result['purchase_id']}<br>
#                                 <strong>💰 Amount Paid:</strong> ₹{investment_value:,.2f}<br>
#                                 <strong>⚖️ Gold Purchased:</strong> {gold_weight:.6f} grams<br>
#                                 <strong>📅 Date:</strong> {result['purchase_details']['date']}<br>
#                                 <strong>✅ Status:</strong> {result['purchase_details']['status']}</p>
#                                 <p><em>Welcome to the gold investors club! 🏆</em></p>
#                             </div>
#                             """, unsafe_allow_html=True)
                            
#                             # Auto-refresh after success
#                             time.sleep(3)
#                             st.rerun()
#                         else:
#                             st.error(f"❌ {result['error']}")
    
#     # Database section with enhanced analytics
#     st.header("🗄️ Investment Dashboard")
    
#     # Refresh button
#     col_refresh, col_export = st.columns([1, 1])
#     with col_refresh:
#         if st.button("🔄 Refresh Database", use_container_width=True):
#             st.rerun()
    
#     # Display purchases with analytics
#     purchases_df = get_all_purchases()
    
#     if not purchases_df.empty:
#         # Summary metrics
#         col1, col2, col3, col4 = st.columns(4)
        
#         total_purchases = len(purchases_df)
#         total_amount = purchases_df['Amount (₹)'].sum()
#         total_gold = purchases_df['Gold Weight (g)'].sum()
#         avg_investment = purchases_df['Amount (₹)'].mean()
        
#         with col1:
#             st.metric("📊 Total Purchases", total_purchases)
#         with col2:
#             st.metric("💰 Total Investment", f"₹{total_amount:,.2f}")
#         with col3:
#             st.metric("⚖️ Total Gold", f"{total_gold:.4f}g")
#         with col4:
#             st.metric("📈 Avg Investment", f"₹{avg_investment:,.2f}")
        
#         # Purchase table
#         st.subheader("💼 All Transactions")
#         st.dataframe(
#             purchases_df, 
#             use_container_width=True, 
#             hide_index=True,
#             column_config={
#                 "Amount (₹)": st.column_config.NumberColumn(
#                     "Amount (₹)",
#                     format="₹%.2f"
#                 ),
#                 "Gold Weight (g)": st.column_config.NumberColumn(
#                     "Gold Weight (g)",
#                     format="%.6f g"
#                 )
#             }
#         )
        
#     else:
#         st.info("🌟 No purchases yet. Be the first to invest in digital gold!")
    
#     # API Documentation and Chat History
#     tab1, tab2 = st.tabs(["📚 API Documentation", "💬 Chat History"])
    
#     with tab1:
#         st.markdown("""
#         ### 🚀 API Endpoints
        
#         **API 1: AI-Powered Gold Investment Q&A Assistant**
#         - **Function:** `process_gold_query(user_query: str)`  
#         - **AI Model:** Google Gemini 2.0 Flash
#         - **Purpose:** Intelligent responses to gold investment queries
#         - **Features:** Natural language understanding, contextual responses, investment guidance
#         - **Returns:** AI-generated advice with purchase nudges
        
#         **API 2: Enhanced Digital Gold Purchase System**  
#         - **Function:** `process_gold_purchase(user_data: dict)`
#         - **Purpose:** Complete gold purchase workflow with validation
#         - **Features:** Email/phone validation, real-time calculations, database persistence
#         - **Returns:** Purchase confirmation with transaction details
        
#         ### 🗃️ Database Schema
        
#         **Purchases Table:**
#         ```sql
#         CREATE TABLE purchases (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL, 
#             phone TEXT NOT NULL,
#             amount REAL NOT NULL,
#             gold_weight REAL NOT NULL,
#             purchase_date TEXT NOT NULL,
#             status TEXT DEFAULT 'Completed'
#         )
#         ```
        
#         **Chat History Table:**
#         ```sql
#         CREATE TABLE chat_history (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_query TEXT NOT NULL,
#             bot_response TEXT NOT NULL,
#             timestamp TEXT NOT NULL,
#             model_used TEXT DEFAULT 'gemini-2.0-flash'
#         )
#         ```
        
#         ### 🤖 AI Integration
#         - **Model:** Google Gemini 2.0 Flash
#         - **Features:** Advanced natural language understanding
#         - **Personality:** Fun, engaging "bestie" tone
#         - **Specialization:** Gold investment expertise
#         - **Fallback:** Built-in responses when API unavailable
#         """)
    
#     with tab2:
#         st.subheader("💬 Recent Conversations")
#         chat_history = get_chat_history()
        
#         if chat_history:
#             for query, response, timestamp, model in chat_history:
#                 with st.expander(f"🕒 {timestamp} - {model}"):
#                     st.markdown(f"**User:** {query}")
#                     st.markdown(f"**Kuber AI:** {response}")
#         else:
#             st.info("No chat history yet. Start a conversation!")

# if __name__ == "__main__":
#     main()

import streamlit as st
import requests
import json
from datetime import datetime
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Simplify Money - Digital Gold Investment",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FFD700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
        border-left: 4px solid #FFD700;
        background-color: #f9f9f9;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .ai-message {
        background-color: #fff3e0;
        border-left-color: #ff9800;
    }
    .success-message {
        background-color: #e8f5e8;
        border-left-color: #4caf50;
        color: #2e7d32;
    }
    .purchase-card {
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #fff9c4 0%, #fff3e0 100%);
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"  # Change this to your deployed API URL

class DigitalGoldUI:
    def __init__(self):
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        if 'user_id' not in st.session_state:
            st.session_state.user_id = 1001  # Default user ID
        if 'user_name' not in st.session_state:
            st.session_state.user_name = "Friend"
        if 'pending_purchase' not in st.session_state:
            st.session_state.pending_purchase = False

    def call_llm_api(self, query: str) -> dict:
        """Call the LLM interaction API"""
        try:
            payload = {
                "user_id": st.session_state.user_id,
                "query": query,
                "user_name": st.session_state.user_name
            }
            
            response = requests.post(
                f"{API_BASE_URL}/api/v1/llm-interaction",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API Error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Connection failed: {str(e)}"}

    def call_purchase_api(self, amount: float) -> dict:
        """Call the digital gold purchase API"""
        try:
            payload = {
                "user_id": st.session_state.user_id,
                "amount": amount,
                "user_name": st.session_state.user_name
            }
            
            response = requests.post(
                f"{API_BASE_URL}/api/v1/purchase-gold",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Purchase failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Purchase failed: {str(e)}"}

    def get_user_purchases(self) -> dict:
        """Get user's purchase history"""
        try:
            response = requests.get(
                f"{API_BASE_URL}/api/v1/user/{st.session_state.user_id}/purchases"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to fetch purchases: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Failed to fetch purchases: {str(e)}"}
        
def main():
    ui = DigitalGoldUI()
    
    # Header
    st.markdown('<h1 class="main-header">💰 Simplify Money - Digital Gold Investment</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 👤 User Settings")
        st.session_state.user_name = st.text_input("Your Name", value=st.session_state.user_name)
        st.session_state.user_id = st.number_input("User ID", value=st.session_state.user_id, min_value=1)
        
        st.markdown("---")
        st.markdown("## 📊 Quick Stats")
        
        # Get user purchases
        purchases_data = ui.get_user_purchases()
        if "error" not in purchases_data:
            st.metric("Total Purchases", purchases_data.get("total_purchases", 0))
            total_invested = sum([p["amount"] for p in purchases_data.get("purchases", [])])
            st.metric("Total Invested", f"₹{total_invested:.2f}")
        
        if st.button("🔄 Refresh Stats"):
            st.rerun()
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat"):
            st.session_state.conversation_history = []
            st.session_state.pending_purchase = False
            st.rerun()

    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 💬 Chat with AI Assistant")
        
        # Display conversation history
        for msg in st.session_state.conversation_history:
            if msg["type"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
            elif msg["type"] == "ai":
                st.markdown(f'<div class="chat-message ai-message"><strong>AI Assistant:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
            elif msg["type"] == "success":
                st.markdown(f'<div class="chat-message success-message"><strong>✅ Success:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Ask me about digital gold investment...",
                placeholder="e.g., I want to invest in digital gold, What are the benefits of gold investment?, etc.",
                height=100
            )
            col_a, col_b = st.columns([1, 4])
            with col_a:
                submit_chat = st.form_submit_button("💬 Send", use_container_width=True)
        
        # Process chat input
        if submit_chat and user_input.strip():
            # Add user message to history
            st.session_state.conversation_history.append({
                "type": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })
            
            # Show loading
            with st.spinner("🤔 AI is thinking..."):
                # Call LLM API
                response = ui.call_llm_api(user_input)
            
            if "error" in response:
                st.error(f"Error: {response['error']}")
            else:
                # Add AI response to history
                st.session_state.conversation_history.append({
                    "type": "ai",
                    "content": response["ai_response"],
                    "timestamp": datetime.now(),
                    "suggests_purchase": response.get("suggests_purchase", False)
                })
                
                # Set pending purchase flag if AI suggests purchase
                if response.get("suggests_purchase", False):
                    st.session_state.pending_purchase = True
            
            st.rerun()
    
    with col2:
        st.markdown("## 🛒 Purchase Digital Gold")
        
        # Quick purchase section
        with st.container():
            st.markdown('<div class="purchase-card">', unsafe_allow_html=True)
            st.markdown("### 💎 Quick Purchase")
            
            purchase_amount = st.number_input(
                "Amount (₹)", 
                min_value=10.0, 
                max_value=100000.0, 
                value=10.0, 
                step=10.0
            )
            
            # Purchase button with dynamic text
            button_text = "🚀 Buy Now!" if not st.session_state.pending_purchase else "✨ Complete Purchase!"
            button_type = "primary" if st.session_state.pending_purchase else "secondary"
            
            if st.button(button_text, type=button_type, use_container_width=True):
                with st.spinner("💳 Processing purchase..."):
                    purchase_result = ui.call_purchase_api(purchase_amount)
                
                if "error" in purchase_result:
                    st.error(f"Purchase failed: {purchase_result['error']}")
                else:
                    # Add success message to chat
                    st.session_state.conversation_history.append({
                        "type": "success",
                        "content": purchase_result["message"],
                        "timestamp": datetime.now()
                    })
                    
                    # Clear pending purchase
                    st.session_state.pending_purchase = False
                    
                    # Show success
                    st.success("🎉 Purchase Successful!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Investment benefits
        st.markdown("---")
        st.markdown("### 🌟 Why Digital Gold?")
        benefits = [
            "💰 Low entry point (₹10)",
            "🏦 Zero storage hassles",
            "⚡ 24/7 liquidity",
            "📈 Hedge against inflation",
            "🔒 Secure & regulated",
            "📱 Instant trading"
        ]
        
        for benefit in benefits:
            st.markdown(f"• {benefit}")
    
    # Purchase history section
    st.markdown("---")
    st.markdown("## 📈 Your Investment History")
    
    purchases_data = ui.get_user_purchases()
    if "error" not in purchases_data and purchases_data.get("purchases"):
        # Display purchases in a nice format
        for purchase in purchases_data["purchases"]:
            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 2])
            with col_a:
                st.markdown(f"**₹{purchase['amount']}**")
            with col_b:
                st.markdown(f"ID: {purchase['transaction_id']}")
            with col_c:
                st.markdown(f"Status: ✅ {purchase['status']}")
            with col_d:
                st.markdown(f"{purchase['timestamp'][:10]}")
            st.markdown("---")
    else:
        st.info("📝 No purchases yet. Start your gold investment journey today!")
    
    # Example queries
    st.markdown("## 💡 Try These Example Queries")
    examples = [
        "I want to invest in digital gold",
        "What are the benefits of gold investment?",
        "How much should I invest in gold?",
        "Is digital gold safe?",
        "Can I sell my gold anytime?",
        "What's the minimum investment amount?"
    ]
    
    cols = st.columns(3)
    for i, example in enumerate(examples):
        with cols[i % 3]:
            if st.button(example, key=f"example_{i}"):
                # Add example to chat
                st.session_state.conversation_history.append({
                    "type": "user",
                    "content": example,
                    "timestamp": datetime.now()
                })
                
                # Call API
                with st.spinner("🤔 AI is thinking..."):
                    response = ui.call_llm_api(example)
                
                if "error" not in response:
                    st.session_state.conversation_history.append({
                        "type": "ai",
                        "content": response["ai_response"],
                        "timestamp": datetime.now(),
                        "suggests_purchase": response.get("suggests_purchase", False)
                    })
                    
                    if response.get("suggests_purchase", False):
                        st.session_state.pending_purchase = True

                st.rerun()

if __name__ == "__main__":
    main()