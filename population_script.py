import os
import django
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gif_and_meme_portal.settings')
django.setup()

from meme_portal.models import Forum, Post, Comment, UserProfile
from django.contrib.auth.models import User
from django.core.files import File
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def populate():
    users = [
        {
            'username': 'bob02', 
            'password': 'hello', 
            'profile_pic': '/media/profile_images/bob_02_profile.png'
        },
        {
            'username': 'user10',
            'password': 'world', 
            'profile_pic': '/media/profile_images/user10_profile_pic.png'
        },
        {
            'username': 'number_1_fan', 
            'password': 'WOW',
            'profile_pic': '/media/profile_images/number_1_fan.jpg'
        },
        {
            'username': 'IAMAUSER', 
            'password': 'BBBBBBBBBBBBBBBBBBBB01',
            'profile_pic': '/media/profile_images/IAMUSER_profile.jpg'
        },
        {
            'username': 'I-love-cats', 
            'password': 'Ih8Dogs', 
            'profile_pic': '/media/profile_images/I-lvoe_cats_profile.jpg'
        },
        {
            'username': 'maxwelld90', 
            'password': 'tangoWithDjango', 
            'profile_pic': '/media/profile_images/rango.jpg'
        },
        {
            'username': 'djagoRocks', 
            'password': 'I_meanThe_M0V1E',
            'profile_pic': '/media/profile_images/djangoRocks.jpg'
        },
        {
            'username': 'imreallyrunningoutofusernames', 
            'password': 'hopethatwasnttoolong123', 
            'profile_pic': '/media/profile_images/imreally_profile.jpg'
        },
        {
            'username': 'WowzersAnotherUsername', 
            'password': 'HopefullyThisislast', 
            'profile_pic': '/media/profile_images/Wowzers_profile.jpg'
        },
    ]

    cat_posts = [
        {
            'comments': [
                { 'content': 'Cute cat', 'author': 'bob02',},
                { 'content': 'My cat looks just the same', 'author': 'user10',},
            ],
            'title': 'Cat photo',
            'url': 'https://images.pexels.com/photos/320014/pexels-photo-320014.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
            'author': 'bob02',
            'likes' : ['user10', 'number_1_fan'],
            'dislikes': ['IAMAUSER'],
        },
        {
            'title': 'Another cat photo',
            'url': 'https://images.pexels.com/photos/416160/pexels-photo-416160.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
            'author': 'user10',
            'likes' : ['user10', 'IAMAUSER'],
            'dislikes': ['bob02'],
        },
        {
            'comments': [
                { 'content': 'Not as cute as my cat', 'author': 'bob02',},
            ],
            'title': 'Cat photo 3',
            'url': 'https://www.photopoly.net/wp-content/uploads/30042011/1.jpg',
            'author': 'IAMAUSER',
            'likes' : [],
            'dislikes': ['bob02', 'IAMAUSER', 'number_1_fan'],
        },
        {
            'comments': [
                { 'content': 'Wow thats a pretty nice photo', 'author': 'user10',},
                { 'content': 'Nice cat', 'author': 'bob02',},
            ],
            'title': 'The last cat photo',
            'url': 'https://www.photopoly.net/wp-content/uploads/30042011/2.jpg',
            'author': 'IAMAUSER',
            'likes' : ['bob02', 'user10'],
            'dislikes': ['WowzersAnotherUsername', 'imreallyrunningoutofusernames'],
        },
    ]

    cs_posts = [
        {
            'comments': [
                { 'content': 'lol', 'author': 'IAMAUSER',},
            ],
            'title': 'Getting help online',
            'url': 'https://i.imgur.com/QEOYcAD.png',
            'author': 'bob02',
            'likes' : ['I-love-cats', 'djagoRocks', 'imreallyrunningoutofusernames'],
            'dislikes': ['IAMAUSER'],
        },
        {
            'title': 'ML meme',
            'url': 'https://i.imgur.com/FzdARaX.jpeg',
            'author': 'IAMAUSER',
            'likes' : [],
            'dislikes': ['bob02', 'IAMAUSER', 'WowzersAnotherUsername', 'imreallyrunningoutofusernames'],
        },
        {
            'comments': [
                { 'content': 'Too true', 'author': 'IAMAUSER',},
                { 'content': 'Laugh cry emoji', 'author': 'bob02',},
            ],
            'title': 'Thanks',
            'url': 'https://i.redd.it/jx0pxoihk4o61.jpg',
            'author': 'user10',
            'likes' : ['bob02', 'IAMAUSER', 'WowzersAnotherUsername', 'imreallyrunningoutofusernames'],
            'dislikes': [],
        },
        {
            'title': 'Proud',
            'url': 'https://i.redd.it/yjdg3jztk1o61.jpg',
            'author': 'number_1_fan',
            'likes' : ['user10', 'djagoRocks'],
            'dislikes': ['I-love-cats', 'number_1_fan'],
        },
        {
            'comments': [
                { 'content': 'XD', 'author': 'number_1_fan',},
                { 'content': 'funny meme', 'author': 'IAMAUSER',},
                { 'content': 'Another comment', 'author': 'bob02',},
            ],
            'title': 'Another meme',
            'url': 'https://i.redd.it/tz0pzdj5g2o61.png',
            'author': 'bob02',
            'likes' : ['WowzersAnotherUsername', 'imreallyrunningoutofusernames', 'bob02'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'Hello, world!', 'author': 'bob02',},
                { 'content': 'This is yet another comment', 'author': 'bob02',},
            ],
            'title': 'Cpp meme',
            'url': 'https://i.redd.it/mglh78m6pxj61.jpg',
            'author': 'number_1_fan',
            'likes' : [],
            'dislikes': ['bob02', 'IAMAUSER', 'WowzersAnotherUsername', 'imreallyrunningoutofusernames', 'user10', 'I-love-cats', 'djagoRocks', 'number_1_fan'],
        },
    ]

    tango_posts = [
        {
            'comments': [
                { 'content': 'Tango with dajngo!', 'author': 'maxwelld90',},
            ],
            'title': 'Luxury Tango',
            'url': 'http://theluxtraveller.com/wp-content/uploads/2014/05/Tango.jpg',
            'author': 'WowzersAnotherUsername',
            'likes' : ['WowzersAnotherUsername', 'bob02'],
            'dislikes': ['number_1_fan'],
        },
        {
            'comments': [
                { 'content': 'Tango with dajngo!', 'author': 'maxwelld90',},
            ],
            'title': 'Arentine Tango',
            'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Tango_Porte%C3%B1o.jpg/1200px-Tango_Porte%C3%B1o.jpg',
            'author': 'imreallyrunningoutofusernames',
            'likes' : [ 'imreallyrunningoutofusernames', 'djagoRocks', 'I-love-cats', 'IAMAUSER'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'Tango with dajngo!', 'author': 'maxwelld90',},
                { 'content': 'Wrong tango bro', 'author': 'WowzersAnotherUsername',},
                { 'content': 'Why am i doing this', 'author': 'djagoRocks',},
            ],
            'title': 'Wow, I sure do with tango',
            'url': 'https://upload.wikimedia.org/wikipedia/en/2/21/Tango_drink.JPG',
            'author': 'number_1_fan',
            'likes' : ['number_1_fan'],
            'dislikes': ['I-love-cats', 'imreallyrunningoutofusernames', 'djagoRocks', 'WowzersAnotherUsername', 'IAMAUSER'],
        },
        {
            'title': 'Tango with Django',
            'url': 'https://image.slidesharecdn.com/howtotangowithdjango-160521005047/95/how-to-tangowithdjango-1-638.jpg?cb=1463792125',
            'author': 'maxwelld90',
            'likes' : [],
            'dislikes': ['I-love-cats', 'imreallyrunningoutofusernames', 'djagoRocks', 'WowzersAnotherUsername', 'IAMAUSER', 'maxwelld90', 'bob02', 'number_1_fan', 'user10'],
        },
    ]

    rango_posts = [
        {
            'title': 'Mr Rango',
            'url': 'http://3.bp.blogspot.com/-CkkZKaxqeEs/T6PrVxUQBvI/AAAAAAAABQw/TOvifoXGkG0/s1600/Rango-035.jpg',
            'author': 'bob02',
            'likes' : ['imreallyrunningoutofusernames', 'djagoRocks', 'WowzersAnotherUsername'],
            'dislikes': ['I-love-cats'],
        },
        {
            'title': 'Tango with Django',
            'url': 'https://image.slidesharecdn.com/howtotangowithdjango-160521005047/95/how-to-tangowithdjango-1-638.jpg?cb=1463792125',
            'author': 'maxwelld90',
            'likes' : ['I-love-cats', 'user10'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'This is a comment about rango', 'author': 'djagoRocks',},
            ],
            'title': 'Rungo',
            'url': 'https://images2.imgbox.com/21/45/ZHWmLk4A_o.png',
            'author': 'user10',
            'likes' : ['IAMAUSER', 'WowzersAnotherUsername'],
            'dislikes': ['number_1_fan'],
        },
        {
            'comments': [
                { 'content': 'Rango meme\'s, love it', 'author': 'djagoRocks',},
                { 'content': 'This is another comment about rango', 'author': 'user10',},
            ],
            'title': 'I\'m sorry bro',
            'url': 'https://i.redd.it/ipa7d916fpl61.jpg',
            'author': 'bob02',
            'likes' : ['imreallyrunningoutofusernames', 'djagoRocks', 'WowzersAnotherUsername'],
            'dislikes': ['I-love-cats'],
        },
        {
            'comments': [
                { 'content': 'This isn\'t even funny bro', 'author': 'number_1_fan',},
            ],
            'title': 'I don\'t even know anymore',
            'url': 'https://i.redd.it/9wtdlclym0l61.jpg',
            'author': 'IAMAUSER',
            'likes' : ['imreallyrunningoutofusernames', 'bob02'],
            'dislikes': ['I-love-cats', 'djagoRocks', 'WowzersAnotherUsername', 'IAMAUSER', 'maxwelld90', 'number_1_fan', 'user10'],
        },
        {
            'title': 'pls send help',
            'url': 'https://i.redd.it/ee8pl0ak11431.jpg',
            'author': 'IAMAUSER',
            'likes' : ['imreallyrunningoutofusernames', 'bob02', 'I-love-cats'],
            'dislikes': [],
        },
        {
            'title': 'don\'t tango with the rango',
            'url': 'https://i.redd.it/g9h7lz8ok0r21.jpg',
            'author': 'I-love-cats',
            'likes' : ['number_1_fan', 'I-love-cats', 'imreallyrunningoutofusernames', 'WowzersAnotherUsername'],
            'dislikes': ['maxwelld90'],
        },
    ]
    django_posts = [
        {
            'title': 'Tango with Django',
            'url': 'https://image.slidesharecdn.com/howtotangowithdjango-160521005047/95/how-to-tangowithdjango-1-638.jpg?cb=1463792125',
            'author': 'maxwelld90',
            'likes' : ['I-love-cats', 'imreallyrunningoutofusernames', 'djagoRocks', 'WowzersAnotherUsername', 'IAMAUSER', 'maxwelld90', 'bob02', 'number_1_fan', 'user10'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'lol not even on npm, disgraceful', 'author': 'number_1_fan',},
                { 'content': 'Thought this was about the movie lol', 'author': 'bob02',},
            ],
            'title': 'STOP USING DJANGO',
            'url': 'https://i.redd.it/ob3luy1wufl61.png',
            'author': 'bob02',
            'likes' : ['maxwelld90', 'WowzersAnotherUsername', 'djagoRocks'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'Gotta be the first time ive ever heard of makemessages', 'author': 'user10',},
            ],
            'title': 'Tab compelation be like',
            'url': 'https://i.imgur.com/sro6l4J.jpg',
            'author': 'number_1_fan',
            'likes' : [ 'imreallyrunningoutofusernames', 'djagoRocks', 'I-love-cats', 'IAMAUSER'],
            'dislikes': ['number_1_fan'],
        },
        {
            'title': 'Django pillow',
            'url': 'https://i.redd.it/4nu68s7qbps51.jpg',
            'author': 'I-love-cats',
            'likes' : [],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'How have I also ran out of comments to write', 'author': 'bob02',},
                { 'content': 'I wonder if anyone will ever read this', 'author': 'IAMAUSER',},
            ],
            'title': 'Ran out of memes about django',
            'url': 'https://i.redd.it/utis11ygw9x41.jpg',
            'author': 'IAMAUSER',
            'likes' : ['WowzersAnotherUsername'],
            'dislikes': [ 'imreallyrunningoutofusernames', 'djagoRocks', 'I-love-cats', 'IAMAUSER'],
        },
    ]

    mathmemes_posts = [
        {
            'title': 'If Rick Astley taught Geometry class:',
            'url': 'https://i.redd.it/f4b4pme1m2r61.jpg',
            'author': 'bob02',
            'likes' : [ 'bob02', 'imreallyrunningoutofusernames'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'Yea me too bro, melts the mind', 'author': 'maxwelld90',},
                { 'content': 'Na I\'ve gotta say i quite enjoy that fact', 'author': 'IAMAUSER',},
            ],
            'title': 'Complex numbers hurt my head',
            'url': 'https://i.redd.it/pzgi0i6uq4r61.png',
            'author': 'maxwelld90',
            'likes' : ['imreallyrunningoutofusernames', 'number_1_fan', 'user10', 'I-love-cats'],
            'dislikes': ['maxwelld90'],
        },
        {
            'comments': [
                { 'content': 'Aha, the man himself', 'author': 'IAMAUSER',},
            ],
            'title': 'Pythagoras',
            'url': 'https://i.redd.it/o97jg87laqq61.jpg',
            'author': 'bob02',
            'likes' : [],
            'dislikes': [ 'bob02', 'WowzersAnotherUsername'],
        },
        {
            'title': 'Determinant Expansion by Minors to be specific.',
            'url': 'https://i.redd.it/puyw310pmhq61.jpg',
            'author': 'imreallyrunningoutofusernames',
            'likes' : [ 'bob02', 'djagoRocks', 'user10'],
            'dislikes': [],
        },
        {
            'title': 'topologists too',
            'url': 'https://i.redd.it/z7xva0ffzlq61.jpg',
            'author': 'IAMAUSER',
            'likes' : [ 'bob02', 'maxwelld90'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'If only we could take it all back', 'author': 'imreallyrunningoutofusernames',},
                { 'content': 'Dam, if only I had taken Computing Science\n\nIf only', 'author': 'bob02',},
            ],
            'title': 'Maybe this math degree is a mistake.',
            'url': 'https://i.redd.it/foyclbisb4q61.jpg',
            'author': 'maxwelld90',
            'likes' : ['maxwelld90', 'imreallyrunningoutofusernames'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'I can\'t even remember what this post was about but heres a comment anyone', 'author': 'number_1_fan',},
            ],
            'title': 'Gosh darn it',
            'url': 'https://i.redd.it/y97jojwb6yp61.jpg',
            'author': 'IAMAUSER',
            'likes' : [ 'bob02', 'IAMAUSER'],
            'dislikes': [],
        },
        {
            'title': 'LaTeX <3',
            'url': 'https://i.redd.it/168fl22rktq61.jpg',
            'author': 'imreallyrunningoutofusernames',
            'likes' : [],
            'dislikes': ['IAMAUSER', 'bob02', 'imreallyrunningoutofusernames', 'WowzersAnotherUsername' ],
        },
        {
            'title': 'Because why not',
            'url': 'https://i.redd.it/nj9qosl4nqq61.jpg',
            'author': 'user10',
            'likes' : [ 'bob02'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'Aha I quite liked this one, pretty good man', 'author': 'bob02',},
                { 'content': 'Ooh thats pretty good actually', 'author': 'IAMAUSER',},
                { 'content': 'Lol', 'author': 'user10',},
            ],
            'title': 'Topologist\'s Morning routine',
            'url': 'https://i.redd.it/3nqccqefgrp61.jpg',
            'author': 'user10',
            'likes' : ['user10',  'bob02', 'maxwelld90'],
            'dislikes': [],
        },
    ]

    history_memes_posts = [
        {
            'comments': [
                { 'content': 'Heres a sample comment', 'author': 'WowzersAnotherUsername',},
            ],
            'title': 'I still don\'t get the connection',
            'url': 'https://i.redd.it/ey6tmutb14r61.jpg',
            'author': 'IAMAUSER',
            'likes' : [ 'imreallyrunningoutofusernames', 'djagoRocks', 'I-love-cats', 'IAMAUSER'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'I don\'t think it does man, you should make a new forum for these sorts of posts', 'author': 'bob02',},
                { 'content': 'This is another comment on the history_memes forum', 'author': 'number_1_fan',},
            ],
            'title': 'I thought this suits the theme!',
            'url': 'https://i.redd.it/2hmf09tjw2r61.jpg',
            'author': 'imreallyrunningoutofusernames',
            'likes' : [],
            'dislikes': [ 'bob02', 'IAMAUSER'],
        },
        {
            'title': 'Colorado what\'s your deal',
            'url': 'https://i.redd.it/iw5sdu4yg1r61.png',
            'author': 'I-love-cats',
            'likes' : [],
            'dislikes': ['IAMAUSER', 'bob02', 'imreallyrunningoutofusernames', 'WowzersAnotherUsername' ],
        },
        {
            'comments': [
                { 'content': 'onokyo, not again', 'author': 'bob02',},
                { 'content': 'This is pretty good', 'author': 'imreallyrunningoutofusernames',},
            ],
            'title': 'Japan\'s capital be like:',
            'url': 'https://i.redd.it/1km1lbl00nn61.jpg',
            'author': 'WowzersAnotherUsername',
            'likes' : ['IAMAUSER', 'bob02', 'imreallyrunningoutofusernames', 'WowzersAnotherUsername' ],
            'dislikes': [],
        },
        {
            'title': '*cough* emus *cough*',
            'url': 'https://i.redd.it/k3x9vi09bdo61.jpg',
            'author': 'maxwelld90',
            'likes' : ['maxwelld90', 'imreallyrunningoutofusernames'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'This is another comment on a post', 'author': 'IAMAUSER',},
                { 'content': 'Wow, heres another one\n\nBy another user that is', 'author': 'WowzersAnotherUsername',},
            ],
            'title': 'Great success!',
            'url': 'https://i.redd.it/rsd3cyh5jtq61.jpg',
            'author': 'IAMAUSER',
            'likes' : [],
            'dislikes': [],
        },
        {
            'title': 'Let us never forget those who fought against Sauron occupation.',
            'url': 'https://i.redd.it/d2lkw8fwtkq61.jpg',
            'author': 'IAMAUSER',
            'likes' : ['imreallyrunningoutofusernames', 'number_1_fan', 'user10', 'I-love-cats'],
            'dislikes': [],
        },
        {
            'comments': [
                { 'content': 'I can\'t even remember what this post was about but heres a comment anyone', 'author': 'number_1_fan',},
            ],
            'title': 'They had their own f\'ing army',
            'url': 'https://i.redd.it/b7sk1t90mfl61.jpg',
            'author': 'I-love-cats',
            'likes' : [],
            'dislikes': [],
        },
    ]

    forums = {
        'cat_photos' : {'posts': cat_posts},
        'cs_memes' : {'posts': cs_posts},
        'tango' : {'posts': tango_posts},
        'rango' : {'posts': rango_posts},
        'django' : {'posts': django_posts},
        'mathmemes' : {'posts': mathmemes_posts},
        'history_memes' : {'posts': history_memes_posts},
    }

    for profile in users:
        add_user_profile(name=profile['username'], psswrd=profile['password'], pic=profile['profile_pic'])

    for name, forum_data in forums.items():
        forum = add_forum(name=name)
        for p in forum_data['posts']:
            post = add_post(forum=forum, title=p['title'], url=p['url'], author=p['author'], likes=p['likes'], dislikes=p['dislikes'])
            if 'comments' in p:
                for c in p['comments']:
                    add_comment(post, c['content'], c['author']);

    for f in Forum.objects.all():
        for p in Post.objects.filter(forum=f):
            for c in Comment.objects.filter(post=p):
                print(f'-> forum: {f}, post: {p}, comment: {c}')

def add_user_profile(name, psswrd, pic):
    try:
        u = User.objects.create_user(name, password=psswrd)
    except django.db.utils.IntegrityError:
        u = User.objects.get(username=name)

    u.save()
     
    up = UserProfile.objects.get_or_create(user=u)[0]
    with open(BASE_DIR + pic, 'rb') as f:
        data = f.read()

    up.picture.save(f'{name}_porfile_pic', ContentFile(data))
    up.save()

    return up

def add_forum(name):
    f = Forum.objects.get_or_create(name=name)[0]

    f.save();

    return f

def add_post(forum, title, url, author, likes, dislikes):
    p = Post.objects.get_or_create(forum=forum, name=title, author=UserProfile.objects.get(user=(User.objects.get(username=author))))[0]
    p.img_url = url

    for name in likes:
        p.likes.add(UserProfile.objects.get(user=(User.objects.get(username=name))))
    for name in dislikes:
        p.dislikes.add(UserProfile.objects.get(user=(User.objects.get(username=name))))

    p.save();

    return p

def add_comment(post, content, author):
    c = Comment.objects.get_or_create(post=post, content=content, author=UserProfile.objects.get(user=(User.objects.get(username=author))))[0]

    c.save();

    return c

if __name__ == '__main__':
    print('Populating database')
    populate()
