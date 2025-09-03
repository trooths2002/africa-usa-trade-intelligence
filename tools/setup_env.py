#!/usr/bin/env python3
"""
Helper script to set up environment variables for deployment
"""
import os
import sys

def setup_env_vars():
    """Guide the user through setting up environment variables"""
    print("🔧 Environment Variable Setup Helper")
    print("=" * 40)
    
    print("\nThis script will help you set up the required environment variables.")
    print("You'll need to set these variables in your hosting platform (Render/Railway).")
    
    # APP_LOGIN_PASSWORD
    print("\n1. APP_LOGIN_PASSWORD")
    print("   This is the password to access your dashboard.")
    print("   Recommendation: Use a strong, unique password.")
    app_password = input("   Enter your desired password (or press Enter for default 'change-me-dev'): ").strip()
    if not app_password:
        app_password = "change-me-dev"
    
    # DATABASE_URL
    print("\n2. DATABASE_URL")
    print("   This is your database connection string.")
    print("   For development: sqlite:///./trade_intelligence.db")
    print("   For production: postgresql://user:password@host:port/database")
    db_url = input("   Enter your database URL (or press Enter for default SQLite): ").strip()
    if not db_url:
        db_url = "sqlite:///./trade_intelligence.db"
    
    # STREAMLIT_API_URL
    print("\n3. STREAMLIT_API_URL")
    print("   This is your deployed dashboard URL.")
    print("   Example: https://your-app.onrender.com")
    api_url = input("   Enter your deployed dashboard URL (or press Enter for default localhost): ").strip()
    if not api_url:
        api_url = "http://localhost:8501"
    
    # DEFAULT_USER_ID
    print("\n4. DEFAULT_USER_ID")
    print("   This is the default user ID for the application.")
    user_id = input("   Enter your default user ID (or press Enter for default 'terrence@freeworldtrade'): ").strip()
    if not user_id:
        user_id = "terrence@freeworldtrade"
    
    # Display summary
    print("\n" + "=" * 40)
    print("✅ Environment Variables Summary:")
    print("=" * 40)
    print(f"APP_LOGIN_PASSWORD: {app_password}")
    print(f"DATABASE_URL: {db_url}")
    print(f"STREAMLIT_API_URL: {api_url}")
    print(f"DEFAULT_USER_ID: {user_id}")
    
    print("\n📋 Next steps:")
    print("1. Set these variables in your hosting platform:")
    print("   - Render: In your service settings under Environment Variables")
    print("   - Railway: In your project variables settings")
    print("2. Set STREAMLIT_API_URL as a GitHub Secret for CI health checks")
    print("3. For PostgreSQL, ensure your database service is configured and accessible")
    
    # Offer to create a .env file for local development
    print("\n📝 Would you like to create a .env file for local development?")
    create_env = input("   Create .env file? (y/N): ").strip().lower()
    
    if create_env == 'y':
        env_content = f"""# Environment variables for local development
APP_LOGIN_PASSWORD={app_password}
DATABASE_URL={db_url}
STREAMLIT_API_URL={api_url}
DEFAULT_USER_ID={user_id}
"""
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ .env file created successfully!")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
    
    print("\n🚀 You're ready to deploy!")
    print("Check DEPLOYMENT_GUIDE.md for detailed deployment instructions.")

if __name__ == "__main__":
    setup_env_vars()