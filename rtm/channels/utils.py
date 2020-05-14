from dash.orgs.models import Org
from django.db.models import Sum

from rtm.channels.models import ChannelDailyStats


def get_messages_sent_org(org: Org) -> int:
    sent = ChannelDailyStats.objects.filter(msg_direction="O", channel__org=org).aggregate(total=Sum("count"))
    return sent.get("total", 0)


def get_messages_received_org(org: Org) -> int:
    received = ChannelDailyStats.objects.filter(msg_direction="I", channel__org=org).aggregate(total=Sum("count"))
    return received.get("total", 0)


def get_messages_engagement_org(sent: int = 0, received: int = 0) -> int:
    sent = 0 if sent is None else sent
    received = 0 if received is None else received
    return (100 * received) / sent if sent > 0 else 0
