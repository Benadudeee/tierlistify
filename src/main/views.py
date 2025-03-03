from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.http import JsonResponse
from .models import TierListEntry, TierListPost, EntryRating, Profile, PostTag
from .forms import RateEntryForm
from django.http import HttpResponse

# Display User Function: Returns data about the User if they're logged into their account
def get_user_or_anon(req):
    try:
        user = User.objects.get(username=req)

        return user
    except:
        return AnonymousUser

# Create your views here.

"""
Returns all TierListPosts from the db
"""
def home(request):
    qs = TierListPost.objects.all()
    user_or_anonymous = get_user_or_anon(request.user)
    # Get the most popular entries

    data = {
        "posts" : qs,
        "user" : user_or_anonymous
    }

    return render(request, 'general/home.html', data)

"""
Gets all the posts based on the selected tag

@param tagname: The name of the selected tag
"""
def posts_by_tag(request, tagname):
    tag = get_object_or_404(PostTag, name=tagname)
    user_or_anonymous = get_user_or_anon(request.user)

    qs = TierListPost.objects.filter(tags=tag)

    data = {
        "posts" : qs,
        "user" : user_or_anonymous
    }

    return render(request, 'general/home.html', data)


"""
Gets a profile based on the given username

@param username: A username in the database
"""
def profile(request, username):
    print(username)
    user = User.objects.get(username=username)

    user_posts = user.profile.tierlistpost_set.all()

    data = {
        "posts" : user_posts,
        "profile" : user.profile,
    }

    return render(request, 'general/profile.html', data)

@login_required
def create_post(request):
    pass

@login_required
def create_entry(request, post_id):
    pass

@login_required
def like(request, post_id):
    user = User.objects.get(username=request.user)
    post = get_object_or_404(TierListPost, id=post_id)

    if(post.likes.filter(username=user.username).exists()):
        post.likes.remove(user)
    else:
        post.likes.add(user)
    
    return JsonResponse({"likes": post.number_of_likes()})

"""
Gets a posts given it's id

@param post_id: The id of the selected post
"""
def get_post(request, post_id):
    user_or_anonymous = get_user_or_anon(request.user)
    post = get_object_or_404(TierListPost, id=post_id)

    data = {
        "post": post,
        "entries": post.tierlistentry_set.all(),
        "user" : user_or_anonymous
    }

    return render(request, "general/post.html", data)

"""
Gets a post entry by its id

@param post_id: The id of the post from the entry
@param entry_id: The id of the entry
"""
def post_entry(request, post_id, entry_id):
    user_or_anonymous = get_user_or_anon(request.user)

    post = get_object_or_404(TierListPost, id=post_id)
    post_entry = get_object_or_404(TierListEntry, id=entry_id)
    
    
    if request.method == "POST":
        form = RateEntryForm(request.POST)

        if form.is_valid():
            rating = int(form.cleaned_data["rating"])

            if(user_or_anonymous.is_anonymous):
                return redirect("/login")

            entry_rating = EntryRating.objects.get_or_create(profile=user_or_anonymous.profile, entry=post_entry)[0]
            entry_rating.rating = int(rating)

            entry_rating.save()

            data = {
                "post" : post,
                "post_entry" : post_entry,
                "form" : form,
                "user" : user_or_anonymous
            }
            return render(request, 'general/widgets/post_entry_profile.html', data)
    else:
        #Post Form
        form = RateEntryForm()

        data = {
            "post" : post,
            "post_entry" : post_entry,
            "form" : form,
            "user" : user_or_anonymous
        }

        return render(request, "general/post_entry.html", data)

