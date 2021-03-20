import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gif_and_meme_portal.settings')
django.setup()

from meme_portal.models import Forum, Post, Comment

def populate():

    comments_cat_post_1 = [
        {
            'content': 'Cute cat',
        },
        {
            'content': 'My cat looks just the same',
        },
    ]
    comments_cat_post_3 = [
        {
            'content': 'Not as cute as my cat',
        },
    ]
    comments_cat_post_4 = [
        {
            'content': 'Wow thats a pretty nice photo',
        },
        {
            'content': 'Nice cat',
        },
    ]
    comments_cs_post_1 = [
        {
            'content': 'lol',
        },
    ]
    comments_cs_post_3 = [
        {
            'content': 'Too true',
        },
        {
            'content': 'Laugh cry emoji',
        },
    ]
    comments_cs_post_5 = [
        {
            'content': 'XD',
        },
        {
            'content': 'funny meme',
        },
        {
            'content': 'Another comment',
        },
    ]
    comments_cs_post_6 = [
        {
            'content': 'Hello, world!',
        },
        {
            'content': 'This is yet another comment',
        },
    ]

    cat_posts = [
        {
            'comments': comments_cat_post_1,
            'title': 'Cat photo',
            'url': 'https://images.pexels.com/photos/320014/pexels-photo-320014.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
        },
        {
            'title': 'Another cat photo',
            'url': 'https://images.pexels.com/photos/416160/pexels-photo-416160.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
        },
        {
            'comments': comments_cat_post_3,
            'title': 'Cat photo 3',
            'url': 'https://www.photopoly.net/wp-content/uploads/30042011/1.jpg',
        },
        {
            'comments': comments_cat_post_4,
            'title': 'The last cat photo',
            'url': 'https://www.photopoly.net/wp-content/uploads/30042011/2.jpg',
        },
    ]

    cs_posts = [
        {
            'comments': comments_cs_post_1,
            'title': 'Getting help online',
            'url': 'https://i.imgur.com/QEOYcAD.png',
        },
        {
            'title': 'ML meme',
            'url': 'https://i.imgur.com/FzdARaX.jpeg',
        },
        {
            'comments': comments_cs_post_3,
            'title': 'Thanks',
            'url': 'https://i.redd.it/jx0pxoihk4o61.jpg',
        },
        {
            'title': 'Proud',
            'url': 'https://i.redd.it/yjdg3jztk1o61.jpg',
        },
        {
            'comments': comments_cs_post_5,
            'title': 'Another meme',
            'url': 'https://i.redd.it/tz0pzdj5g2o61.png',
        },
        {
            'comments': comments_cs_post_6,
            'title': 'Cpp meme',
            'url': 'https://i.redd.it/mglh78m6pxj61.jpg',
        },
    ]

    forums = {
        'cat_photos' : {'posts': cat_posts},
        'cs_memes' : {'posts': cs_posts},
    }

    for name, forum_data in forums.items():
        forum = add_forum(name=name)
        for p in forum_data['posts']:
            post = add_post(forum=forum, title=p['title'], url=p['title'])
            if 'comments' in p:
                for c in p['comments']:
                    add_comment(post, c['content']);

    for f in Forum.objects.all():
        for p in Post.objects.filter(forum=f):
            for c in Comment.objects.filter(post=p):
                print(f'-> forum: {f}, post: {p}, comment: {c}')

def add_forum(name):
    f = Forum.objects.get_or_create(name=name)[0]

    return f

def add_post(forum, title, url):
    p = Post.objects.get_or_create(forum=forum, name=title)[0]
    p.url = url

    return p

def add_comment(post, content):
    c = Comment.objects.get_or_create(post=post, content=content)[0]

    return c

if __name__ == '__main__':
    print('Populating database')
    populate()