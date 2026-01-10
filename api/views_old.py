from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.cache import cache
from .models import Business, Customer, Promotion, MapView, Analytics
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    BusinessSerializer, CustomerSerializer, PromotionSerializer,
    AnalyticsSerializer
)
import logging

logger = logging.getLogger(__name__)

# Test endpoint
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def test_api(request):
    """Simple health check endpoint"""
    return Response({
        'message': 'API is working!',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0'
    })

# Register API
class RegisterAPI(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'], url_path='register')
    def register_user(self, request):
        """Register a new user"""
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                
                # Create auth token
                token, created = Token.objects.get_or_create(user=user)
                
                # Log registration
                logger.info(f"New user registered: {user.username}")
                
                return Response({
                    'user': UserSerializer(user, context=self.get_serializer_context()).data,
                    'token': token.key,
                    'message': 'User created successfully'
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response({
                'error': 'Registration failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# Login API
class LoginAPI(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        """Authenticate user and return token"""
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Invalid credentials',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = serializer.validated_data
            
            # Create or get token
            token, created = Token.objects.get_or_create(user=user)
            
            # Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            # Log successful login
            logger.info(f"User logged in: {user.username}")
            
            return Response({
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'token': token.key,
                'message': 'Login successful'
            })
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response({
                'error': 'Authentication failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# Logout API
class LogoutAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Logout user and delete token"""
        try:
            # Delete the token
            Token.objects.filter(user=request.user).delete()
            
            # Logout from session
            logout(request)
            
            logger.info(f"User logged out: {request.user.username}")
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return Response({
                'error': 'Logout failed'
            }, status=status.HTTP_400_BAD_REQUEST)

# User API
class UserAPI(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'], url_path='me')
    def get_current_user(self, request):
        """Get current authenticated user"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'], url_path='update-profile')
    def update_profile(self, request):
        """Update user profile"""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Business ViewSet
class BusinessViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category', 'address', 'description']
    ordering_fields = ['created_at', 'name', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return businesses based on user permissions"""
        queryset = Business.objects.all().select_related('owner')
        
        # Filter by owner for non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(Q(owner=self.request.user) | Q(is_public=True))
        
        return queryset
    
    def perform_create(self, serializer):
        """Set owner when creating business"""
        serializer.save(owner=self.request.user)
        logger.info(f"Business created by {self.request.user.username}: {serializer.data['name']}")
    
    @action(detail=False, methods=['get'], url_path='nearby')
    def nearby_businesses(self, request):
        """Get businesses near coordinates (simplified)"""
        try:
            lat = float(request.query_params.get('lat', 0))
            lng = float(request.query_params.get('lng', 0))
            radius = float(request.query_params.get('radius', 10))  # Default 10km
            
            # Simple filtering (in production use GeoDjango)
            businesses = Business.objects.all()
            
            # Add pagination
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', 20)
            
            paginator = Paginator(businesses, page_size)
            page_obj = paginator.get_page(page)
            
            serializer = self.get_serializer(page_obj, many=True)
            
            return Response({
                'results': serializer.data,
                'count': paginator.count,
                'next': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages
            })
            
        except ValueError as e:
            return Response({
                'error': 'Invalid coordinates',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='promotions')
    def business_promotions(self, request, pk=None):
        """Get all promotions for a specific business"""
        business = self.get_object()
        promotions = Promotion.objects.filter(
            business=business,
            is_active=True,
            end_date__gte=timezone.now()
        )
        
        serializer = PromotionSerializer(promotions, many=True)
        return Response(serializer.data)

# Promotion ViewSet
class PromotionViewSet(viewsets.ModelViewSet):
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'business__name', 'business__category']
    ordering_fields = ['created_at', 'start_date', 'end_date', 'discount_value']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return promotions based on visibility"""
        queryset = Promotion.objects.filter(
            is_active=True,
            end_date__gte=timezone.now()
        ).select_related('business', 'business__owner')
        
        # Filter by business owner for non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(business__owner=self.request.user) | Q(is_public=True)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        """Set creator and validate business ownership"""
        business = serializer.validated_data.get('business')
        
        # Check if user owns the business or is admin
        if business.owner != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't own this business")
        
        serializer.save(created_by=self.request.user)
        logger.info(f"Promotion created by {self.request.user.username}: {serializer.data['title']}")
    
    @action(detail=False, methods=['get'], url_path='active')
    def active_promotions(self, request):
        """Get all active promotions with pagination"""
        promotions = self.get_queryset()
        
        # Apply additional filters
        category = request.query_params.get('category')
        if category:
            promotions = promotions.filter(business__category=category)
        
        # Pagination
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        
        paginator = Paginator(promotions, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = self.get_serializer(page_obj, many=True)
        
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number
        })
    
    @action(detail=True, methods=['post'], url_path='redeem')
    @permission_classes([permissions.IsAuthenticated])
    def redeem_promotion(self, request, pk=None):
        """Redeem a promotion (simplified)"""
        promotion = self.get_object()
        
        # Check if promotion is still valid
        if not promotion.is_active or promotion.end_date < timezone.now():
            return Response({
                'error': 'Promotion is no longer valid'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Log redemption
        logger.info(f"Promotion redeemed: {promotion.title} by {request.user.username}")
        
        return Response({
            'message': 'Promotion redeemed successfully',
            'promotion': self.get_serializer(promotion).data,
            'redemption_code': f"REDEEM-{promotion.id}-{request.user.id}-{datetime.now().timestamp()}"
        })

# Analytics ViewSet
class AnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnalyticsSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        """Return analytics with optional date filtering"""
        queryset = Analytics.objects.all().order_by('-date')
        
        # Date filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard_stats(self, request):
        """Get comprehensive dashboard statistics"""
        cache_key = 'dashboard_stats'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Calculate statistics
        stats = {
            'users': {
                'total': User.objects.count(),
                'active_today': User.objects.filter(last_login__date=today).count(),
                'active_this_week': User.objects.filter(last_login__gte=week_ago).count(),
                'new_today': User.objects.filter(date_joined__date=today).count(),
                'new_this_week': User.objects.filter(date_joined__gte=week_ago).count(),
            },
            'businesses': {
                'total': Business.objects.count(),
                'active_today': Business.objects.filter(
                    updated_at__date=today
                ).count(),
                'new_this_week': Business.objects.filter(
                    created_at__gte=week_ago
                ).count(),
                'by_category': Business.objects.values('category').annotate(
                    count=Count('id')
                ).order_by('-count')[:10],
            },
            'promotions': {
                'total_active': Promotion.objects.filter(
                    is_active=True,
                    end_date__gte=timezone.now()
                ).count(),
                'ending_soon': Promotion.objects.filter(
                    is_active=True,
                    end_date__range=[today, today + timedelta(days=3)]
                ).count(),
                'new_this_week': Promotion.objects.filter(
                    created_at__gte=week_ago
                ).count(),
            },
            'revenue': {
                'today': Analytics.objects.filter(date=today).aggregate(
                    total=Sum('revenue')
                )['total'] or 0,
                'this_week': Analytics.objects.filter(
                    date__gte=week_ago
                ).aggregate(total=Sum('revenue'))['total'] or 0,
                'this_month': Analytics.objects.filter(
                    date__gte=month_ago
                ).aggregate(total=Sum('revenue'))['total'] or 0,
                'average_daily': Analytics.objects.filter(
                    date__gte=month_ago
                ).aggregate(avg=Avg('revenue'))['avg'] or 0,
            },
            'engagement': {
                'map_views_today': MapView.objects.filter(
                    viewed_at__date=today
                ).count(),
                'map_views_this_week': MapView.objects.filter(
                    viewed_at__gte=week_ago
                ).count(),
                'promotion_views_today': 0,  # Add your model for this
                'promotion_redemptions_today': 0,  # Add your model for this
            },
            'timestamps': {
                'generated_at': timezone.now().isoformat(),
                'date_range': {
                    'today': today.isoformat(),
                    'week_ago': week_ago.isoformat(),
                    'month_ago': month_ago.isoformat()
                }
            }
        }
        
        # Cache for 5 minutes
        cache.set(cache_key, stats, 300)
        
        return Response(stats)

# Admin User Management
class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all().order_by('-date_joined')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login', 'username']
    
    @action(detail=False, methods=['get'], url_path='stats')
    def user_statistics(self, request):
        """Get user statistics for admin dashboard"""
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        staff_users = User.objects.filter(is_staff=True).count()
        superusers = User.objects.filter(is_superuser=True).count()
        
        # Get registration trends
        today = timezone.now().date()
        registrations_today = User.objects.filter(date_joined__date=today).count()
        registrations_week = User.objects.filter(
            date_joined__gte=today - timedelta(days=7)
        ).count()
        
        return Response({
            'totals': {
                'all_users': total_users,
                'active_users': active_users,
                'staff_users': staff_users,
                'superusers': superusers,
            },
            'recent_activity': {
                'registered_today': registrations_today,
                'registered_this_week': registrations_week,
                'logged_in_today': User.objects.filter(last_login__date=today).count(),
                'logged_in_this_week': User.objects.filter(
                    last_login__gte=today - timedelta(days=7)
                ).count(),
            },
            'distribution': {
                'by_status': {
                    'active': active_users,
                    'inactive': total_users - active_users
                },
                'by_role': {
                    'regular': total_users - staff_users,
                    'staff': staff_users,
                    'superuser': superusers
                }
            }
        })
    
    @action(detail=True, methods=['post'], url_path='toggle-active')
    def toggle_user_active(self, request, pk=None):
        """Toggle user active status"""
        user = self.get_object()
        
        # Prevent deactivating self
        if user == request.user:
            return Response({
                'error': 'Cannot deactivate your own account'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = not user.is_active
        user.save()
        
        action = 'activated' if user.is_active else 'deactivated'
        logger.info(f"User {action} by admin: {user.username}")
        
        return Response({
            'message': f'User {action} successfully',
            'is_active': user.is_active
        })

# Admin Dashboard
class AdminDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'], url_path='overview')
    def dashboard_overview(self, request):
        """Get admin dashboard overview"""
        cache_key = f'admin_dashboard_{timezone.now().date()}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        today = timezone.now().date()
        
        overview = {
            'summary': {
                'total_customers': User.objects.count(),
                'total_businesses': Business.objects.count(),
                'active_promotions': Promotion.objects.filter(
                    is_active=True,
                    end_date__gte=timezone.now()
                ).count(),
                'monthly_revenue': Analytics.objects.filter(
                    date__month=today.month,
                    date__year=today.year
                ).aggregate(total=Sum('revenue'))['total'] or 0,
            },
            'today': {
                'new_users': User.objects.filter(date_joined__date=today).count(),
                'new_businesses': Business.objects.filter(created_at__date=today).count(),
                'map_views': MapView.objects.filter(viewed_at__date=today).count(),
                'promotions_created': Promotion.objects.filter(created_at__date=today).count(),
            },
            'system': {
                'active_sessions': 0,  # Would need session tracking
                'api_requests_today': 0,  # Would need request logging
                'uptime': '99.9%',  # Mock data
                'last_backup': (today - timedelta(days=1)).isoformat(),
            }
        }
        
        # Cache for 1 minute
        cache.set(cache_key, overview, 60)
        
        return Response(overview)
    
    @action(detail=False, methods=['get'], url_path='activity-logs')
    def activity_logs(self, request):
        """Get recent activity logs (mock data - implement proper logging)"""
        # In production, use a proper logging system
        logs = [
            {
                'id': 1,
                'timestamp': timezone.now().isoformat(),
                'level': 'INFO',
                'action': 'User login',
                'user': request.user.username,
                'ip_address': request.META.get('REMOTE_ADDR', 'unknown'),
                'details': 'Successful authentication'
            },
            {
                'id': 2,
                'timestamp': (timezone.now() - timedelta(minutes=5)).isoformat(),
                'level': 'INFO',
                'action': 'Promotion created',
                'user': 'business_owner',
                'ip_address': '192.168.1.100',
                'details': 'New promotion "Summer Sale" created'
            },
        ]
        
        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        return Response({
            'results': logs[start_idx:end_idx],
            'count': len(logs),
            'total_pages': (len(logs) + page_size - 1) // page_size,
            'current_page': page
        })

