from datetime import date
import importlib
import django
import os
from django.http import request, response
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from meme_portal.models import Post, Forum, Comment, UserProfile
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from .views import like_link, dislike_link, user_account, my_posts

def add_forum(name):
    forum = Forum.objects.get_or_create(name=name)[0]
    forum.save()
    return forum

def add_post(forum, title, img_url, author):
    post = Post.objects.get_or_create(forum=forum, name=title, img_url=img_url, author=author)[0]
    post.save()
    return post

def add_comment(post, content, author):
    comment = Comment.objects.get_or_create(post=post, content=content, author=UserProfile.objects.get(user=(User.objects.get(username=author))))[0]
    comment.save()
    return comment

def add_userProfile(username = 'bob02', password = 'hello', profile_pic = '/media/profile_images/bob_02_profile.png'):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
     
    try:
        u = User.objects.create_user(username, password=password)
    except django.db.utils.IntegrityError:
        u = User.objects.get(username=username)
    u.save()
     
    up = UserProfile.objects.get_or_create(user=u)[0]
    with open(BASE_DIR + profile_pic, 'rb') as f:
        data = f.read()

    up.picture.save(f'{username}_porfile_pic', ContentFile(data))
    up.save()
    return up

def add_like(post, usr):
    post.likes.add(usr)
    
def add_dislike(post, usr):
    post.dislikes.add(usr)

class IndexViewTests(TestCase):
    def test_index_view_with_no_forums(self):
        """
        If no forums exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('meme_portal:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no forums present.')
        self.assertQuerysetEqual(response.context['forum_data'], [])
    
    def test_index_view_with_empty_forums(self):
        """
        Ensure that the index page shows nothing if all forums present have no data within them
        """
        add_forum('cs_memes')
        add_forum('Hello_world')
        add_forum('math_memes')

        response = self.client.get(reverse('meme_portal:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'cs_memes')
        self.assertNotContains(response, 'Hello_world')
        self.assertNotContains(response, 'math_memes')

        self.assertContains(response, 'There are no forums present.')

        num_forums = len(response.context['forum_data'])
        self.assertEquals(num_forums, 0)

    def test_index_view_with_3_filled_forums(self):
        """
        Checks whether all 3 forms are diplsyed, no dupicates are sent to the page
        """
        cs = add_forum('cs_memes')
        HW = add_forum('Hello_world')
        math = add_forum('math_memes')

        usr = add_userProfile()

        add_post(cs, "title", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", usr)
        add_post(HW, "other_title", "http://thewowstyle.com/wp-content/uploads/2015/01/nature-images.jpg", usr)
        add_post(math, "another_title", "https://eskipaper.com/images/images-2.jpg", usr)

        response = self.client.get(reverse('meme_portal:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'cs_memes')
        self.assertContains(response, 'Hello_world')
        self.assertContains(response, 'math_memes')

        num_forums = len(response.context['forum_data'])
        self.assertEquals(num_forums, 3)

    def test_index_view_with_3_filled_forums_and_1_empty(self):
        """
        Checks that only 3 forms are diplsyed, no dupicates are sent to the page and the empty forum is not displayed
        """
        cs = add_forum('cs_memes')
        HW = add_forum('Hello_world')
        math = add_forum('math_memes')
        hm = add_forum('history_memes')

        usr = add_userProfile()

        add_post(cs, "title", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", usr)
        add_post(HW, "other_title", "http://thewowstyle.com/wp-content/uploads/2015/01/nature-images.jpg", usr)
        add_post(math, "another_title", "https://eskipaper.com/images/images-2.jpg", usr)

        response = self.client.get(reverse('meme_portal:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'cs_memes')
        self.assertContains(response, 'Hello_world')
        self.assertContains(response, 'math_memes')

        num_forums = len(response.context['forum_data'])
        self.assertEquals(num_forums, 3)

    def test_index_view_with_5_filled_forums(self):
        """
        Checks whether all 5 forms are diplsyed, no dupicates and all are present
        """
        cs = add_forum('cs_memes')
        HW = add_forum('Hello_world')
        math = add_forum('math_memes')
        hm = add_forum('history_memes')
        am = add_forum('another_meme')

        usr = add_userProfile()

        add_post(cs, "title", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", usr)
        add_post(HW, "other_title", "http://thewowstyle.com/wp-content/uploads/2015/01/nature-images.jpg", usr)
        add_post(math, "another_title", "https://eskipaper.com/images/images-2.jpg", usr)
        add_post(hm, "title2", "https://hddesktopwallpapers.in/wp-content/uploads/2015/09/nice-images.jpg", usr)
        add_post(am, "other_title2", "https://wonderfulengineering.com/wp-content/uploads/2014/01/highway-wallpapers-15.jpg", usr)

        response = self.client.get(reverse('meme_portal:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'cs_memes')
        self.assertContains(response, 'Hello_world')
        self.assertContains(response, 'math_memes')
        self.assertContains(response, 'history_memes')
        self.assertContains(response, 'another_meme')

        num_forums = len(response.context['forum_data'])
        self.assertEquals(num_forums, 5)

    def test_index_view_with_6_filled_forums(self):
        """
        Ensure that only 5 forums are diplayed to the front page, any 5 however
        """
        cs = add_forum('cs_memes')
        HW = add_forum('Hello_world')
        math = add_forum('math_memes')
        hm = add_forum('history_memes')
        am = add_forum('another_meme')
        f6 = add_forum('forum_6')

        usr = add_userProfile()

        add_post(cs, "title", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", usr)
        add_post(HW, "other_title", "http://thewowstyle.com/wp-content/uploads/2015/01/nature-images.jpg", usr)
        add_post(math, "another_title", "https://eskipaper.com/images/images-2.jpg", usr)
        add_post(hm, "title2", "https://hddesktopwallpapers.in/wp-content/uploads/2015/09/nice-images.jpg", usr)
        add_post(am, "other_title2", "https://wonderfulengineering.com/wp-content/uploads/2014/01/highway-wallpapers-15.jpg", usr)
        add_post(f6, "other_title3", "http://thewowstyle.com/wp-content/uploads/2015/07/Natural-World-Wallpaper-HD-.jpg", usr)

        response = self.client.get(reverse('meme_portal:index'))
        self.assertEqual(response.status_code, 200)

        num_forums = len(response.context['forum_data'])
        self.assertEquals(num_forums, 5)

class ForumViewTests(TestCase):
    def test_froum_view_with_0_posts(self):
        """
        This method will test to see if the page diplays the correct message when no posts are present
        """
        mf = add_forum('meme_forum')
        response = self.client.get(reverse('meme_portal:show_forum', kwargs={'forum_name_slug':'meme_forum'}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This Forum contains no posts.')

        num_posts = len(response.context['posts'])
        self.assertEquals(num_posts, 0)

    def test_froum_view_doesnt_exist(self):
        """
        This method will test to see if the page diplays the correct message when the forum doesn't exist
        """
        response = self.client.get(reverse('meme_portal:show_forum', kwargs={'forum_name_slug':'meme_forum'}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This Forum does not exist yet.')

    def test_froum_view_with_some_posts(self):
        """
        This method will test to see if the page diplays all of the posts in the forum, with no repeats
        """
        mf = add_forum('meme_forum')
        usr = add_userProfile()

        add_post(mf, "title", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", usr)
        add_post(mf, "other_title", "http://thewowstyle.com/wp-content/uploads/2015/01/nature-images.jpg", usr)
        add_post(mf, "another_title", "https://eskipaper.com/images/images-2.jpg", usr)
        add_post(mf, "title2", "https://hddesktopwallpapers.in/wp-content/uploads/2015/09/nice-images.jpg", usr)
        add_post(mf, "other_title2", "https://wonderfulengineering.com/wp-content/uploads/2014/01/highway-wallpapers-15.jpg", usr)
        add_post(mf, "other_title3", "http://thewowstyle.com/wp-content/uploads/2015/07/Natural-World-Wallpaper-HD-.jpg", usr)

        response = self.client.get(reverse('meme_portal:show_forum', kwargs={'forum_name_slug':'meme_forum'}))

        self.assertEqual(response.status_code, 200)

        num_posts = len(response.context['posts'])
        self.assertEquals(num_posts, 6)

    def test_froum_view_best_first(self):
        """
        This method will test to see if the page diplays the posts sorted by likes, descending
        """
        mf = add_forum('meme_forum')

        usr1 = add_userProfile()
        usr2 = add_userProfile("bob", "Password1234", "/media/profile_images/user10_profile_pic.png")

        post_1 = add_post(mf, "post1", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", usr1)
        post_2 = add_post(mf, "post2", "http://thewowstyle.com/wp-content/uploads/2015/01/nature-images.jpg", usr2)
        post_3 = add_post(mf, "post3", "https://eskipaper.com/images/images-2.jpg", usr2)

        add_like(post_2, usr1)
        add_like(post_2, usr2)
        add_like(post_1, usr2)

        response = self.client.get(reverse('meme_portal:show_forum_sort', kwargs={'forum_name_slug':'meme_forum', 'sort_by':'top_posts'}))

        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['posts'][0], post_2)
        self.assertEquals(response.context['posts'][1], post_1)
        self.assertEquals(response.context['posts'][2], post_3)

    def test_froum_view_worst_first(self):
        """
        This method will test to see if the page diplays the posts sorted by likes, ascending
        """
        mf = add_forum('meme_forum')

        usr1 = add_userProfile()
        usr2 = add_userProfile("bob", "Password1234", "/media/profile_images/user10_profile_pic.png")

        post_1 = add_post(mf, "post1", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", usr1)
        post_2 = add_post(mf, "post2", "http://thewowstyle.com/wp-content/uploads/2015/01/nature-images.jpg", usr2)
        post_3 = add_post(mf, "post3", "https://eskipaper.com/images/images-2.jpg", usr2)

        add_like(post_2, usr1)
        add_like(post_2, usr2)
        add_like(post_1, usr2)

        response = self.client.get(reverse('meme_portal:show_forum_sort', kwargs={'forum_name_slug':'meme_forum', 'sort_by':'worst_posts'}))

        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['posts'][0], post_3)
        self.assertEquals(response.context['posts'][1], post_1)
        self.assertEquals(response.context['posts'][2], post_2)

    def test_froum_view_newest_first(self):
        """
        This method will test to see if the page diplays the posts sorted by time posted, descending
        """
        mf = add_forum('meme_forum')

        usr1 = add_userProfile()
        usr2 = add_userProfile("bob", "Password1234", "/media/profile_images/user10_profile_pic.png")

        post_1 = add_post(mf, "post1", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", usr1)
        post_2 = add_post(mf, "post2", "http://thewowstyle.com/wp-content/uploads/2015/01/nature-images.jpg", usr2)
        post_3 = add_post(mf, "post3", "https://eskipaper.com/images/images-2.jpg", usr2)

        add_like(post_2, usr1)
        add_like(post_2, usr2)
        add_like(post_1, usr2)

        response = self.client.get(reverse('meme_portal:show_forum_sort', kwargs={'forum_name_slug':'meme_forum', 'sort_by':'newest_first'}))

        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['posts'][0], post_3)
        self.assertEquals(response.context['posts'][1], post_2)
        self.assertEquals(response.context['posts'][2], post_1)

    def test_froum_view_oldest_first(self):
        """
        This method will test to see if the page diplays the posts sorted by time posted, ascending
        """
        mf = add_forum('meme_forum')

        usr1 = add_userProfile()
        usr2 = add_userProfile("bob", "Password1234", "/media/profile_images/user10_profile_pic.png")

        post_1 = add_post(mf, "post1", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", usr1)
        post_2 = add_post(mf, "post2", "http://thewowstyle.com/wp-content/uploads/2015/01/nature-images.jpg", usr2)
        post_3 = add_post(mf, "post3", "https://eskipaper.com/images/images-2.jpg", usr2)

        add_like(post_2, usr1)
        add_like(post_2, usr2)
        add_like(post_1, usr2)

        response = self.client.get(reverse('meme_portal:show_forum_sort', kwargs={'forum_name_slug':'meme_forum', 'sort_by':'oldest_first'}))

        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['posts'][0], post_1)
        self.assertEquals(response.context['posts'][1], post_2)
        self.assertEquals(response.context['posts'][2], post_3)

class LikeButtonTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.usr = add_userProfile()

    def test_like_button(self):
        """
        This method will test if a user is added to a posts likes if the correct get request is sent
        """
        mf = add_forum('meme_forum')
        post_1 = add_post(mf, "post1", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", self.usr)

        request = self.request_factory.get(reverse('meme_portal:like_post', kwargs={'forum_name_slug':'meme_forum', 'post_name_slug':post_1.slug}))
        request.user = self.usr.user

        response = like_link(request, 'meme_forum', post_1.slug)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(post_1.likes.count(), 1)

    def test_like_button(self):
        """
        This method will test if a user is added to a posts dislikes if the correct get request is sent
        """
        mf = add_forum('meme_forum')
        post_1 = add_post(mf, "post1", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", self.usr)

        request = self.request_factory.get(reverse('meme_portal:dislike_post', kwargs={'forum_name_slug':'meme_forum', 'post_name_slug':post_1.slug}))
        request.user = self.usr.user

        response = dislike_link(request, 'meme_forum', post_1.slug)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(post_1.dislikes.count(), 1)

class RegisterTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_normal_page(self):
        """
        This method tests if the corrent response is recived from the register page
        """
        response = self.client.get(reverse('meme_portal:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter your details!')

    def test_register_post_request(self):
        """
        This method tests if a new user is sent to the database when a post
        is sent to the register page
        """
        current_count = UserProfile.objects.all().count()

        response = self.client.post(reverse('meme_portal:register'), data={
            'username': 'bob02',
            'email': 'example.gov@gmail.com',
            'password': 'HEy_pa33w0rd!',
            'picture': '/media/profile_images/bob_02_profile.png',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserProfile.objects.all().count(), current_count + 1)

class LoginTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_normal_page(self):
        """
        This method tests if the corrent response is recived from the login page
        """
        response = self.client.get(reverse('meme_portal:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter your login and password!')

    def test_login_post_request(self):
        """
        This method tests if the user is now logged in when the correct post request
        is sent to the login page
        """
        add_userProfile()
        response = self.client.post(reverse('meme_portal:login'), data={
            'username': 'bob02',
            'password': 'hello',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)

class ShowPostTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_show_posts_page_dosent_exist(self):
        """
        This method will test the output of the show post page when the the post does not exist
        """
        mf = add_forum('meme_forum')
        response = self.client.get(reverse('meme_portal:show_post', kwargs={'forum_name_slug':'meme_forum', 'post_name_slug':'nothign'}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This post does not exist.')

class AccountPageTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = add_userProfile()

    def test_account_page_not_logged_in(self):
        """
        This method will test the output of the accounts page when you are not logged in
        """
        response = self.client.get(reverse('meme_portal:account'))

        # 302 due to the redirection to the login page
        self.assertEqual(response.status_code, 302)

    def test_account_page_logged_in(self):
        """
        This method will test the output of the accounts page when you are not logged in
        """
        request = self.request_factory.get(reverse('meme_portal:account'))
        request.user = self.user.user

        response = user_account(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome Back bob02!')

class MyPostsTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = add_userProfile()

    def test_my_posts_page_logged_in(self):
        """
        This method will test the output of the my posts page when the user is logged in 
        """
        mf = add_forum('meme_forum')

        post_1 = add_post(mf, "post1", "https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", self.user)
        post_2 = add_post(mf, "post2", "http://thewowstyle.com/wp-content/uploads/2015/01/nature-images.jpg", self.user)
        post_3 = add_post(mf, "post3", "https://eskipaper.com/images/images-2.jpg", self.user)

        request = self.request_factory.get(reverse('meme_portal:my_posts'))
        request.user = self.user.user

        response = my_posts(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Posts:')
