import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gif_and_meme_portal.settings')
django.setup()

from meme_portal.models import Forum, Post, Comment

def populate():
    cat_posts = [
        {
            'comments': [
                { 'content': 'Cute cat', },
                { 'content': 'My cat looks just the same', },
            ],
            'title': 'Cat photo',
            'url': 'https://images.pexels.com/photos/320014/pexels-photo-320014.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
            'likes': 99,
        },
        {
            'title': 'Another cat photo',
            'url': 'https://images.pexels.com/photos/416160/pexels-photo-416160.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
            'likes': 260,
        },
        {
            'comments': [
                { 'content': 'Not as cute as my cat', },
            ],
            'title': 'Cat photo 3',
            'url': 'https://www.photopoly.net/wp-content/uploads/30042011/1.jpg',
            'likes': 20,
        },
        {
            'comments': [
                { 'content': 'Wow thats a pretty nice photo', },
                { 'content': 'Nice cat', },
            ],
            'title': 'The last cat photo',
            'url': 'https://www.photopoly.net/wp-content/uploads/30042011/2.jpg',
            'likes': 1,
        },
    ]

    cs_posts = [
        {
            'comments': [
                { 'content': 'lol', },
            ],
            'title': 'Getting help online',
            'url': 'https://i.imgur.com/QEOYcAD.png',
            'likes': 23,
        },
        {
            'title': 'ML meme',
            'url': 'https://i.imgur.com/FzdARaX.jpeg',
            'likes': 456,
        },
        {
            'comments': [
                { 'content': 'Too true', },
                { 'content': 'Laugh cry emoji', },
            ],
            'title': 'Thanks',
            'url': 'https://i.redd.it/jx0pxoihk4o61.jpg',
            'likes': 1258,
        },
        {
            'title': 'Proud',
            'url': 'https://i.redd.it/yjdg3jztk1o61.jpg',
            'likes': 45,
        },
        {
            'comments': [
                { 'content': 'XD', },
                { 'content': 'funny meme', },
                { 'content': 'Another comment', },
            ],
            'title': 'Another meme',
            'url': 'https://i.redd.it/tz0pzdj5g2o61.png',
            'likes': 22,
        },
        {
            'comments': [
                { 'content': 'Hello, world!', },
                { 'content': 'This is yet another comment', },
            ],
            'title': 'Cpp meme',
            'url': 'https://i.redd.it/mglh78m6pxj61.jpg',
            'likes': 2200,
        },
    ]

    forums = {
        'cat_photos' : {'posts': cat_posts},
        'cs_memes' : {'posts': cs_posts},
    }

    for name, forum_data in forums.items():
        forum = add_forum(name=name)
        for p in forum_data['posts']:
            post = add_post(forum=forum, title=p['title'], url=p['title'], likes=p['likes'])
            if 'comments' in p:
                for c in p['comments']:
                    add_comment(post, c['content']);

    for f in Forum.objects.all():
        for p in Post.objects.filter(forum=f):
            for c in Comment.objects.filter(post=p):
                print(f'-> forum: {f}, post: {p}, comment: {c}')

def add_forum(name):
    f = Forum.objects.get_or_create(name=name)[0]

    f.save();

    return f

def add_post(forum, title, url, likes):
    p = Post.objects.get_or_create(forum=forum, name=title)[0]
    p.url = url
    p.likes = likes

    p.save();

    return p

def add_comment(post, content):
    c = Comment.objects.get_or_create(post=post, content=content)[0]

    c.save();

    return c

if __name__ == '__main__':
    print('Populating database')
    populate()
