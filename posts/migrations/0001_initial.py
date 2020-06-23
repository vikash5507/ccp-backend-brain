# Generated by Django 3.0.7 on 2020-06-22 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('postId', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('creationTime', models.DateTimeField(auto_now_add=True)),
                ('lastModifiedTime', models.DateTimeField(auto_now=True)),
                ('likeCount', models.IntegerField(default=0)),
                ('shareCount', models.IntegerField(default=0)),
                ('replyCount', models.IntegerField(default=0)),
                ('text', models.CharField(max_length=5000)),
                ('language', models.CharField(choices=[('EN', 'English'), ('HI', 'Hindi')], max_length=5)),
                ('locality', models.CharField(max_length=30)),
                ('district', models.CharField(max_length=30)),
                ('state', models.CharField(choices=[('AP', 'Andhra Pradesh'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CG', 'Chattisgarh'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('HR', 'Haryana'), ('HP', 'Himachal Pradesh'), ('JH', 'Jharkhand'), ('KA', 'Karnataka'), ('KL', 'Kerala'), ('MP', 'Madhya Pradesh'), ('MH', 'Maharashtra'), ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OD', 'Odisha'), ('PB', 'Punjab'), ('RJ', 'Rajasthan'), ('SK', 'Sikkim'), ('TN', 'Tamil Nadu'), ('TS', 'Telangana'), ('TR', 'Tripura'), ('UP', 'Uttar Pradesh'), ('UK', 'Uttarakhand'), ('WB', 'West Bengal'), ('AN', 'Andaman and Nicobar Islands'), ('CH', 'Chandigarh'), ('DD', 'Dadra and Nagar Haveli and Daman and Diu'), ('DL', 'Delhi'), ('JK', 'Jammu and Kashmir'), ('LA', 'Ladakh'), ('LD', 'Lakshadweep'), ('PY', 'Puducherry')], max_length=2)),
                ('deleted', models.BooleanField(default=False)),
                ('media', models.ManyToManyField(to='posts.Media')),
                ('parentPostId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='posts.Post')),
                ('sharePostId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='posts.Post')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='LikesActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activityTime', models.DateTimeField(auto_now_add=True)),
                ('postId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
    ]
