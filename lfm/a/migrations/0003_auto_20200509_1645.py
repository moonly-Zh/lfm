# Generated by Django 3.0.5 on 2020-05-09 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0002_auto_20200508_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Location',
            field=models.CharField(choices=[('上海市', '上海市'), ('河北', '河北'), ('吉林', '吉林'), ('江苏', '江苏'), ('甘肃', '甘肃'), ('天津市', '天津市'), ('香港特别行政区', '香港特别行政区'), ('湖北', '湖北'), ('重庆市', '重庆市'), ('西藏自治区', '西藏自治区'), ('浙江', '浙江'), ('安徽', '安徽'), ('福建', '福建'), ('山东', '山东'), ('贵州', '贵州'), ('广西壮族自治区', '广西壮族自治区'), ('辽宁', '辽宁'), ('宁夏回族自治区', '宁夏回族自治区'), ('山西', '山西'), ('台湾', '台湾'), ('内蒙古自治区', '内蒙古自治区'), ('江西', '江西'), ('青海', '青海'), ('河南', '河南'), ('广东', '广东'), ('湖南', '湖南'), ('云南', '云南'), ('陕西', '陕西'), ('黑龙江', '黑龙江'), ('北京', '北京'), ('海南', '海南'), ('澳门特别行政区', '澳门特别行政区'), ('新疆', '新疆'), ('四川', '四川')], max_length=50),
        ),
        migrations.AlterField(
            model_name='article',
            name='Userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.User'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='Userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.User'),
        ),
        migrations.AlterField(
            model_name='like',
            name='Articleid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.Article'),
        ),
        migrations.AlterField(
            model_name='remark',
            name='Articleid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.Article'),
        ),
    ]
