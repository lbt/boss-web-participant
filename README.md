Boss Web Participant
====================

The intention is to allow a process to block until a human interacts
with a web application to provide additional data.

The mechanism is similar to obsticket.

An Exo-based participant listens for workitems and places them into
the django DB.

To understand how this code works one needs to know that BOSS can mark
Workitems to be 'forgotten' which means that it expects no reply.  The
generic Participant class notices this request and simply does not
send any reply back via AMQP.  For our purposes, this behaviour is
"abused" by writing the Workitem to the Django DB and then marking the
Workitem as 'forgotten' by the participant code; thus ensuring the
workitem is not returned by the generic code and is held by the Django
app.  Once the user interacts with the Workitem the web-app briefly
connects to AMQP and sends the Workitem back to BOSS which just
handles it as if it had been returned by the original participant.
