# The tests will then be run, and the output displayed -- do you pass them all?
# 
# Once you are done with the tests, delete the module. You don't need to put it in your Git repository!
#

import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class ProjectStructureTests(TestCase):
	"""
    Simple tests to probe the file structure of your project so far.
    We also include a test to check whether you have added meme_portal to your list of INSTALLED_APPS.
    """
	def setUp(self):
		self.project_base_dir = os.getcwd()
		self.rango_app_dir = os.path.join(self.project_base_dir, 'meme_portal')
    

class IndexPageTests(TestCase):


	def setUp(self):
		self.views_module = importlib.import_module('meme_portal.views')
		self.views_module_listing = dir(self.views_module)
        
		self.project_urls_module = importlib.import_module('tango_with_django_project.urls')
		
	def test_view_exists(self):
		"""
        Does the index() view exist in meme_portals views.py module?
        """
		name_exists = 'index' in self.views_module_listing
		is_callable = callable(self.views_module.index)
        
		self.assertTrue(name_exists, f"{FAILURE_HEADER}The index() view for meme_portal does not exist.{FAILURE_FOOTER}")
		self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the index() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")