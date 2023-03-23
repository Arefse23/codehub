
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Question, Category, Answer, Reply, Profile, Badge
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import SignUpForm, UpdateProfileForm, UpdateUserForm, CreateAnswerForm, CreateReplyForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse


# =======================Category Section========================

def home(request):
    categories = Category.objects.all().order_by('id')
    questions = None
    for category in categories:
        if(questions is None):
            questions = Question.objects.filter(category=category).order_by('-date')[:3]
        else:
            questions |= Question.objects.filter(category=category).order_by('-date')[:3]
    return render(request,'home.html', {'categories': categories, 'questions': questions})

def about(request):
    return render(request,'about.html')


# =======================Qustion Section========================

def question_index(request):
    #Search for questions
    search = request.GET.get('search')
    if(search is None ):
        questions = Question.objects.all()
    else:
        questions = Question.objects.filter(title__icontains = search)
    categories = Category.objects.all().order_by('id')
    return render(request,'question/question_index.html', 
    {'questions': questions.order_by('-id'), 'categories': categories})

def question_detail(request, question_id):
    question= Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question=question).order_by('-id')
    answer_form = CreateAnswerForm()
    return render(request, 'question/question_detail.html', {'question': question, 'answers':answers, 'answer_form': answer_form})

class CreateQuestion(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model= Question
    fields = ['title', 'body', 'category']
    success_message = 'Question created successfully!'
    def form_valid(self, form) :
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class QuestionUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Question
    fields = ['title', 'body', 'category']
    success_message = 'Question updated successfully!'
    def form_valid(self, form) :
        if form.instance.user != self.request.user:
            messages.error(self.request,'Error: not authorized!')
            return redirect('home')
        return super().form_valid(form)

class QuestionDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Question
    success_url = '/question/'
    success_message = 'Question removed successfully!'
    def form_valid(self, form) :
        if self.object.user != self.request.user:
            messages.error(self.request,'Error: not authorized!')
            return redirect('home')
        return super().form_valid(form)

# =======================Answer Section========================
def answer_detail(request, answer_id):
    answer= Answer.objects.get(id=answer_id)
    replies = Reply.objects.filter(answer=answer).order_by('-id')
    reply_form = CreateReplyForm()
    return render(request, 'answer/answer_detail.html', {'answer': answer, 'replies': replies, 'reply_form': reply_form})

@login_required
def answer_create(request, question_id):
    form = CreateAnswerForm(request.POST)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.question = Question.objects.get(id=question_id)
        answer.user = request.user
        answer.save()
        messages.success(request, 'Answer created successfully!')
    return redirect('question_detail', question_id = question_id)

class AnswerUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Answer
    fields = ['title', 'body']
    success_message = 'Answer updated successfully!'
    def form_valid(self, form) :
        if form.instance.user != self.request.user:
            messages.error(self.request,'Error: not authorized!')
            return redirect('home')
        return super().form_valid(form)


class AnswerDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Answer
    success_message = 'Answer deleted successfully!'
    def get_success_url(self):
        return reverse('question_detail', args=([str(self.object.question.id)]))
    def form_valid(self, form) :
        if self.object.user != self.request.user:
            messages.error(self.request,'Error: not authorized!')
            return redirect('home')
        return super().form_valid(form)

# =======================Reply Section========================

def reply_index(request):
    replies = Reply.objects.all()
    return render(request,'reply/reply_index.html', {'replies': replies})

def reply_detail(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    return render(request, 'reply/reply_detail.html', {'reply': reply })

@login_required
def reply_create(request, answer_id):
    form = CreateReplyForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.answer = Answer.objects.get(id=answer_id)
        reply.user = request.user
        reply.save()
        messages.success(request, 'Reply created successfully!')
    return redirect('answer_detail', answer_id = answer_id)
    

class ReplyUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Reply
    fields = ['title', 'body']
    success_message = 'Reply updated successfully!'
    def form_valid(self, form) :
        if form.instance.user != self.request.user:
            messages.error(self.request,'Error: not authorized!')
            return redirect('home')
        return super().form_valid(form)
    

class ReplyDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Reply
    success_message = 'Reply deleted successfully!'
    def get_success_url(self):
        return reverse('answer_detail', args=([str(self.object.answer.id)]))
    def form_valid(self, form) :
        if self.object.user != self.request.user:
            messages.error(self.request,'Error: not authorized!')
            return redirect('home')
        return super().form_valid(form)


# =======================Auth Section========================

def signup(request):
    if request.method == 'POST':
        # Make a 'user' form object with the data from the browser
        form = SignUpForm(request.POST)
        if form.is_valid():
            # save user to DB
            user = form.save()
            # Log in the user automatically once they sign up
            login(request, user)
            messages.success(request,f"Account was successfully created! Welcome {user.username}!")
            return redirect('home')
        
    # If there's a bad post or get request
    formSecond = SignUpForm()
    try:
        formSecond.errors.update(form.errors)
    except Exception as e:
        print(e)
    context = {'form': formSecond}
    return render(request, 'registration/signup.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        # Make a 'user' form object with the data from the browser
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            login(request, request.user)
            messages.success(request,"Your password has been changed successfully!")
            return redirect('home')
        
    # If there's a bad post or get request
    formSecond = PasswordChangeForm(request.user)
    try:
        formSecond.errors.update(form.errors)
    except Exception as e:
        print(e)
    context = {'form': formSecond}
    return render(request, 'registration/change_password.html', context)



# =======================Profile Section========================
@login_required
def profile_index(request):
    profile = Profile.objects.get(user = request.user)
    badges_profile_doesnt_have = Badge.objects.exclude(id__in = profile.badges.all().values_list('id'))
    return render(request, 'profile/index.html', {'badges' : badges_profile_doesnt_have} )

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request,'profile/profile_list.html', {'profiles': profiles})

def profile_detail(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'profile/profile_detail.html', {'selected_user': user })

@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile_index')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile/update.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile_question(request):
    questions = Question.objects.filter(user = request.user)
    return render(request,'question/questionp_index.html', {'questions': questions.order_by('-id')})

@login_required
def profile_answer(request):
    answers = Answer.objects.filter(user = request.user)
    return render(request,'answer/answer_index.html', {'answers': answers})


# =======================Category Section========================

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category).order_by('-date')
    return render(request, 'category/detail.html', {'category': category, 'questions': questions})

# =======================Badge Section========================

def check_badge(user, point_difference):
    #modify user profile points
    profile = Profile.objects.get(user=user)
    profile.points += point_difference
    #add badge to user profile
    badges = Badge.objects.filter(point_limit=profile.points)
    for badge in badges:
        if(not profile.badges.contains(badge)):
            profile.badges.add(badge)
    profile.save()

# =======================Like/Dislike Section========================
@login_required
def like_answer(request, pk):
    answer = Answer.objects.get(pk=pk)
    #toggle like
    if(answer.likes.contains(request.user)):
        answer.likes.remove(request.user)
        check_badge(answer.user, -1)
        messages.success(request, 'Answer like removed successfully!')
    else:
        answer.likes.add(request.user)
        check_badge(answer.user, 1)
        messages.success(request, 'Answer like added successfully!')
    #remove dislike from answer if it exists
    if(answer.dislikes.contains(request.user)):
        answer.dislikes.remove(request.user)
    #save changes to answer
    answer.save()
    return redirect(f'/question/{answer.question.id}')

@login_required
def dislike_answer(request, pk):
    answer = Answer.objects.get(pk=pk)
    #toggle dislike
    if(answer.dislikes.contains(request.user)):
        answer.dislikes.remove(request.user)
        check_badge(answer.user, 1)
        messages.success(request, 'Answer dislike removed successfully!')
    else:
        answer.dislikes.add(request.user)
        check_badge(answer.user, -1)
        messages.success(request, 'Answer dislike added successfully!')
    #remove dislike from answer if it exists
    if(answer.likes.contains(request.user)):
        answer.likes.remove(request.user)
    #save changes to answer
    answer.save()
    return redirect(f'/question/{answer.question.id}')
