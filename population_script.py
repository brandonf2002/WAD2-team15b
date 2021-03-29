import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gif_and_meme_portal.settings')
django.setup()

from meme_portal.models import Forum, Post, Comment, UserProfile
from django.contrib.auth.models import User

def populate():
    users = [
        {'username': 'bob02', 'password': 'hello'},
        {'username': 'user10', 'password': 'world'},
        {'username': 'number_1_fan', 'password': 'WOW'},
        {'username': 'IAMAUSER', 'password': 'BBBBBBBBBBBBBBBBBBBB01'},
    ]

    cat_posts = [
        {
            'comments': [
                { 'content': 'Cute cat', 'author': 'bob02',},
                { 'content': 'My cat looks just the same', 'author': 'user10',},
            ],
            'title': 'Cat photo',
            'url': 'https://images.pexels.com/photos/320014/pexels-photo-320014.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
            'likes': 99,
            'author': 'bob02'
        },
        {
            'title': 'Another cat photo',
            'url': 'https://images.pexels.com/photos/416160/pexels-photo-416160.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
            'likes': 260,
            'author': 'user10'
        },
        {
            'comments': [
                { 'content': 'Not as cute as my cat', 'author': 'bob02',},
            ],
            'title': 'Cat photo 3',
            'url': 'https://www.photopoly.net/wp-content/uploads/30042011/1.jpg',
            'likes': 20,
            'author': 'IAMAUSER'
        },
        {
            'comments': [
                { 'content': 'Wow thats a pretty nice photo', 'author': 'user10',},
                { 'content': 'Nice cat', 'author': 'bob02',},
            ],
            'title': 'The last cat photo',
            'url': 'https://www.photopoly.net/wp-content/uploads/30042011/2.jpg',
            'likes': 1,
            'author': 'IAMAUSER'
        },
    ]

    cs_posts = [
        {
            'comments': [
                { 'content': 'lol', 'author': 'IAMAUSER',},
            ],
            'title': 'Getting help online',
            'url': 'https://i.imgur.com/QEOYcAD.png',
            'likes': 23,
            'author': 'bob02'
        },
        {
            'title': 'ML meme',
            'url': 'https://i.imgur.com/FzdARaX.jpeg',
            'likes': 456,
            'author': 'IAMAUSER'
        },
        {
            'comments': [
                { 'content': 'Too true', 'author': 'IAMAUSER',},
                { 'content': 'Laugh cry emoji', 'author': 'bob02',},
            ],
            'title': 'Thanks',
            'url': 'https://i.redd.it/jx0pxoihk4o61.jpg',
            'likes': 1258,
            'author': 'user10'
        },
        {
            'title': 'Proud',
            'url': 'https://i.redd.it/yjdg3jztk1o61.jpg',
            'likes': 45,
            'author': 'number_1_fan'
        },
        {
            'comments': [
                { 'content': 'XD', 'author': 'number_1_fan',},
                { 'content': 'funny meme', 'author': 'IAMAUSER',},
                { 'content': 'Another comment', 'author': 'bob02',},
            ],
            'title': 'Another meme',
            'url': 'https://i.redd.it/tz0pzdj5g2o61.png',
            'likes': 22,
            'author': 'bob02'
        },
        {
            'comments': [
                { 'content': 'Hello, world!', 'author': 'bob02',},
                { 'content': 'This is yet another comment', 'author': 'bob02',},
            ],
            'title': 'Cpp meme',
            'url': 'https://i.redd.it/mglh78m6pxj61.jpg',
            'likes': 2200,
            'author': 'number_1_fan'
        },
    ]

    forums = {
        'cat_photos' : {'posts': cat_posts},
        'cs_memes' : {'posts': cs_posts},
    }

    for profile in users:
        add_user_profile(name=profile['username'], psswrd=profile['password'])

    for name, forum_data in forums.items():
        forum = add_forum(name=name)
        for p in forum_data['posts']:
            post = add_post(forum=forum, title=p['title'], url=p['url'], likes=p['likes'], author=p['author'])
            if 'comments' in p:
                for c in p['comments']:
                    add_comment(post, c['content'], c['author']);

    for f in Forum.objects.all():
        for p in Post.objects.filter(forum=f):
            for c in Comment.objects.filter(post=p):
                print(f'-> forum: {f}, post: {p}, comment: {c}')

def add_user_profile(name, psswrd):
    try:
        u = User.objects.create_user(name, password=psswrd)
    except django.db.utils.IntegrityError:
        u = User.objects.get(username=name)

    u.save()
     
    up = UserProfile.objects.get_or_create(user=u)[0]
    up.save()

    return up

def add_forum(name):
    f = Forum.objects.get_or_create(name=name)[0]

    f.save();

    return f

def add_post(forum, title, url, likes, author):
    p = Post.objects.get_or_create(forum=forum, name=title, author=UserProfile.objects.get(user=(User.objects.get(username=author))))[0]
    p.img_url = url
    p.likes = likes

    p.save();

    return p

def add_comment(post, content, author):
    c = Comment.objects.get_or_create(post=post, content=content, author=UserProfile.objects.get(user=(User.objects.get(username=author))))[0]

    c.save();

    return c

if __name__ == '__main__':
    print('Populating database')
    populate()
