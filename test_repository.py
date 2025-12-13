"""
Test script to verify Repository pattern is working correctly
Run this to make sure database connections work
"""

import sys
from datetime import datetime
from backend.models.repositories import UserRepository, AnalysisRepository
from backend.models.db_models import UserDB, UserAnalysisDB
from backend.services.auth_service import AuthService
from backend.config.database import DatabaseConnection

def test_database_connection():
    """Test 1: Verify database connection"""
    print("\n" + "="*60)
    print("TEST 1: Database Connection")
    print("="*60)
    
    try:
        db = DatabaseConnection.get_database()
        is_healthy = DatabaseConnection.health_check()
        
        if is_healthy:
            print("✅ Database connection: HEALTHY")
            return True
        else:
            print("❌ Database connection: UNHEALTHY")
            return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_user_repository():
    """Test 2: User Repository operations"""
    print("\n" + "="*60)
    print("TEST 2: User Repository")
    print("="*60)
    
    try:
        # Create test user
        test_email = "test_repo@example.com"
        test_user_id = "test-repo-123"
        
        # Hash password
        password_hash = AuthService.hash_password("TestPassword123")
        
        # Create user object
        user = UserDB(
            user_id=test_user_id,
            email=test_email,
            password_hash=password_hash,
            company_name="Test Company",
            subscription_tier="free",
            is_active=True,
            created=datetime.utcnow(),
            updated=datetime.utcnow()
        )
        
        print(f"📝 Creating user: {test_email}")
        
        # Check if user already exists
        existing_user = UserRepository.find_by_email(test_email)
        if existing_user:
            print(f"⚠️  User already exists, skipping creation")
        else:
            # Create user
            success = UserRepository.create(user)
            if success:
                print("✅ User created successfully")
            else:
                print("❌ User creation failed")
                return False
        
        # Find by email
        print(f"\n🔍 Finding user by email: {test_email}")
        found_user = UserRepository.find_by_email(test_email)
        if found_user:
            print(f"✅ Found user: {found_user.user_id}")
            print(f"   Email: {found_user.email}")
            print(f"   Company: {found_user.company_name}")
        else:
            print("❌ User not found by email")
            return False
        
        # Find by ID
        print(f"\n🔍 Finding user by ID: {test_user_id}")
        found_user = UserRepository.find_by_id(test_user_id)
        if found_user:
            print(f"✅ Found user: {found_user.email}")
        else:
            print("❌ User not found by ID")
            return False
        
        # Update last login
        print(f"\n🔄 Updating last login")
        updated = UserRepository.update_last_login(test_user_id)
        if updated:
            print("✅ Last login updated")
        else:
            print("❌ Last login update failed")
        
        # Verify password
        print(f"\n🔐 Testing password verification")
        is_valid = AuthService.verify_password("TestPassword123", password_hash)
        if is_valid:
            print("✅ Password verification: SUCCESS")
        else:
            print("❌ Password verification: FAILED")
            return False
        
        is_invalid = AuthService.verify_password("WrongPassword", password_hash)
        if not is_invalid:
            print("✅ Wrong password correctly rejected")
        else:
            print("❌ Wrong password incorrectly accepted")
            return False
        
        print("\n✅ All User Repository tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ User Repository test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_analysis_repository():
    """Test 3: Analysis Repository operations"""
    print("\n" + "="*60)
    print("TEST 3: Analysis Repository")
    print("="*60)
    
    try:
        test_user_id = "test-repo-123"
        test_analysis_id = "test-analysis-456"
        
        # Create test analysis
        analysis = UserAnalysisDB(
            analysis_id=test_analysis_id,
            user_id=test_user_id,
            project_id="test-project",
            query="Test query: analyze my infrastructure",
            result={
                "status": "success",
                "analysis": "Test analysis result",
                "recommendations": []
            },
            cost_savings=1000.0,
            execution_time=5.2,
            status="completed",
            created=datetime.utcnow(),
            updated=datetime.utcnow()
        )
        
        print(f"📝 Creating analysis: {test_analysis_id}")
        
        # Check if analysis already exists
        existing_analysis = AnalysisRepository.find_by_id(test_analysis_id)
        if existing_analysis:
            print("⚠️  Analysis already exists, skipping creation")
        else:
            # Create analysis
            success = AnalysisRepository.create(analysis)
            if success:
                print("✅ Analysis created successfully")
            else:
                print("❌ Analysis creation failed")
                return False
        
        # Find by user ID
        print(f"\n🔍 Finding analyses for user: {test_user_id}")
        user_analyses = AnalysisRepository.find_by_user_id(test_user_id, limit=5)
        print(f"✅ Found {len(user_analyses)} analyses")
        
        for a in user_analyses:
            print(f"   - {a.analysis_id}: {a.query[:50]}...")
        
        # Find by analysis ID
        print(f"\n🔍 Finding analysis by ID: {test_analysis_id}")
        found_analysis = AnalysisRepository.find_by_id(test_analysis_id)
        if found_analysis:
            print(f"✅ Found analysis: {found_analysis.query}")
            print(f"   Status: {found_analysis.status}")
            print(f"   Cost savings: ${found_analysis.cost_savings}")
        else:
            print("❌ Analysis not found")
            return False
        
        # Count analyses
        print(f"\n📊 Counting analyses for user")
        count = AnalysisRepository.count_by_user(test_user_id)
        print(f"✅ Total analyses: {count}")
        
        print("\n✅ All Analysis Repository tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Analysis Repository test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_jwt_tokens():
    """Test 4: JWT token operations"""
    print("\n" + "="*60)
    print("TEST 4: JWT Token Operations")
    print("="*60)
    
    try:
        test_user_id = "test-repo-123"
        test_email = "test_repo@example.com"
        
        # Create token
        print(f"🔑 Creating JWT token for {test_email}")
        token = AuthService.create_access_token(
            user_id=test_user_id,
            email=test_email
        )
        print(f"✅ Token created: {token[:50]}...")
        
        # Verify token
        print(f"\n🔍 Verifying JWT token")
        payload = AuthService.verify_token(token)
        
        if payload.get("user_id") == test_user_id:
            print(f"✅ Token verified successfully")
            print(f"   User ID: {payload['user_id']}")
            print(f"   Email: {payload['sub']}")
        else:
            print("❌ Token verification failed")
            return False
        
        print("\n✅ All JWT token tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ JWT token test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_test_data():
    """Optional: Clean up test data"""
    print("\n" + "="*60)
    print("CLEANUP: Removing test data")
    print("="*60)
    
    try:
        test_user_id = "test-repo-123"
        test_analysis_id = "test-analysis-456"
        
        # Delete test analysis
        print(f"🗑️  Deleting test analysis: {test_analysis_id}")
        deleted = AnalysisRepository.delete_by_id(test_analysis_id)
        if deleted:
            print("✅ Analysis deleted")
        else:
            print("⚠️  Analysis not found or already deleted")
        
        # Delete test user
        print(f"🗑️  Deleting test user: {test_user_id}")
        deleted = UserRepository.delete_user(test_user_id)
        if deleted:
            print("✅ User deleted")
        else:
            print("⚠️  User not found or already deleted")
        
        print("\n✅ Cleanup completed!")
        
    except Exception as e:
        print(f"\n⚠️  Cleanup warning: {e}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 REPOSITORY PATTERN TEST SUITE")
    print("="*60)
    print("This will verify that the Repository pattern is working correctly")
    print("and that database connections are functional.")
    
    results = {
        "Database Connection": test_database_connection(),
        "User Repository": test_user_repository(),
        "Analysis Repository": test_analysis_repository(),
        "JWT Tokens": test_jwt_tokens()
    }
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ Your Repository pattern is working correctly!")
        print("✅ Database connections are functional!")
        print("✅ No more db.User issues!")
        
        # Ask about cleanup
        response = input("\n🗑️  Do you want to clean up test data? (y/n): ")
        if response.lower() == 'y':
            cleanup_test_data()
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Please check the error messages above.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())