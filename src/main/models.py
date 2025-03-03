from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import random

# Create your models here.

# This is a signal that creates a new profile when a User is created
def create_profile(sender, instance, created, **kwargs):
    if created: # When a new instance of User is made
        # Creates a Profile connecting to the user and saves it
        user_profile = Profile(user=instance)
        user_profile.save()

# Puts it all together. Basically says that it'll call this function AFTER the User model is created
post_save.connect(create_profile, sender=User)

# Create Post ID: 
#   - Creates a 12 long string of random integers ranging from 0 to 10

def create_post_id():
    post_id = ""
    for i in range(12):
        post_id += str(random.randint(0, 10))

    return post_id

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_url = models.ImageField(upload_to="users/", default="users/default.png")

    def __str__(self):
        return self.user.username


class PostTag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"tagname: {self.name}"

class TierListPost(models.Model):
    id = models.IntegerField(primary_key=True, default=create_post_id())
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=550, default="")
    likes = models.ManyToManyField(User, related_name="likedtierlistposts")
    tags = models.ManyToManyField(PostTag, related_name="posttags")

    def number_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return f"""
            id: {self.id}  
            author: {self.author}  
            title: {self.name}
        """


class TierListEntry(models.Model):
    id = models.IntegerField(primary_key=True, default=create_post_id())
    post = models.ForeignKey(TierListPost, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="img/%y")


    def get_total_points(self):
        points = 0

        for rating in self.entryrating_set.all():
            points += rating.rating
        
        return points
    
    def get_total_inputs(self):
        return self.entryrating_set.count()
    
    def get_average(self):
        total_points = self.get_total_points()
        total_inputs = self.get_total_inputs()

        if(total_inputs == 0):
            total_inputs = 1
        
        average = round(total_points / total_inputs, 2)

        return average

# Stores where the user rated the entries
class EntryRating(models.Model):
    entry = models.ForeignKey(TierListEntry, on_delete=models.CASCADE) # The entry that was rated
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # The user who rated the entry
    rating = models.IntegerField(default=0)
