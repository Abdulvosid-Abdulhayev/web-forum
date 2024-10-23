from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Comment
from .forms import TopicForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

def index(request):
    topics = Topic.objects.all().order_by('-created_at')
    return render(request, 'forum/index.html', {'topics': topics})

@login_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = TopicForm()
    return render(request, 'forum/create_topic.html', {'form': form})

@login_required
def update_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.user != topic.author:
        return redirect('topic_detail', pk=pk)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', pk=pk)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'forum/update_topic.html', {'form': form})

def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    comments = topic.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.topic = topic
            comment.author = request.user
            comment.save()
            return redirect('topic_detail', pk=pk)
    else:
        comment_form = CommentForm()
    return render(request, 'forum/topic_detail.html', {
        'topic': topic,
        'comments': comments,
        'comment_form': comment_form,
    })

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
