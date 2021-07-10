from django.urls import path,include
from .views import UserReview,WatchListView,WatchListView2,ReviewCreate,WatchDetailView,StreamPlatormListView,StreamPlatformDetailView,ReviewList,ReviewDetail

urlpatterns = [

    path('list/', WatchListView.as_view(),name='watch-list-view'),
    path('list2/', WatchListView2.as_view(),name='watch-list-view2'),
    path('<int:pk>',WatchDetailView.as_view(), name = 'watch-detail-view'),

    path('stream/',StreamPlatormListView.as_view(),name='stream-platform-list-view'),
    path('stream/<int:pk>',StreamPlatformDetailView.as_view(),name='stream-platform-detail-view'),  

    path('<int:pk>/reviews-create/',ReviewCreate.as_view(), name = 'review-create'),
    path('<int:pk>/reviews/',ReviewList.as_view(), name = 'review-list'),
    path('reviews/<int:pk>',ReviewDetail.as_view(), name = 'review-detail'),

    path('review/',UserReview.as_view(), name = 'user-review')

]