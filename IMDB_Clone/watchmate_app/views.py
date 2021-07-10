import re
from django.core.exceptions import ValidationError
from django.db import reset_queries
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAdminUser
#from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
#from watchmate_app.throttling import ReviewCreateThrottle,ReviewListThrottle

#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from watchmate_app.permissions import IsReviewed_user_Or_Read_only,IsAdminOrReadOnly
from watchmate_app.pagination import WatchListPagination,WatchListLOPagination,WatchListCPagination
from .serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from .models import WatchList,StreamPlatform,Review

class UserReview(generics.ListAPIView):

    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)

class ReviewCreate(generics.CreateAPIView):
    #throttle_classes = [ReviewCreateThrottle]
    permission_classes = [IsAuthenticated]

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(review_user=review_user,watchlist=watchlist)

        if review_queryset.exists():
            raise ValidationError ("You have already reviewed this !!!")
        
        # count = Review.objects.all().count()
        
        # if count == 0:
        #      watchlist.avg_ratings = 0
        #      watchlist.number_of_ratings=0
 
        if watchlist.number_of_ratings == 0:
            watchlist.avg_ratings = serializer.validated_data['rating']
        else:
            watchlist.avg_ratings = (watchlist.avg_ratings+serializer.validated_data['rating'])/2

        watchlist.number_of_ratings+=1
        watchlist.save()
        serializer.save(watchlist=watchlist,review_user=review_user)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewed_user_Or_Read_only]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
 
class ReviewList(generics.ListAPIView):
    #throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    permission_classes = [IsAuthenticated]
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['review_user__username', 'active']
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['review_user__username', 'description']
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['review_user__username', 'description']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)


# class ReviewDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class WatchListView2(generics.ListAPIView):
    pagination_class = WatchListCPagination
    serializer_class = WatchListSerializer
    queryset = WatchList.objects.all()

class WatchListView(APIView):

    #throttle_classes = [UserRateThrottle,AnonRateThrottle]
    
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchDetailView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except:
            return Response({'error': 'not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatormListView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self,request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except:
            return Response({'error':'not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
            
    def delete(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






    

