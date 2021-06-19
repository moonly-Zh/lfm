from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create
# your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .models import User, Remark, Like, Article, Follow
from . import ipurl
from django.utils.timezone import now
import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.shortcuts import render
from django.http import JsonResponse
import datetime
from django.db import connection

def follow(request):
    if request.method == 'GET':
        return JsonResponse({'ret': 1, 'msg': 'wrong method!'})
    elif request.method == 'POST':
        a=request.POST.get('userid')
        b=request.POST.get('followuserid')
        if a==b:
            return JsonResponse({'ret':1,'msg':' can not follow self'})
        elif Follow.objects.filter(Userid_id = a, FollowUserid = b).exists():
            return JsonResponse({'ret':0,'msg':'already follow'})
        else:
            Follow.objects.create(Userid_id = a, FollowUserid = b , FollowDate=now())
            return JsonResponse({'ret':0, 'msg':'follow successful'})

def del_follow(request):
    if request.method == 'GET':
        return JsonResponse({'ret': 1, 'msg': 'wrong method!'})
    elif request.method == 'POST':
        a=request.POST.get('userid')
        b=request.POST.get('followuserid')
        if a==b:
            return JsonResponse({'ret':1,'msg':' can not del_follow self'})
        elif Follow.objects.filter(Userid_id = a, FollowUserid = b).exists():
            Follow.objects.filter(Userid_id = a, FollowUserid = b).delete()
            return JsonResponse({'ret':0, 'msg':'delete follow successful'})
        else:
            return JsonResponse({'ret':1, 'msg':'no follow'})

def regist(request):
    if request.method == 'GET':
        return JsonResponse({'ret': 1, 'msg': 'wrong method!'})
    elif request.method == 'POST':
        UserName = request.POST.get('username')
        PassWord = request.POST.get('password')
        if User.objects.filter(UserName=UserName).exists():
            return JsonResponse({'ret': 1, 'msg': 'this UserName were already existed'})
        else:
            SignDate = now().year
            User.objects.create(UserName=UserName, PassWord=PassWord)
            return JsonResponse({'ret': 0, 'msg': 'regist successful'})


def login(request):
    if request.method == 'GET':
        return JsonResponse({'ret': 1, 'msg': 'wrong method!'})
    elif request.method == 'POST':
        UserName = request.POST.get('username')
        PassWord = request.POST.get('password')
        if User.objects.filter(UserName=UserName).exists():
            user = User.objects.get(UserName=UserName)
            if user.PassWord == PassWord:
                userid=user.id
                return JsonResponse({'ret': 0, 'msg': 'login successfully!','userid': userid})
            else:
                return JsonResponse({'ret': 1, 'msg': 'wrong password'})
        else:
            return JsonResponse({'ret': 1, 'msg': 'id not exist'})


def remark(request):
    if request.method == 'GET':
        return JsonResponse({'ret': 1, 'msg': 'wrong method!'})
    elif request.method == "POST":
        articleid = request.POST.get('articleid')
        remark = request.POST.get('remark')
        remarkuserid = request.POST.get('remarkuserid')
        remarkdate = now()
    
        Remark.objects.create(Articleid_id=articleid, Remark=remark, RemarkUserid=remarkuserid, RemarkDate=remarkdate)
        
        return JsonResponse({'ret': 0, 'msg': 'remark successful'})

def like(request):
    if request.method == 'GET':
        return JsonResponse({'ret': 1, 'msg': 'wrong method!'})
    elif request.method == 'POST':
        articleid = request.POST.get('articleid')
        likeuserid = request.POST.get('likeuserid')
        if Like.objects.filter(Articleid_id=articleid, LikeUserid=likeuserid).exists():
            num = Like.objects.filter(Articleid_id=articleid).count()
            return JsonResponse({'ret': 0, 'msg': 'already liked','num':num})
        else:
            Like.objects.create(Articleid_id=articleid, LikeUserid=likeuserid)
            num = Like.objects.filter(Articleid_id=articleid).count()
            return JsonResponse({'ret': 0, 'msg': 'like successful','num':num})

def del_like(request):
    if request.method == 'GET':
        return JsonResponse({'ret': 1, 'msg': 'wrong method!'})
    elif request.method == 'POST':
        articleid = request.POST.get('articleid')
        likeuserid = request.POST.get('likeuserid')
        if Like.objects.filter(Articleid_id=articleid, LikeUserid=likeuserid).exists():
            Like.objects.filter(Articleid_id=articleid, LikeUserid=likeuserid).delete()
            num = Like.objects.filter(Articleid_id=articleid).count()
            return JsonResponse({'ret': 0, 'msg': 'delete like successful','num':num})
        else:
            num = Like.objects.filter(Articleid_id=articleid).count()
            return JsonResponse({'ret': 0, 'msg': 'no like','num':num})


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST','PUT','DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'show_article':
        return showarticle(request)
    elif action == 'login':
        return login(request)
    elif action == 'add_article':
        return addarticle(request)
    elif action == 'modify_article':
        return modifyarticle(request)
    elif action == 'del_article':
        return deletearticle(request)
    elif action == 'list_article':
        return listarticles(request)
    elif action == 'have_been':
        return have_been(request)
    elif action == 'search_by_location':
        return search_by_location(request)
    elif action == 'recommend':
        return recommend(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})




#文章列表
def listarticles(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    userid = request.GET.get("userid", "")
    qs = Article.objects.filter(Userid_id = userid).values('id','Title','Location','SDate','EDate')

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})



#展示文章
def showarticle(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    articleid = request.GET.get("articleid","")

    if Article.objects.filter(id=articleid).exists():
        # 根据 id 从数据库中找到相应文章记录
        a = Article.objects.filter(id=articleid).values('Userid_id').distinct()
        b = list(a)[0]['Userid_id']

        article = Article.objects.filter(id=articleid).values()
        username = User.objects.filter(id=b).values('UserName')
    else:
        return JsonResponse({
            'ret': 1,
            'msg': f'id 为`{articleid}`的文章不存在'
        })
    retlist = list(article)
    usernames = list(username)[0]['UserName']
    return JsonResponse({'ret': 0, 'article':retlist ,'username':usernames})




#添加文章
def addarticle(request):

    info = request.params['data']

    # 从请求消息中 获取要添加文章的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象

    article = Article.objects.create(
        Userid_id=info['userid'],
        Title=info['title'],
        Public=info['public'],
        Body=info['body'],
        Location=info['location'],
        SDate=info['sdate'],
        EDate=info['edate'],)

    return JsonResponse({'ret': 0, 'id': article.id})

def add_article(request):

    # 从请求消息中 获取要添加文章的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    article = Article.objects.create(
        Userid_id=request.POST.get('userid'),
        Title=request.POST.get('title'),
        Public=request.POST.get('public'),
        Body=request.POST.get('body'),
        Location=request.POST.get('location'),
        SDate=request.POST.get('sdate'),
        EDate=request.POST.get('edate'),)

    return JsonResponse({'ret': 0, 'id': article.id})


#修改文章
def modifyarticle(request):
    # 从请求消息中 获取修改文章的信息
    # 找到该文章，并且进行修改操作

    articleid = request.params['articleid']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        article = Article.objects.get(id=articleid)
    except Article.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{articleid}`的文章不存在'
        }

    if 'title' in newdata:
        article.Title = newdata['title']
    if 'public' in newdata:
        article.Public = newdata['public']
    if 'body' in newdata:
        article.Body = newdata['body']
    if 'location' in newdata:
        article.Location = newdata['location']
    if 'sdate' in newdata:
        article.SDate = newdata['sdate']
    if 'edate' in newdata:
        article.EDate = newdata['edate']

    # 执行save才能将修改信息保存到数据库
    article.save()

    return JsonResponse({'ret': 0})



# 删除文章
def deletearticle(request):

    articleid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的文章记录
        article = Article.objects.get(id=articleid)
    except Article.DoesNotExist:
        return JsonResponse({
                'ret': 1,
                'msg': f'id 为`{articleid}`的文章不存在'
        })

    article.delete()

    return JsonResponse({'ret': 0})




#用户去过的地方
def have_been(request):
    userid = request.GET.get("userid","")
    qs = Article.objects.filter(Userid_id = userid).values('Location').distinct()
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})



#该地写过的文章

def search_by_location(request):
    location = request.GET.get("location")
    qs = Article.objects.filter(Location=location).values('id', 'Title', 'Location', 'SDate', 'EDate')
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


#推荐，因为不知道怎么推荐干脆从头输出可公开的
def recommend(request):
    qs = Article.objects.filter(Public=1).values('id', 'Title', 'Body' , 'Location')
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})



# Create your views here.
def show_my_articles(request):
    userName = request.GET.get("userName", " ")
    # request: userName
    if userName == " ":
        return JsonResponse({"statue": 10021, "message": "parameter empty"})  # 检查是否参数为空
    try:
        user = User.objects.get(UserName=userName)
    except ObjectDoesNotExist:
        return JsonResponse({"statue": 10021, "message": "userNotExist"})  # 检查用户id是否存在
    userId = user.id
    result = Article.objects.filter(Userid_id=userId).values() # 查询本人写的所有文章
    data = list(result)
    return JsonResponse({'status': 200, 'message': 'success', 'data': data})


def search_articles_by_location(request):
    # request：userId, location
    userName = request.GET.get("userName", " ")
    location = request.GET.get("location", " ")  # 读取到搜索内容
    if location == " " or userName == " ":
        return JsonResponse({"statue": 10021, "message": "parameter empty"})  # 检查是否参数为空
    if userName != "" and location != "":
        try:
            user = User.objects.get(UserName=userName)
        except ObjectDoesNotExist:
            return JsonResponse({"statue": 10021, "message": "userNotExist"})  # 检查用户id是否存在
        result = Article.objects.filter(Location=location, Userid_id=user.id).values()  # 查询本人写的所有文章 以及各个文章所有评论和点赞数
        data = list(result)  # 序列化为json
        # if result:
        return JsonResponse({'status': 200, 'message': 'success', 'data': data})
        # else:
        #     return JsonResponse({'status': 10022, 'message': 'queryresultisempty'})


def search_articles_by_date(request):
    # request：int userName; month, year 旅游的时间
    userName = request.GET.get("userName", " ")
    month = request.GET.get("month", -1)  # 读取到搜索内容
    year = request.GET.get("year", -1)  # 读取到搜索内容
    if month == -1 or userName == " " or year == -1:
        return JsonResponse({"statue": 10021, "message": "parameter empty"})  # 检查是否参数为空
    if userName != " " and month != -1 and year != -1:
        try:
            user = User.objects.get(UserName=userName)
        except ObjectDoesNotExist:
            return JsonResponse({"statue": 10021, "message": "userNotExist"})  # 检查用户id是否存在

        result = Article.objects.filter(SDate__month=month, SDate__year=year, Userid_id=user.id).values()
        data = list(result)  # 序列化为json
        return JsonResponse({'status': 200, 'message': 'success', 'data': data})


def dictfetchall(cursor):
    """将游标返回的结果保存到一个字典对象中"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def article_detail(request):
    articleId = request.GET.get("articleId", " ")  # 读取到搜索内容
    if articleId == " ":
        return JsonResponse({"statue": 10021, "message": "parameter empty"})  # 检查是否参数为空
    if articleId != " ":
        # 查询该文章的评论和点赞数
        try:
            article = Article.objects.get(id=articleId)
        except ObjectDoesNotExist:
            return JsonResponse({"statue": 10021, "message": "articleNotExist"})  # 检查id是否存在
        # result1 = Remarktest.objects.filter(Articleid_id=articleId)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT UserName, Remark FROM user, remark WHERE user.id=RemarkUserid AND Articleid_id = %s",
            [articleId])
        result1 = dictfetchall(cursor)  # 结果是列表里面嵌套字典
        likeNumber = Like.objects.filter(Articleid_id=articleId).count()
        #result2 = {'likeNumber': likeNumber}
    # data = serializers.serialize("json", result1) + serializers.serialize("json", result2)  # 序列化为json
    #data = json.dumps(result1) + json.dumps(result2)
    return JsonResponse({'status': 200, 'message': 'success', 'recommend': result1, 'likenumber':likeNumber })


def myLike(request):
    userName = request.GET.get("userName", " ")
    if userName == " ":
        return JsonResponse({"statue": 10021, "message": "parameter error"})  # 检查是否参数为空
    try:
        user = User.objects.get(UserName=userName)
    except ObjectDoesNotExist:
        return JsonResponse({"statue": 10021, "message": "userNotExist"})
    # result = Article.objects.filter(Liketest__LikeUserid=user.id)
    # data = serializers.serialize("json", result)  # 序列化为json
    cursor = connection.cursor()
    cursor.execute(
        "SELECT UserName, article.id, Title, Public, Body, Location, SDate, EDate FROM user, article, liketest WHERE user.id=Userid_id AND Articleid_id = article.id AND LikeUserid = %s", [user.id])
    result = dictfetchall(cursor)  # 结果是列表里面嵌套字典
    # data = json.dumps(result)
    return JsonResponse({'status': 200, 'message': 'success', 'data': result})


def summary(request):
    # request: int userName
    userName = request.GET.get("userName", " ")
    if userName == " ":
        return JsonResponse({"statue": 10021, "message": "parameter error"})  # 检查是否参数为空
    try:
        user = User.objects.get(UserName=userName)
    except ObjectDoesNotExist:
        return JsonResponse({"statue": 10021, "message": "userNotExist"})
    if userName != " ":
        city_last = Article.objects.last()
        city_ordered = Article.objects.filter(Userid_id=user.id).order_by(F('EDate') - F('SDate')).reverse()
        if city_ordered == None:
            pass
        else:
            city_longest = city_ordered[0]
        result = {}
        # 注册天数 int ; city_last:最近一次旅游的城市名称 string； city_longest:呆过最长城市名称 string；
        result['cityLast'] = city_last.Location
        result['sighUpDays'] = (datetime.date.today() - user.SignDate).days
        result['cityLongest_city'] = city_longest.Location
        result['cityLongest_start'] = city_longest.SDate
        result['cityLongest_end'] = city_longest.EDate
        # data = serializers.serialize("json", city_last)
        # data = serializers.serialize("json", city_longest) + serializers.serialize("json", city_last)  # 序列化为json
        
        return JsonResponse({'status': 200, 'message': 'success', 'data': result})


def show_follow(request):
    userName = request.GET.get("userName", " ")
    if userName == " ":
        return JsonResponse({"statue": 10021, "message": "parameter error"})  # 检查是否参数为空
    try:
        user = User.objects.get(UserName=userName)
    except ObjectDoesNotExist:
        return JsonResponse({"statue": 10021, "message": "userNotExist"})
    cursor = connection.cursor()
    cursor.execute(
        "SELECT UserName FROM user, follow WHERE user.id=FollowUserid AND Userid_id = %s",
        [user.id])
    result = dictfetchall(cursor)  # 结果是列表里面嵌套字典
    # data = json.dumps(result)
    return JsonResponse({'status': 200, 'message': 'success', 'data': result})

