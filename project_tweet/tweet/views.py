from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.


def index(request):
    return render(request, "index.html")


# to get all the tweets


def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request, "tweet_list.html", {"tweets": tweets})


# to create tweets


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            # save the tweet if it's valid but not on the DB
            tweet = form.save(commit=False)
            # get the user who tweeted
            tweet.user = request.user
            # save in the DB
            tweet.save()
            return redirect("tweet_list")
    else:
        form = TweetForm()

    return render(request, "tweet_form.html", {"form": form})


# to edit the tweet, always 'instance'


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("tweet_list")
    else:
        form = TweetForm(instance=tweet)
    return render(request, "tweet_form.html", {"form": form})


# to delete the tweet


def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect("tweet_list")
    return render(request, "tweet_delete.html", {"tweet": tweet})


# user registration


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("tweet_list")
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})
