from django.urls import path


from . import views
urlpatterns = [
    # Catrgory Urls
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Question Urls
    path('question/', views.question_index, name='question_index'),
    path('question/create/', views.CreateQuestion.as_view() , name='create_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/<int:pk>/update/', views.QuestionUpdate.as_view(), name='update_question'),
    path('question/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question_delete'),
    #add answer to question
    path('question/<int:question_id>/add_answer', views.answer_create, name='answer_create'),

    # Answer Urls
    path('answer/<int:answer_id>/', views.answer_detail, name="answer_detail"),
    path('answer/<int:pk>/update/', views.AnswerUpdate.as_view(), name="answer_update"),
    path('answer/<int:pk>/delete/', views.AnswerDelete.as_view(), name="answer_delete"),
    #add reply to question
    path('answer/<int:answer_id>/add_reply', views.reply_create, name='reply_create'),
   
    # Reply Urls
    path('reply/', views.reply_index, name="reply_index"),
    path('reply/<int:reply_id>', views.reply_detail, name="reply_detail"),
    path('reply/<int:pk>/update/', views.ReplyUpdate.as_view(), name="reply_update"),
    path('reply/<int:pk>/delete/', views.ReplyDelete.as_view(), name="reply_delete"),

    # Auth Urls
    path('signup/', views.signup, name='signup'),
    path('change_password/', views.change_password, name='change_password'),
    
    # Profile Urls
    path('profile/', views.profile_index, name='profile_index'),
    path('profile/list', views.profile_list, name='profile_list'),
    path('profile/update', views.profile_update, name='profile_update'),
    path('profile/answer/', views.profile_answer, name="profile_answer"),
    path('profile/question/', views.profile_question, name="profile_question"),
    path('profile/<int:user_id>', views.profile_detail, name='profile_detail'),
    
    # Category Urls
    path('category/<int:category_id>', views.category_detail, name='category_detail'),

    # like answer
    path('like/<int:pk>/answer', views.like_answer, name='like_answer'),

    # dislike answer
    path('dislike/<int:pk>/answer', views.dislike_answer, name='dislike_answer'),
]