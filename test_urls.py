from django.test import TestCase, Client
from django.urls import reverse

class URLTests(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_home_url(self):
        """Test that home URL exists"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        print("✅ Home URL works")
    
    def test_demo_url(self):
        """Test that demo URL exists"""
        response = self.client.get('/demo/')
        self.assertEqual(response.status_code, 200)
        print("✅ Demo URL works")
    
    def test_owner_dashboard_url(self):
        """Test that owner dashboard URL exists"""
        response = self.client.get('/owner/dashboard/')
        self.assertEqual(response.status_code, 200)
        print("✅ Owner Dashboard URL works")
    
    def test_admin_dashboard_url(self):
        """Test that admin dashboard URL exists"""
        response = self.client.get('/admin/dashboard/')
        self.assertEqual(response.status_code, 200)
        print("✅ Admin Dashboard URL works")
    
    def test_customer_dashboard_url(self):
        """Test that customer dashboard URL exists"""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirects to login
        print("✅ Customer Dashboard URL exists (requires login)")
    
    def test_signup_url(self):
        """Test that signup URL exists"""
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        print("✅ Signup URL works")
    
    def test_login_url(self):
        """Test that login URL exists"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        print("✅ Login URL works")
    
    def test_all_urls_different(self):
        """Test that different URLs return different content"""
        urls = ['/', '/demo/', '/owner/dashboard/', '/admin/dashboard/']
        responses = []
        
        for url in urls:
            response = self.client.get(url)
            responses.append(response.content)
        
        # Check that all responses are different
        unique_responses = set(responses)
        self.assertEqual(len(unique_responses), len(urls))
        print(f"✅ All {len(urls)} URLs show DIFFERENT content!")

if __name__ == '__main__':
    import django
    django.setup()
    
    test = URLTests()
    test.setUp()
    
    print("🧪 Running URL tests...")
    print("="*50)
    
    try:
        test.test_home_url()
        test.test_demo_url()
        test.test_owner_dashboard_url()
        test.test_admin_dashboard_url()
        test.test_customer_dashboard_url()
        test.test_signup_url()
        test.test_login_url()
        test.test_all_urls_different()
        
        print("="*50)
        print("🎉 ALL TESTS PASSED! Your dashboard issue is FIXED!")
        print("Each URL now shows its own unique content.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
