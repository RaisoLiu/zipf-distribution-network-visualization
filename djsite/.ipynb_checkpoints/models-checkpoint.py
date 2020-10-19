from django.db import models

class Data_in_addr(models.Model):
    file = models.FileField()
    key = models.CharField(max_length=200)
    def __str__(self):
        return self.key

class Data_in_str(models.Model):
	target_str = models.CharField(max_length=200)

	def __str__(self):
		return self.target_str


