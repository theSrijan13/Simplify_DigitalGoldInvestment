#!/usr/bin/env python3
"""
Digital Gold Investment API - Test Script
Run this after starting the FastAPI backend to test all endpoints
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_header(title: str):
    print(f"\n{'='*50}")
    print(f"🧪 {title}")
    print(f"{'='*50}")

def print_response(response: requests.Response, endpoint_name: str):
    print(f"\n📡 {endpoint_name}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Success!")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except:
            print(f"Response: {response.text}")
    else:
        print("❌ Failed!")
        print(f"Error: {response.text}")

def test_health_check():
    """Test basic health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print_response(response, "Health Check")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_llm_interaction():
    """Test LLM interaction endpoint with various queries"""
    test_queries = [
        {
            "user_id": 1001,
            "query": "I want to invest in digital gold",
            "user_name": "TestUser1"
        },
        {
            "user_id": 1002,
            "query": "What are the benefits of gold investment?",
            "user_name": "TestUser2"
        },
        {
            "user_id": 1003,
            "query": "How is the weather today?",  # Non-gold related query
            "user_name": "TestUser3"
        },
        {
            "user_id": 1004,
            "query": "Should I buy gold right now?",
            "user_name": "TestUser4"
        }
    ]
    
    print_header("Testing LLM Interaction API")
    
    for i, query_data in enumerate(test_queries, 1):
        print(f"\n🔍 Test Case {i}: '{query_data['query']}'")
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/llm-interaction",
                json=query_data,
                headers={"Content-Type": "application/json"},
                timeout=30  # LLM calls can take longer
            )
            print_response(response, f"LLM Interaction Test {i}")
            
            # Brief pause between requests
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ LLM Test {i} failed: {e}")

def test_purchase_api():
    """Test digital gold purchase endpoint"""
    test_purchases = [
        {
            "user_id": 1001,
            "amount": 10.0,
            "user_name": "Buyer1"
        },
        {
            "user_id": 1002,
            "amount": 100.0,
            "user_name": "Buyer2"
        },
        {
            "user_id": 1003,
            "amount": 500.0,
            "user_name": "Buyer3"
        },
        {
            "user_id": 1004,
            "amount": 5.0,  # Should fail - below minimum
            "user_name": "Buyer4"
        }
    ]
    
    print_header("Testing Purchase API")
    
    transaction_ids = []
    
    for i, purchase_data in enumerate(test_purchases, 1):
        print(f"\n💳 Purchase Test {i}: ₹{purchase_data['amount']}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/purchase-gold",
                json=purchase_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            print_response(response, f"Purchase Test {i}")
            
            # Store successful transaction IDs
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    transaction_ids.append(data.get("transaction_id"))
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Purchase Test {i} failed: {e}")
    
    return transaction_ids

def test_user_purchases():
    """Test fetching user purchase history"""
    print_header("Testing User Purchase History")
    
    test_user_ids = [1001, 1002, 1003, 9999]  # 9999 should have no purchases
    
    for user_id in test_user_ids:
        print(f"\n👤 Fetching purchases for User {user_id}")
        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/user/{user_id}/purchases",
                timeout=10
            )
            print_response(response, f"User {user_id} Purchases")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch purchases for user {user_id}: {e}")

def test_admin_stats():
    """Test admin statistics endpoint"""
    print_header("Testing Admin Statistics")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/admin/stats", timeout=10)
        print_response(response, "Admin Statistics")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Admin stats test failed: {e}")

def test_error_scenarios():
    """Test various error scenarios"""
    print_header("Testing Error Scenarios")
    
    error_tests = [
        {
            "name": "Invalid JSON in LLM API",
            "method": "POST",
            "url": f"{BASE_URL}/api/v1/llm-interaction",
            "data": "invalid json",
            "headers": {"Content-Type": "application/json"}
        },
        {
            "name": "Missing fields in Purchase API",
            "method": "POST",
            "url": f"{BASE_URL}/api/v1/purchase-gold",
            "data": json.dumps({"amount": 100}),  # Missing user_id
            "headers": {"Content-Type": "application/json"}
        },
        {
            "name": "Non-existent endpoint",
            "method": "GET",
            "url": f"{BASE_URL}/api/v1/non-existent",
            "data": None,
            "headers": {}
        }
    ]
    
    for test in error_tests:
        print(f"\n🚫 {test['name']}")
        try:
            if test["method"] == "POST":
                response = requests.post(
                    test["url"],
                    data=test["data"],
                    headers=test["headers"],
                    timeout=10
                )
            else:
                response = requests.get(test["url"], timeout=10)
            
            print(f"Status Code: {response.status_code}")
            if response.status_code >= 400:
                print("✅ Error handled correctly!")
            else:
                print("⚠️  Expected error but got success")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")

def run_complete_workflow_test():
    """Run a complete end-to-end workflow test"""
    print_header("Complete Workflow Test")
    
    workflow_user = {
        "user_id": 2001,
        "user_name": "WorkflowTester"
    }
    
    print("🔄 Step 1: User asks about gold investment")
    llm_response = requests.post(
        f"{BASE_URL}/api/v1/llm-interaction",
        json={
            **workflow_user,
            "query": "I'm interested in digital gold investment"
        },
        timeout=30
    )
    
    if llm_response.status_code == 200:
        llm_data = llm_response.json()
        print("✅ LLM responded successfully")
        print(f"AI Response: {llm_data.get('ai_response', '')[:100]}...")
        
        if llm_data.get("suggests_purchase"):
            print("🔄 Step 2: AI suggests purchase, making purchase...")
            
            purchase_response = requests.post(
                f"{BASE_URL}/api/v1/purchase-gold",
                json={
                    **workflow_user,
                    "amount": 50.0
                },
                timeout=10
            )
            
            if purchase_response.status_code == 200:
                purchase_data = purchase_response.json()
                print("✅ Purchase successful!")
                print(f"Transaction ID: {purchase_data.get('transaction_id')}")
                
                print("🔄 Step 3: Fetching purchase history...")
                history_response = requests.get(
                    f"{BASE_URL}/api/v1/user/{workflow_user['user_id']}/purchases"
                )
                
                if history_response.status_code == 200:
                    history_data = history_response.json()
                    print("✅ Purchase history retrieved!")
                    print(f"Total purchases: {history_data.get('total_purchases', 0)}")
                    print("🎉 Complete workflow test PASSED!")
                else:
                    print("❌ Failed to fetch purchase history")
            else:
                print("❌ Purchase failed")
        else:
            print("ℹ️  AI didn't suggest purchase for this query")
    else:
        print("❌ LLM interaction failed")

def main():
    """Main test runner"""
    print("🚀 Digital Gold Investment API - Comprehensive Test Suite")
    print(f"Testing API at: {BASE_URL}")
    
    # Start with health check
    if not test_health_check():
        print("\n❌ API is not running! Please start the FastAPI backend first:")
        print("   uvicorn main:app --reload --port 8000")
        return
    
    print("\n🎯 Running all tests...")
    
    # Run all test suites
    test_llm_interaction()
    test_purchase_api()
    test_user_purchases()
    test_admin_stats()
    test_error_scenarios()
    run_complete_workflow_test()
    
    print("\n" + "="*50)
    print("🏁 Test Suite Complete!")
    print("="*50)
    print("\n💡 Next steps:")
    print("1. Check FastAPI docs: http://localhost:8000/docs")
    print("2. Start Streamlit UI: streamlit run streamlit_app.py")
    print("3. Test the complete user experience!")

if __name__ == "__main__":
    main()