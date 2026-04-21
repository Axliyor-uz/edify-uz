from django.db import models


# class Subscription(models.Model):
#     user = models.CharField(max_length = 20)
#     plan_choices = [
#         ('basic', 'Basic'),
#         ('pro', 'Pro'),
#         ('enterprice', 'Enterprice'),
#     ]
#     start_date = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=False)
#     plan_type = models.CharField(max_length = 20, choices = plan_choices, default='basic')



#     def __str__(self):
#         return self.user

#     def can_access_premium_features(self):
#         return self.is_active  and (self.plan_type('pro') or self.plan_type('enterprice'))
    
#     def get_remaining_days(self):

#         return 30- self.start_date