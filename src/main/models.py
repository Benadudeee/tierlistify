from django.db import models
from django.utils import timezone
from userprofile.createprofile import Profile
import random


def create_post_id():
    post_id = ""
    for i in range(12):
        post_id += str(random.randint(0, 10))

    return post_id


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PostTag(BaseModel):
    name = models.CharField(max_length=30)
    def __str__(self):
        return f"tagname: {self.name}"
    
class TierListPost(BaseModel):
    id = models.BigIntegerField(primary_key=True, default=create_post_id)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=550, default="")
    likes = models.ManyToManyField(Profile, related_name="likedtierlistposts")
    tags = models.ManyToManyField(PostTag, related_name="posttags")
    is_private = models.BooleanField(default=False)

    def number_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return f"""
            id: {self.id}  
            author: {self.author}  
            title: {self.name}
        """
    
    def get_tiers(self):
        pass

class Tier(BaseModel):
    pass

# class TierListEntry(models.Model):
#     id = models.IntegerField(primary_key=True, default=create_post_id())
#     post = models.ForeignKey(TierListPost, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     image = models.ImageField(upload_to="img/%y")


#     def get_total_points(self):
#         points = 0

#         for rating in self.entryrating_set.all():
#             points += rating.rating
        
#         return points
    
#     def get_total_inputs(self):
#         return self.entryrating_set.count()
    
#     def get_average(self):
#         total_points = self.get_total_points()
#         total_inputs = self.get_total_inputs()

#         if(total_inputs == 0):
#             total_inputs = 1
        
#         average = round(total_points / total_inputs, 2)

#         return average

# # Stores where the user rated the entries
# class EntryRating(models.Model):
#     entry = models.ForeignKey(TierListEntry, on_delete=models.CASCADE) # The entry that was rated
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # The user who rated the entry
#     rating = models.IntegerField(default=0)
