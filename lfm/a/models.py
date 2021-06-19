from django.db import models

# Create your models here.
from django.utils.timezone import now


class User(models.Model):
    UserName = models.CharField(max_length=30, unique=True)
    PassWord = models.CharField(max_length=30)
    SignDate = models.DateField(auto_now=True)

    def __str__(self):
        return [self.UserName, self.PassWord]

    class Meta:
        db_table = 'user'


class Article(models.Model):
    LOCATION_SIZES = {
        ('北京', '北京'),
        ('山东', '山东'),
        ('山西', '山西'),
        ('河南', '河南'),
        ('河北', '河北'),
        ('湖南', '湖南'),
        ('湖北', '湖北'),
        ('辽宁', '辽宁'),
        ('吉林', '吉林'),
        ('江苏', '江苏'),
        ('浙江', '浙江'),
        ('安徽', '安徽'),
        ('福建', '福建'),
        ('江西', '江西'),
        ('广东', '广东'),
        ('海南', '海南'),
        ('四川', '四川'),
        ('贵州', '贵州'),
        ('云南', '云南'),
        ('陕西', '陕西'),
        ('甘肃', '甘肃'),
        ('青海', '青海'),
        ('新疆', '新疆'),
        ('台湾', '台湾'),
        ('黑龙江', '黑龙江'),
        ('上海市', '上海市'),
        ('天津市', '天津市'),
        ('重庆市', '重庆市'),
        ('西藏自治区', '西藏自治区'),
        ('内蒙古自治区', '内蒙古自治区'),
        ('广西壮族自治区', '广西壮族自治区'),
        ('宁夏回族自治区', '宁夏回族自治区'),
        ('香港特别行政区', '香港特别行政区'),
        ('澳门特别行政区', '澳门特别行政区'),
    }

    Userid = models.ForeignKey('User',on_delete=models.CASCADE)
    Title = models.CharField(max_length=40)
    Public = models.BooleanField(default=True)
    Body = models.TextField(max_length=5000)
    Location = models.CharField(max_length=50, choices=LOCATION_SIZES)
    SDate = models.DateField(auto_now=False,default='1111-11-11')
    EDate = models.DateField(auto_now=False,default='1111-11-11')

    class Meta:
        db_table = 'article'
        ordering = ['SDate']
    
    def __str__(self):
        return self.Title




class Follow(models.Model):
    Userid = models.ForeignKey('User', on_delete=models.CASCADE)
    FollowUserid = models.IntegerField()
    FollowDate = models.DateField(auto_now=True)

    class Meta:
        db_table = 'follow'


class Remark(models.Model):
    Articleid = models.ForeignKey('Article', on_delete=models.CASCADE)
    Remark = models.TextField(max_length=100000)
    RemarkUserid = models.IntegerField()
    RemarkDate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'remark'


class Like(models.Model):
    Articleid = models.ForeignKey('Article', on_delete=models.CASCADE)
    LikeUserid = models.IntegerField()

    class Meta:
        db_table = 'liketest'



