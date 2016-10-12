from django.test import TestCase
from app.models import FlowTable
import sitetest3.settings

# Create your tests here.
testmodel = FlowTable.objects.filter(cate='DCN')
for each in testmodel:
    print(each.flow_data)