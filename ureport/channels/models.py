from django.db import models
from django.utils.translation import ugettext_lazy as _

from dash.orgs.models import Org


class ChannelStats(models.Model):
    org = models.ForeignKey(
        Org,
        on_delete=models.PROTECT,
        related_name="channels",
        verbose_name=_("UNCT"),
        help_text=_("The organization this channel is part of"),
    )

    uuid = models.CharField(max_length=255)
    channel_type = models.CharField(max_length=5)
    msg_count = models.PositiveIntegerField()
    ivr_count = models.PositiveIntegerField()
    error_count = models.PositiveIntegerField()

    @classmethod
    def update_or_create(cls, org, uuid, channel_type, msg_count, ivr_count, error_count):
        existing = cls.objects.filter(uuid=uuid, org=org)

        if existing:
            existing.update(msg_count=msg_count, ivr_count=ivr_count, error_count=error_count)
            channel = existing.first()
        else:
            channel = ChannelStats.objects.create(
                org=org,
                uuid=uuid,
                channel_type=channel_type,
                msg_count=msg_count,
                ivr_count=ivr_count,
                error_count=error_count,
            )
        return channel

    def __str__(self):
        return "{} - {}".format(self.uuid, self.channel_type)


class ChannelDailyStats(models.Model):
    channel = models.ForeignKey(
        ChannelStats,
        on_delete=models.CASCADE,
        related_name="daily_stats",
    )
    msg_type = models.CharField(max_length=1)
    msg_direction = models.CharField(max_length=1)
    date = models.DateField()
    count = models.PositiveIntegerField()

    @classmethod
    def update_or_create(cls, channel, direction, msg_type, date, count):
        direction = "I" if direction == "Incoming" else "O"
        msg_type = "M" if msg_type == "msg" else "I"
        existing = cls.objects.filter(channel=channel, msg_type=msg_type, date=date)

        if existing:
            existing.update(count=count)
        else:
            ChannelDailyStats.objects.create(
                channel=channel,
                msg_type=msg_type,
                msg_direction=direction,
                date=date,
                count=count,
            )


class ChannelMonthlyStats(models.Model):
    channel = models.ForeignKey(
        ChannelStats,
        on_delete=models.CASCADE,
        related_name="monthly_stats",
    )
    date = models.DateField()
    incoming_messages_count = models.PositiveIntegerField()
    outgoing_messages_count = models.PositiveIntegerField()
    incoming_ivr_count = models.PositiveIntegerField()
    outgoing_ivr_count = models.PositiveIntegerField()

    @classmethod
    def update_or_create(cls, channel, date, incoming_messages, outgoing_messages, incoming_ivr, outgoing_ivr):
        existing = cls.objects.filter(channel=channel, date=date)

        if existing:
            existing.update(
                incoming_messages_count=incoming_messages,
                outgoing_messages_count=outgoing_messages,
                incoming_ivr_count=incoming_ivr,
                outgoing_ivr_count=outgoing_ivr,
            )
        else:
            ChannelMonthlyStats.objects.create(
                channel=channel,
                date=date,
                incoming_messages_count=incoming_messages,
                outgoing_messages_count=outgoing_messages,
                incoming_ivr_count=incoming_ivr,
                outgoing_ivr_count=outgoing_ivr,
            )
