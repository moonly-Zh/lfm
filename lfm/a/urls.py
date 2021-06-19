from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^follow/', views.follow),
    url(r'^delfollow/', views.del_follow),
    url(r'^regist/', views.regist),
    url(r'^login/', views.login),
    url(r'^remark/', views.remark),
    url(r'^like/', views.like),
    url(r'^dellike/', views.del_like),
    url(r'^articl/', views.dispatcher),
    url(r'^ShowMyArticles/', views.show_my_articles),
    url(r'^SearchByLocation/', views.search_articles_by_location),
    url(r'^SearchByDate/', views.search_articles_by_date),
    url(r'^ArticleDetail/', views.article_detail),
    url(r'^Summary/', views.summary),
    url(r'^MyLike/', views.myLike),
    url(r'^ShowFollow/', views.show_follow),
    url(r'^addarticl/', views.add_article),
]