
from django.shortcuts import render,render_to_response
from app.models import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import pymysql
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required




@login_required
def index(request):
    date_str = str(request.POST.get('filter1'))
    number_perpage = str(request.POST.get('filter2'))
    datedrop_list = FlowTable.objects.values('last_date').distinct()
    if number_perpage=='None' or number_perpage=='' or number_perpage=='每页数据条数':
        limit=30
        number_perpage='每页数据条数'
    else:
        limit = int(number_perpage)
    if date_str=='None' or date_str=='' or date_str=='日期选择':
        paginator = Paginator(FlowTable.objects.all(), limit)
        date_str = '日期选择'
    else:
        paginator = Paginator(FlowTable.objects.all().filter(last_date=date_str),limit)
    page = request.GET.get('page',1)
    loaded = paginator.page(page)
    context = {
        'fb':loaded,
        'datedrop_list':datedrop_list,
        'date_str':date_str,
        'number_perpage':number_perpage
    }
    return render(request, 'index.html', context)

@login_required
def chart(request):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='flows3', charset='UTF8')
    cur_cate = conn.cursor()
    cur_date = conn.cursor()
    cur_city = conn.cursor()
    cur_city_bandwidth= conn.cursor()
    cur_city_peak= conn.cursor()
    cur_city_busyavg=conn.cursor()
    cur_city_avg=conn.cursor()

    cur_flow = conn.cursor()
    cur_peak = conn.cursor()
    cur_busyavg=conn.cursor()
    cur_avg=conn.cursor()

    cate_str = str(request.POST.get('filter1'))
    city_str = str(request.POST.get('filter2'))
    date_str = str(request.POST.get('filter3'))

    count_exist=1
    if city_str=='None' or city_str=='':
        str_sql_city=''
    else:
        if count_exist==1:
            str_sql_city=" where city='"+city_str+"'"
        else:
            str_sql_city=" and city='"+city_str+"'"
        count_exist+=1

    if cate_str=='None' or cate_str=='':
        str_sql_cate=''
    else:
        if count_exist==1:
            str_sql_cate=" where cate='"+cate_str+"'"
        else:
            str_sql_cate=" and cate='"+cate_str+"'"
        count_exist+=1

    if date_str=='None' or date_str=='':
        str_sql_date=''
    else:
        if count_exist==1:
            str_sql_date=" where last_date='"+date_str+"'"
        else:
            str_sql_date=" and last_date='"+date_str+"'"
        count_exist+=1
    sql_add=str(str_sql_city+str_sql_cate+str_sql_date)

    cur_cate.execute("select cate,sum(flow_data) from app_flowtable"+sql_add+" GROUP by cate  order by sum(flow_data) desc")
    cur_date.execute("select last_date,sum(flow_data) from app_flowtable"+sql_add+" group by last_date")
    cur_city.execute("select city,sum(flow_data) from app_flowtable"+sql_add+" GROUP by city  order by sum(flow_data) desc")
    cur_city_bandwidth.execute("select city,sum(band_width) from app_flowtable"+sql_add+" GROUP by city  order by sum(band_width) desc")
    cur_city_peak.execute("select city,avg(bu_peak) from app_flowtable"+sql_add+" GROUP by city  order by avg(bu_peak) desc")
    cur_city_busyavg.execute("select city,avg(bu_busy_avg) from app_flowtable"+sql_add+" GROUP by city  order by avg(bu_busy_avg) desc")
    cur_city_avg.execute("select city,avg(bu_avg) from app_flowtable"+sql_add+" GROUP by city  order by avg(bu_avg) desc")


    cate_flow =[]
    cate_dic = {}
    for each in cur_cate:
        cate_dic['name'] = each[0]
        cate_dic['data'] = each[1]/1000000
        cate_flow.append(cate_dic)
        cate_dic = {}

    date_name = []
    date_data = []
    for each in cur_date:
        date_name.append(each[0])
        date_data.append(each[1]/1000000)

    city_name = []
    city_data = []
    for each in cur_city:
        city_name.append(each[0])
        city_data.append(each[1]/1000000)
        city_bandwidth = []
        bandwidth_dic = {}
    for each in cur_city_bandwidth:
        bandwidth_dic['name'] = each[0]
        bandwidth_dic['data'] = each[1]
        city_bandwidth.append(bandwidth_dic)
        bandwidth_dic = {}

    city_peak_name = []
    city_peak_data = []
    for each in cur_city_peak:
        city_peak_name.append(each[0])
        city_peak_data.append(each[1])

    city_busyavg_name = []
    city_busyavg_data = []
    for each in cur_city_busyavg:
        city_busyavg_name.append(each[0])
        city_busyavg_data.append(each[1])

    city_avg_name = []
    city_avg_data = []
    for each in cur_city_avg:
        city_avg_name.append(each[0])
        city_avg_data.append(each[1])



    cur_flow.execute("select sum(flow_data) from app_flowtable" + sql_add)
    cur_peak.execute("select avg(bu_peak) from app_flowtable" + sql_add)
    cur_busyavg.execute("select avg(bu_busy_avg) from app_flowtable" + sql_add)
    cur_avg.execute("select avg(bu_avg) from app_flowtable" + sql_add)

    try:
        for each in cur_flow:
                    flow_data=int(each[0]/1000000)
        for each in cur_peak:
                    peak_data=str(round(each[0]*100,2))+'%'
        for each in cur_busyavg:
                    busyavg_data=str(round(each[0]*100,2))+'%'
        for each in cur_avg:
            avg_data = str(round(each[0] * 100, 2)) + '%'
    except TypeError:
        flow_data=peak_data=busyavg_data=avg_data='无数据'


    cur_catedrop=conn.cursor()
    cur_citydrop = conn.cursor()
    cur_datedrop = conn.cursor()
    cur_catedrop.execute("select distinct cate from app_flowtable")
    cur_citydrop.execute("select distinct city from app_flowtable")
    cur_datedrop.execute("select distinct last_date from app_flowtable")
    catedroplist=[]
    citydroplist=[]
    datedroplist=[]
    for each in cur_catedrop:
        catedroplist.append(each[0])
    for each in cur_citydrop:
        citydroplist.append(each[0])
    for each in cur_datedrop:
        datedroplist.append(each[0])


    context = {
        'cateflow':cate_flow,
        'city_bandwidth':city_bandwidth,
        'datename':date_name,
        'datedata':date_data,
        'cityname':city_name,
        'citydata':city_data,
        'city_peak_name':city_peak_name,
        'city_peak_data':city_peak_data,
        'city_busyavg_name':city_busyavg_name,
        'city_busyavg_data': city_busyavg_data,
        'city_avg_name': city_avg_name,
        'city_avg_data': city_avg_data,
        'flowdata':flow_data,
        'peakdata':peak_data,
        'busyavgdata':busyavg_data,
        'avgdata':avg_data,
        'catedroplist':catedroplist,
        'citydroplist':citydroplist,
        'datedroplist':datedroplist,


    }
    return render(request,'chart.html',context)

@login_required
def top_n(request):
    date_str = str(request.POST.get('filter1'))
    top_str = str(request.POST.get('filter2'))
    datedrop_list = FlowTable.objects.values('last_date').distinct()


    if date_str == 'None' or date_str == '':
        if top_str=='None' or top_str=='':
            topcount=10
        else:
            topcount=int(top_str)
        flow_top=FlowTable.objects.order_by('-flow_data')[0:topcount]
        peak_top=FlowTable.objects.order_by('-bu_peak')[0:topcount]
        busyavg_top=FlowTable.objects.order_by('-bu_busy_avg')[0:topcount]
        avg_top=FlowTable.objects.order_by('-bu_avg')[0:topcount]
    else:
        if top_str=='None' or top_str=='':
            topcount=10
        else:
            topcount=int(top_str)
        flow_top=FlowTable.objects.filter(last_date=date_str).order_by('-flow_data')[0:topcount]
        peak_top=FlowTable.objects.filter(last_date=date_str).order_by('-bu_peak')[0:topcount]
        busyavg_top=FlowTable.objects.filter(last_date=date_str).order_by('-bu_busy_avg')[0:topcount]
        avg_top=FlowTable.objects.filter(last_date=date_str).order_by('-bu_avg')[0:topcount]

    context = {
        'flow_top':flow_top,
        'peak_top':peak_top,
        'busyavg_top':busyavg_top,
        'avg_top':avg_top,
        'datedrop_list':datedrop_list,
        'topcount':topcount
    }
    return render(request, 'top_n.html', context)

@login_required
def buildlog(request):

    title_post=str(request.POST.get('title'))
    inner_post=str(request.POST.get('inner'))
    if title_post!='None' and inner_post!='None':
        if (title_post != '' and inner_post != ''):
            BuildLog.objects.create(title=title_post,inner=inner_post)
    build_log=BuildLog.objects.all()
    context={
            'build_log':build_log,
        }
    return render(request, 'buildlog.html',context)

@login_required
def link(request):
    return render(request, 'link.html')

@login_required
def warning(request):
    date_str = str(request.POST.get('filter1'))
    datedrop_list=FlowTable.objects.values('last_date').distinct()

    if date_str=='None' or date_str=='':
        overload_list=FlowTable.objects.filter(bu_peak__gte=0.7).order_by("-bu_peak")
    else:
        overload_list=FlowTable.objects.filter(bu_peak__gte=0.7).filter(last_date=date_str).order_by("-bu_peak")


    context={
        'overload_list':overload_list,
        'datedrop_list':datedrop_list
    }

    return render(request, 'warning.html', context)

@login_required
def test(request):
    model0=FlowTable.objects.all()
    listbox=model0.values('cate').distinct()
    sum_cate=model0.raw('select id,cate,sum("flow_data") from app_flowtable group by cate')
    context={
        'listbox':listbox,
        'sum_cate':sum_cate
    }

    return render(request,'test.html',context)

def login_view(request):
    if request.method=='post':

        username=request.POST.get('username')
        password=request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user!=None:

            return HttpResponseRedirect('index.html')
    else:
        return render_to_response('registration/login.html')


def loginjudge(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user !=None:
        return user.is_active
    else:
        return False






