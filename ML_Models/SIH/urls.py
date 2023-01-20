from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("article-summarizer/", views.ArticleSummarizer.as_view(), name="article_summarizer"),
    path("text-summarizer/", views.TextSummarizer.as_view(), name="text_summarizer")
]
