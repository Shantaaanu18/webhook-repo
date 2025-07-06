#!/usr/bin/env python3
"""
Test script for GitHub Webhook Handler
Sends test webhook events to verify functionality
"""

import requests
import json
import time

# Test webhook URL (update this to match your setup)
WEBHOOK_URL = "http://localhost:5000/webhook"

def test_push_event():
    """Test a push event webhook"""
    print("Testing push event...")
    
    payload = {
        "ref": "refs/heads/main",
        "pusher": {
            "name": "testuser"
        },
        "repository": {
            "name": "test-repo"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "push"
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_pull_request_event():
    """Test a pull request event webhook"""
    print("\nTesting pull request event...")
    
    payload = {
        "action": "opened",
        "pull_request": {
            "user": {
                "login": "testuser"
            },
            "head": {
                "ref": "feature-branch"
            },
            "base": {
                "ref": "main"
            }
        },
        "repository": {
            "name": "test-repo"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request"
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_merge_event():
    """Test a merge event webhook"""
    print("\nTesting merge event...")
    
    payload = {
        "action": "closed",
        "pull_request": {
            "user": {
                "login": "testuser"
            },
            "head": {
                "ref": "feature-branch"
            },
            "base": {
                "ref": "main"
            },
            "merged": True
        },
        "repository": {
            "name": "test-repo"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request"
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_events_api():
    """Test the events API endpoint"""
    print("\nTesting events API...")
    
    try:
        response = requests.get("http://localhost:5000/events")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            events = response.json()
            print(f"Found {len(events)} events")
            for event in events[:3]:  # Show first 3 events
                print(f"  - {event.get('type', 'unknown')} by {event.get('author', 'unknown')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("🧪 GitHub Webhook Handler - Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server is not running. Please start the application first:")
        print("   python run.py")
        return
    
    # Run tests
    tests = [
        test_push_event,
        test_pull_request_event,
        test_merge_event,
        test_events_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your webhook handler is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main() 