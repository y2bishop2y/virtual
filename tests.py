#!flask/bin/python
# -*- coding: utf8 -*-

import os
import unittest

from config import basedir
from app import app, db
from datetime import datetime, timedelta
from app.models import User, Post
from app.translate import microsoft_translate
from coverage import coverage 

# cov = coverage(branch = True, omit = ['flask/*', 'tests.py'], timid = True)
# cov.start()

class TestAvatar(unittest.TestCase):


	def setUp(self):

		app.config['TESTING'] = True
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

		self.app = app.test_client()
		db.create_all()


	def tearDown(self):
		db.session.remove()
		db.drop_all()


	def test_avatar(self):

		u = User(nickname = 'emiliano', email = 'emiliano@medlista.com')

		avatar = u.avatar(128)
		expected = 'http://www.gravatar.com/avatar/c74976822d1615784f4a2595510d2a2b'

		assert avatar[0:len(expected)] == expected


class TestNickName(unittest.TestCase):

	def setUp(self):

		app.config['TESTING'] = True
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

		self.app = app.test_client()
		db.create_all()


	def tearDown(self):
		db.session.remove()
		db.drop_all()


	def test_make_unique_nickname(self):
		u = User(nickname = 'john', email = 'john@example.com')

		db.session.add(u)
		db.session.commit()

		nickname = User.make_unique_nickname('john')
		assert nickname != 'john'

		u = User(nickname = nickname, email = 'susan@example.com')

		db.session.add(u)
		db.session.commit()

		nickname2 = User.make_unique_nickname('john')

		assert nickname2 != 'john'
		assert nickname2 != nickname


class TestFollow(unittest.TestCase):

	def setUp(self):

		app.config['TESTING'] = True
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

		self.app = app.test_client()
		db.create_all()


	def tearDown(self):
		db.session.remove()
		db.drop_all()



	def test_follow(self):
		u1 = User(nickname = 'john',  email = 'john@example.com')
		u2 = User(nickname = 'susan', email = 'susan@example.com')

		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()

		assert u1.unfollow(u2) == None
		u = u1.follow(u2)

		db.session.add(u)
		db.session.commit()

		assert u1.follow(u2) == None
		assert u1.is_following(u2)
		assert u1.followed.count() == 1
		assert u1.followed.first().nickname == 'susan'
		
		assert u2.followers.count() == 1
		assert u2.followers.first().nickname == 'john'
		u = u1.unfollow(u2)

		assert u != None
		db.session.add(u)
		db.session.commit()

		assert u1.is_following(u2) == False
		assert u1.followed.count() == 0
		assert u2.followers.count() == 0
		assert u1.followers


	def test_follow_posts(self):

		# make for users
		u1 = User(nickname = 'john', email = 'john@example.com')
		u2 = User(nickname = 'susan', email = 'susan@example.com')
		u3 = User(nickname = 'mary', email = 'mary@example.com')
		u4 = User(nickname = 'david', email = 'david@example.com')

		db.session.add(u1)
		db.session.add(u2)
		db.session.add(u3)
		db.session.add(u4)

		# make four posts
		utcnow = datetime.utcnow()
		p1 = Post(body = 'post from john',  author = u1, timestamp = utcnow + timedelta(seconds = 1))
		p2 = Post(body = 'post from susan', author = u2, timestamp = utcnow + timedelta(seconds = 2))
		p3 = Post(body = 'post from mary',  author = u3, timestamp = utcnow + timedelta(seconds = 3))
		p4 = Post(body = 'post from david', author = u4, timestamp = utcnow + timedelta(seconds = 4))

		db.session.add(p1)
		db.session.add(p2)
		db.session.add(p3)
		db.session.add(p4)
		db.session.commit()

		# setup the followers
		u1.follow(u1)
		u1.follow(u2)
		u1.follow(u4)
		u2.follow(u2)
		u2.follow(u3)
		u3.follow(u3)
		u3.follow(u4)
		u4.follow(u4)

		db.session.add(u1)
		db.session.add(u2)
		db.session.add(u3)
		db.session.add(u4)
		db.session.commit()

		# check the follow posts of each user
		f1 = u1.followed_posts().all()
		f2 = u2.followed_posts().all()
		f3 = u3.followed_posts().all()
		f4 = u4.followed_posts().all()

		print "THIS IS THE LENGTH: %d" % len(f1)
		assert len(f1) == 3
		assert len(f2) == 2
		assert len(f3) == 2
		assert len(f4) == 1

		assert f1 == [p4, p2, p1]
		assert f2 == [p3, p2]
		assert f3 == [p4, p3]
		assert f4 == [p4]




class TestTranslate(unittest.TestCase):

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


	def test_translation(self):

		assert microsoft_translate(u'English', 'en', 'es') == u'Inglés'
        assert microsoft_translate(u'Español', 'es', 'en') == u'Spanish'


class TestDeletePost(unittest.TestCase):
	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_delete_post(self):
		# create a user and a post
		u = User(nickname = 'john', email = 'john@example.com')
		p = Post(body = 'test post', author = u, timestamp = datetime.utcnow())

		db.session.add(u)
		db.session.add(p)
		db.session.commit()

		# Query the post and destroy the session
		p = Post.query.get(1)

		db.session.remove()

		# Delete the post using a new session
		db.session = db.create_scoped_session()
		db.session.delete(p)
		db.session.commit()


class TestUser(unittest.TestCase):
	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


	def test_user(self):
		# make valid nicknames 
		n = User.make_valid_nickname('John_123')

		assert n == 'John_123'

		n = User.make_valid_nickname('John_[123]\n')
		assert n == 'John_123'

		# create a User
		u = User(nickname = 'john', email = 'john@example.com')
		db.session.add(u)
		db.session.commit()

		assert u.is_authenticated() == True
		assert u.is_active() == True
		assert u.is_anonymous() == False
		assert u.id == int(u.get_id())


	def test_make_unique_nickname(self):

		# create a user and write it to the database 
		u = User(nickname = 'john', email = 'john@example.com')

		db.session.add(u)
		db.session.commit()

		nickname = User.make_unique_nickname('susan')
		assert nickname == 'susan'

		nickname = User.make_unique_nickname('john')
		assert nickname != 'john'





if __name__ == '__main__':


	try:
		suite1 = unittest.TestLoader().loadTestsFromTestCase(TestAvatar)
		suite2 = unittest.TestLoader().loadTestsFromTestCase(TestNickName)
		suite3 = unittest.TestLoader().loadTestsFromTestCase(TestTranslate)
		suite4 = unittest.TestLoader().loadTestsFromTestCase(TestFollow)
		suite5 = unittest.TestLoader().loadTestsFromTestCase(TestDeletePost)
		suite6 = unittest.TestLoader().loadTestsFromTestCase(TestUser)

		suite = unittest.TestSuite([suite1, suite2, suite3, suite4, suite5, suite6])
		# suite = unittest.TestSuite([suite1])
		unittest.TextTestRunner(verbosity = 2).run(suite)

		# unittest.main()
	except:
		print "HERE ???"
		pass


	# cov.stop()
	# cov.save()

	# print "\n\nCoverage Report:\n"
	# cov.report()

	# print "HTML version: " + os.path.join(basedir, "tmp/coverage/index.hml")
	# cov.html_report(directory = "tmp/coverage")
	# cov.erase()






