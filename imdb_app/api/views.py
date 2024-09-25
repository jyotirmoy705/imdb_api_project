from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets,filters
from imdb_app.api.throttles import WatchListThrottle, ReviewThrottle
from rest_framework.exceptions import ValidationError
from imdb_app.api.serializers import WatchlistSerializer, StreamPlatformSerializer, ReviewSerializer
from imdb_app.models import Watchlist, StreamPlatform, Review
from imdb_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from imdb_app.api.paginations import WatchlistPagination
from django.db.models import Sum, Count

def UpdateAvgRating(pk, review): # To update review count and average rating in Review table which will take watchlist id and review object as argument
    watchlist = Watchlist.objects.get(pk=pk)
    ratings = Review.objects.filter(watchlist=review.watchlist).aggregate(
        total_rating = Sum('rating'),
        count = Count('rating')
    )
    
    if ratings['count'] > 0:
        avg_rating = round(float(ratings['total_rating']) / ratings['count'], 1)
    else:
        avg_rating = 0

    cserializer = WatchlistSerializer(watchlist, data={'avg_rating': avg_rating, 'rating_count': ratings['count']}, partial=True)
    if cserializer.is_valid():
        cserializer.save()
    else:
        # Handle serializer errors as needed
        print(cserializer.errors)
    

class WatchlistGV(generics.ListAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    pagination_class = WatchlistPagination
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    # filterset_fields = ['title', 'active', 'platform__name']
    search_fields = ['title', 'active']
# class WatchlistAV(viewsets.ModelViewSet):

class StreamPlatformAV(viewsets.ModelViewSet):

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [AdminOrReadOnly]
    

class WatchlistAV(APIView):
    permission_classes = [AdminOrReadOnly]
    pagination_class = WatchlistPagination
    # throttle_classes = [WatchListThrottle]
    def get(self, request):
        watchlist = Watchlist.objects.all()
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)
    def post(self, request):

        serializer = WatchlistSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
       

class WatchdetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    # throttle_classes = [WatchListThrottle]
    def get(self, request, pk):
        try:
            watched = Watchlist.objects.get(pk = pk)
            serializer = WatchlistSerializer(watched)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            watched = Watchlist.objects.get(pk=pk)
            serializer = WatchlistSerializer(watched, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def patch(self, request, pk):
        try:
            watched = Watchlist.objects.get(pk=pk)
            serializer = WatchlistSerializer(watched, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            watched = Watchlist.objects.get(pk=pk)
            watched.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
##########################################
    
    
class WatchlistwiseReviewAV(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # To get reviews related to a perticular watchlist having id = pk. 'queryset = Review.objects.all()' is removed to avoid getting all reviews instead of specific.
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)
######################################################   
class WatchlistwiseReviewCreateAV(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]    
    
    def post(self, request, pk):
        watchlist = Watchlist.objects.get(pk = pk)
        reviewer = self.request.user
        review_queryset = Review.objects.filter(watchlist = watchlist, reviewer = reviewer) 
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watchlist.")
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(watchlist=watchlist, reviewer = reviewer)
            review = Review.objects.get(pk = serializer.data['id'])
            UpdateAvgRating(pk, review)
            return Response(status = status.HTTP_201_CREATED)
        else:     
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 
        
class ReviewDetailAV(APIView):
    permission_classes = [ReviewUserOrReadOnly]
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk = pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def patch(self,request, pk):
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review, data = request.data, partial = True)
           
        if serializer.is_valid():
            serializer.save() 
            UpdateAvgRating(review.watchlist.pk, review)                
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            self.check_object_permissions(request, review)  # Check permissions

            review.delete()
            UpdateAvgRating(review.watchlist.pk, review)
            
            return Response({'status': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
  