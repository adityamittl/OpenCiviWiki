"""
Activity Model
Records user activity
"""

from django.db import models

from accounts.models import Profile
from .civi import Civi
from .thread import Thread


class ActivityManager(models.Manager):
    def votes(self, civi_id):
        civi = Civi.objects.get(id=civi_id)
        votes = dict(
            votes_vneg=civi.votes_vneg,
            votes_neg=civi.votes_neg,
            votes_neutral=civi.votes_neutral,
            votes_pos=civi.votes_pos,
            votes_vpos=civi.votes_vpos,
        )
        return votes


class Activity(models.Model):
    account = models.ForeignKey(
        Profile, default=None, null=True, on_delete=models.PROTECT
    )
    thread = models.ForeignKey(
        Thread, default=None, null=True, on_delete=models.PROTECT
    )
    civi = models.ForeignKey(Civi, default=None, null=True, on_delete=models.PROTECT)

    activity_CHOICES = (
        ("vote_vneg", "Vote Strongly Disagree"),
        ("vote_neg", "Vote Disagree"),
        ("vote_neutral", "Vote Neutral"),
        ("vote_pos", "Vote Agree"),
        ("vote_vpos", "Vote Strongly Agree"),
        ("favorite", "Favor a Civi"),
    )
    activity_type = models.CharField(max_length=255, choices=activity_CHOICES)

    read = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def is_positive_vote(self):
        return self.activity_type.endswith("pos")

    @property
    def is_negative_vote(self):
        return self.activity_type.endswith("neg")
