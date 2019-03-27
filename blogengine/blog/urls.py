from django.urls import path, include

from .views import (
    posts_list, tags_list,
    PostCreate, PostUpdate, PostDetail, PostDelete,
    TagCreate, TagUpdate, TagDetail, TagDelete
)


post_paths = [
    path('create/', PostCreate.as_view(), name='post_create_url'),
    path('<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('<str:slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('<str:slug>/delete/', PostDelete.as_view(), name='post_delete_url')
]

tag_paths = [
    path('', tags_list, name='tags_list_url'),
    path('create/', TagCreate.as_view(), name='tag_create_url'),
    path('<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('<str:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url')
]

urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('post/', include(post_paths)),
    path('tags/', include(tag_paths))
]
