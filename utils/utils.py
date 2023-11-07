from django.db import models
from django.utils import timezone

"""
# A models mixin that helps in deleting a user's account data temporarily
# The deleted data is saved as a copy for a 30 day period before being deleted permanently
"""
class UserAccountMixin(models.Model):
    # saving the account deleted timezone
    deleted_at = timezone.now()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def undelete(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True