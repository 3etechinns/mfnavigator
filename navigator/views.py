from django.shortcuts import render
from bakery.views import BuildableDetailView, BuildableListView
from .models import AMC, MutualFund, MutualFundStaticJSON
import os, mfnavigator.settings, abc
import datetime

# Create your views here.
class AMCListView(BuildableListView):
	model = AMC
	template_name = 'navigator/amc_list.html'
	build_path = 'amcs.html'

class LastYearsStaticJSONView(BuildableDetailView,metaclass=abc.ABCMeta):
	model = MutualFund
	template_name = 'navigator/navjson.json'
	n = 0

	def get_url(self, obj):
		return '/%dy-navs/%s.json' % (self.n, obj.amfisymbol)

	def get_build_path(self, obj):
		path = os.path.join(mfnavigator.settings.BUILD_DIR, '%dy-navs' % self.n)
		os.path.exists(path) or os.makedirs(path)
		return os.path.join(path, obj.amfisymbol + '.json')

	def get_context_data(self, **kwargs):
		context = super(LastYearsStaticJSONView, self).get_context_data(**kwargs)
		obj = context['object']
		today = datetime.date.today()
		last_year = today - datetime.timedelta(days=365)
		context['navvals'] = obj.mutualfundnav_set.filter(date__range = (str(last_year), str(today))).order_by('date')
		return context

class Last1YearStaticJSONView(LastYearsStaticJSONView):
	n = 1

class LastYearsViewer(BuildableListView,metaclass=abc.ABCMeta):
	model = MutualFund
	n = 0

	def __init__(self):
		self.template_name = 'navigator/allmf_%dy.html' % self.n
		self.path = os.path.join(mfnavigator.settings.BUILD_DIR, '%dy-navs' % self.n)
		os.path.exists(self.path) or os.makedirs(self.path)
		self.build_path = os.path.join(self.path, 'index.html')

	def get_url(self, obj):
		return '/%dy-navs/' % self.n

	def get_context_data(self, **kwargs):
		context = super(LastYearsViewer, self).get_context_data(**kwargs)
		context['defaultmf'] = '103174'
		return context

class Last1YearViewer(LastYearsViewer):
	n = 1
