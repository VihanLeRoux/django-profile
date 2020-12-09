from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_pic_dir(instance, filename):
    return 'profile_pictures/user_{0}/{1}'.format(instance.user.id, filename)
    
class Profile(models.Model):
    profile_picture = models.ImageField(upload_to=user_pic_dir, default='../static/images/user.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=500, blank=True)
        
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()