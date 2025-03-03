from django.test import TestCase
from django.contrib.auth.models import User
from .models import TierListPost, TierListEntry, EntryRating

# Create your tests here.
class AllGeneralTests(TestCase):
    def test_tlp_is_working(self):
        user = User.objects.create_user("john", "lennon@gmail.com", "password")
        tlp = TierListPost.objects.create(author=user.profile, name="tier list post", description="tier list post description")

        self.assertEquals(tlp.name, "tier list post")

    
    def test_user_like_updates_like(self):
        user = User.objects.create_user("john", "lennon@gmail.com", "password")
        tlp = TierListPost.objects.create(author=user.profile, name="tier list post", description="tier list post description")

        tlp.likes.add(user)

        self.assertEqual(1, tlp.number_of_likes())

    def test_can_get_user_from_likes(self):
        user = User.objects.create_user("john", "lennon@gmail.com", "password")

        tlp = TierListPost.objects.create(author=user.profile, name="tier list post", description="tier list post description")

        tlp.likes.add(user)

        self.assertTrue(tlp.likes.filter(username=user.username).exists())

    def test_get_all_user_likes(self):
        user = User.objects.create_user("john", "lennon@gmail.com", "password")

        tlp = TierListPost.objects.create(author=user.profile, name="tier list post", description="tier list post description")
        tlp2 = TierListPost.objects.create(author=user.profile, name="tier list post2", description="tier list post description2")
        tlp3 = TierListPost.objects.create(author=user.profile, name="tier list post2", description="tier list post description3")

        tlp.likes.add(user)
        tlp2.likes.add(user)
        tlp3.likes.add(user)

        user_liked_posts = user.likedtierlistposts.all()

        for post in user_liked_posts:
            print(post)

        self.assertEqual(user_liked_posts.count(), 3)

    def test_user_rating_created(self):
            user = User.objects.create_user("john", "lennon@gmail.com", "password")
            tlp = TierListPost.objects.create(author=user.profile, name="tier list post", description="tier list post description")
            tle = TierListEntry.objects.create(post=tlp, name="entry")

            rating = EntryRating.objects.create(entry=tle, profile=user.profile, rating=5)

            self.assertTrue(user.profile == rating.profile)

    def test_rating_access(self):
        user = User.objects.create_user("john", "lennon@gmail.com", "password")
        tlp = TierListPost.objects.create(author=user.profile, name="tier list post", description="tier list post description")
        tle = TierListEntry.objects.create(post=tlp, name="entry")

        rating = EntryRating.objects.create(entry=tle, profile=user.profile, rating=5)

        print(tle.get_total_points())
        self.assertTrue(True)

    def test_entryrating_count(self):
        user = User.objects.create_user("john", "lennon@gmail.com", "password")
        tlp = TierListPost.objects.create(author=user.profile, name="tier list post", description="tier list post description")
        tle = TierListEntry.objects.create(post=tlp, name="entry")

        rating = EntryRating.objects.create(entry=tle, profile=user.profile, rating=5)

        self.assertTrue(tle.get_total_inputs() == 1)

    def test_entryrating_average(self):
        user = User.objects.create_user("john", "lennon@gmail.com", "password")
        tlp = TierListPost.objects.create(author=user.profile, name="tier list post", description="tier list post description")
        tle = TierListEntry.objects.create(post=tlp, name="entry")

        rating = EntryRating.objects.create(entry=tle, profile=user.profile, rating=3)
        rating2 = EntryRating.objects.create(entry=tle, profile=user.profile, rating=2)

        self.assertTrue(tle.get_average() == 2.5)
         

    