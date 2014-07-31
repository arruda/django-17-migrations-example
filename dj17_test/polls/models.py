from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey('auth.User', null=True)

    def __unicode__(self):
        return "%s vote for: %s" % (str(self.user), str(self.choice))
