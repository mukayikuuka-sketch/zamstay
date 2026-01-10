def demo_dashboard(request):
    """Demo dashboard showing all user roles - for presentations"""
    return render(request, 'owner-dashboard.html')
