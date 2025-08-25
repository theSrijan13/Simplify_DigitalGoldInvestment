
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
