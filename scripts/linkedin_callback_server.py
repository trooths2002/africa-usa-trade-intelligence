#!/usr/bin/env python3
"""
Simple HTTP server to capture LinkedIn OAuth callback
This server will receive the authorization code from LinkedIn
"""

import http.server
import socketserver
import urllib.parse
from http import HTTPStatus
import threading
import webbrowser
import time

class LinkedInCallbackHandler(http.server.SimpleHTTPRequestHandler):
    """Handler for LinkedIn OAuth callback"""
    
    def do_GET(self):
        """Handle GET requests"""
        # Parse the URL to extract query parameters
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # Check if this is the OAuth callback
        if parsed_url.path == '/':
            # Extract the authorization code
            auth_code = query_params.get('code', [None])[0]
            state = query_params.get('state', [None])[0]
            
            if auth_code:
                print("\n" + "="*60)
                print("✅ AUTHORIZATION CODE RECEIVED!")
                print("="*60)
                print(f"Authorization Code: {auth_code}")
                print(f"State: {state}")
                print("="*60)
                print("You can now use this code to get your access token.")
                print("Copy this code and use it in the LinkedIn OAuth script.")
                print("="*60)
                
                # Send a response to the browser
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                response_html = """
                <html>
                <head><title>LinkedIn OAuth Success</title></head>
                <body>
                    <h1 style="color: green;">✅ Authorization Successful!</h1>
                    <p>Your authorization code has been captured.</p>
                    <p>Please copy this code and use it in the LinkedIn OAuth script:</p>
                    <textarea rows="5" cols="80" onclick="this.select()">{}</textarea>
                    <p>You can now close this window and return to the terminal.</p>
                </body>
                </html>
                """.format(auth_code)
                
                self.wfile.write(response_html.encode())
                
                # Signal that we've received the code
                self.server.auth_code_received = auth_code
            else:
                # Show the authorization form
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                response_html = """
                <html>
                <head><title>LinkedIn OAuth Callback</title></head>
                <body>
                    <h1>LinkedIn OAuth Callback Server</h1>
                    <p>Waiting for authorization code...</p>
                    <p>Please complete the LinkedIn authorization process.</p>
                </body>
                </html>
                """
                
                self.wfile.write(response_html.encode())

def start_callback_server(port=8501):
    """Start the callback server"""
    try:
        with socketserver.TCPServer(("", port), LinkedInCallbackHandler) as httpd:
            print(f"🚀 Starting LinkedIn OAuth callback server on port {port}")
            print(f"📝 Make sure your LinkedIn app redirect URI is set to: http://localhost:{port}")
            
            # Add a flag to track when we receive the auth code
            httpd.auth_code_received = None
            
            # Start the server in a separate thread
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            print("✅ Callback server is running!")
            print("🔄 Please proceed with LinkedIn authorization in your browser")
            print("💡 This server will automatically capture the authorization code")
            
            # Wait for the authorization code
            while httpd.auth_code_received is None:
                time.sleep(1)
            
            # Return the authorization code
            return httpd.auth_code_received
            
    except Exception as e:
        print(f"❌ Error starting callback server: {str(e)}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("🔐 LINKEDIN OAUTH CALLBACK SERVER")
    print("=" * 60)
    print("This server will capture the LinkedIn OAuth authorization code")
    print("=" * 60)
    
    auth_code = start_callback_server()
    if auth_code:
        print(f"\n✅ Authorization code captured: {auth_code}")
        print("You can now use this code to get your access token")
    else:
        print("\n❌ Failed to capture authorization code")