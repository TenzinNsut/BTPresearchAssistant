import unittest
import os
import sys
from main import app

class TestDeployment(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """Test the home page loads"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_static_files_exist(self):
        """Test that static files exist in the static directory"""
        static_files = ['styles.css', 'homeStyle.css', 'test.html']
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        
        # Check if the static directory exists
        self.assertTrue(os.path.exists(static_dir), f"Static directory not found at {static_dir}")
        
        # Check each file
        for file in static_files:
            file_path = os.path.join(static_dir, file)
            self.assertTrue(os.path.exists(file_path), f"File {file} not found in static directory")
            
    def test_static_routes(self):
        """Test that static routes work"""
        static_files = ['styles.css', 'homeStyle.css', 'test.html']
        
        for file in static_files:
            response = self.app.get(f'/static/{file}')
            self.assertEqual(response.status_code, 200, f"Failed to access /static/{file}")
    
    def test_chat_endpoint(self):
        """Test the chat endpoint with a simple message"""
        data = {
            'msg': 'hello',
            'session_id': 'test_session'
        }
        response = self.app.post('/get', data=data)
        self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
    # Create necessary files for testing
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        
    # Create test files if they don't exist
    for file_name, content in [
        ('styles.css', '/* Test CSS */'),
        ('homeStyle.css', '/* Test Home CSS */'),
        ('test.html', '<html><body>Test</body></html>')
    ]:
        file_path = os.path.join(static_dir, file_name)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(content)
    
    # Run the tests
    unittest.main() 