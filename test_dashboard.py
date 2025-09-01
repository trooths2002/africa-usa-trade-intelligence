import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import dashboard.app
    print("Dashboard app imported successfully!")
except Exception as e:
    print(f"Error importing dashboard app: {e}")
    import traceback
    traceback.print_exc()