from datetime import datetime
from django.db import models


class Qna_Posting(models.Model):
    qna_idx = models.AutoField(primary_key=True)
    id = models.ForeignKey('User.User',
                           on_delete=models.CASCADE,
                           db_column="id")
    title = models.CharField(max_length=255,
                             null=True)
    body = models.TextField(null=True)
    pic = models.ImageField()
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'Qna_Posting'
        app_label = 'Qna'
        managed = False


class Qna_Chatting(models.Model):
    qna_chatting_index = models.AutoField(primary_key=True)
    qna_idx = models.ForeignKey('Qna_Posting',
                                on_delete=models.CASCADE,
                                db_column="qna_idx")
    username = models.CharField(max_length=150,
                                blank=True)
    date = models.DateTimeField(default=datetime.now)
    chatting = models.TextField(null=True)

    class Meta:
        db_table = 'Qna_Chatting'
        app_label = 'Qna'
        managed = False
