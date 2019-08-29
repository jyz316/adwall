from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Advertisement(models.Model):
    text = models.TextField()
    image = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published', null=True)

    def pub_date_label(self):
        if not self.pub_date:
            return ''
        pub_date = timezone.localtime(self.pub_date)    
        return pub_date.strftime("%Y年%m月%d日")

    def pub_time_label(self):
    	if not self.pub_date:
    		return ''
    	pub_date = timezone.localtime(self.pub_date)
    	return pub_date.strftime("%Y年%m月%d日 %H时%M分")


