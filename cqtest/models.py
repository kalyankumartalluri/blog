from django.db import models

# Create your models here.

class TestSuite(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def __init__(self, name):
        self.name = name

class TestStep(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    expresult = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def __init__(self, name):
        self.name = name

class Test(models.Model):
    author = models.ForeignKey('auth.User')
    name = models.CharField('test name', max_length=200)
    requirement = models.CharField("requirements", blank=True, null=True,max_length=200)
    desc = models.CharField("description", blank=True, null=True,max_length=200)
    stepdesc = models.CharField("step description", blank=True, null=True, max_length=200)
    stepexpresult = models.CharField("step expresult", blank=True, null=True, max_length=200)
    # steps = models.ManyToManyField(TestStep, blank=True)
    tokenised = models.CharField("tokens", blank=True, null=True, max_length=500)

    def __unicode__(self):
        return self.name

    def publish(self):
        self.save()

