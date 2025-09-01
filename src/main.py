"""
Main entry point for the Africa-USA Trade Intelligence Platform
"""
import uvicorn
import subprocess
import sys
import time
import signal
import os
from typing import List

class PlatformLauncher:
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
    
    def start_api_server(self):
        """Start the FastAPI server"""
        print("Starting API server...")
        # Change to src directory and run uvicorn with correct module path
        api_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], cwd=os.path.join(os.getcwd(), "src"))
        self.processes.append(api_process)
        print("API server started on http://localhost:8000")
    
    def start_dashboard(self):
        """Start the Streamlit dashboard"""
        print("Starting Streamlit dashboard...")
        dashboard_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", 
            "run", "dashboard/app.py",
            "--server.port", "8501"
        ], cwd=os.path.join(os.getcwd(), "src"))
        self.processes.append(dashboard_process)
        print("Dashboard started on http://localhost:8501")
    
    def start_intelligence_server(self):
        """Start the MCP intelligence server"""
        print("Starting MCP intelligence server...")
        intelligence_process = subprocess.Popen([
            sys.executable, "intelligence/server.py"
        ], cwd=os.path.join(os.getcwd(), "src"))
        self.processes.append(intelligence_process)
        print("MCP intelligence server started")
    
    def start_all_services(self):
        """Start all platform services"""
        print("Starting Africa-USA Trade Intelligence Platform...")
        
        # Start services
        self.start_api_server()
        time.sleep(2)  # Give API server time to start
        
        self.start_intelligence_server()
        time.sleep(2)  # Give intelligence server time to start
        
        self.start_dashboard()
        
        print("\nAll services started successfully!")
        print("Access the dashboard at: http://localhost:8501")
        print("API documentation at: http://localhost:8000/docs")
        
        # Keep the main process alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down services...")
            self.shutdown()
    
    def shutdown(self):
        """Shutdown all services"""
        print("Stopping all services...")
        for process in self.processes:
            if process.poll() is None:  # Process is still running
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        print("All services stopped.")

def signal_handler(sig, frame):
    print('\nReceived interrupt signal. Shutting down...')
    launcher.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    launcher = PlatformLauncher()
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start all services
    launcher.start_all_services()