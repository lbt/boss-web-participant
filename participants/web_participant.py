#!/usr/bin/python

"""This is the BOSS Web Participant

It takes a workitem and stores it until a web interaction provides
data to continue the process.

Example::

  define 'ask someone' do
    sequence do
      web_participant :users => 'release-team',
                      :question => "Does RC look OK?",
                      :answer => "rc_ok"
      _if :test => '${f:rc_ok} == yes' do
         notify_irc :irc_channel => '${irc.log_channel}', :msg => 'RC looks OK'
         notify_irc :irc_channel => '${irc.log_channel}', :msg => 'RC is not OK'
      end
    end
  end

"""

from RuoteAMQP.participant import Workitem
from .models import Participant
import django


class ParticipantHandler:
    def __init__(self, name):
        self.db_participant = None
        pass

    def handle_wi_control(self, ctrl):
        "Handle any special control actions"
        # Cancel should remove this from the DB
        pass

    def handle_lifecycle_control(self, ctrl):
        """ participant control thread """
        if ctrl.message == "start":
            # Setup django when we're told to start, not at init time
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bwp.settings')
            django.setup()
            # NB: Ensure that a re-connecting DB is being used

    def handle_wi(self, wid):
        """Accept the WI and write it to Django for handling
        """

        # Fail by default
        wid.result = False

        if wid.fields.msg is None:
            wid.fields.msg = []

        missing = [name for name in ["bwp"]
                   if not getattr(wid.params, name, None)]
        if missing:
            raise RuntimeError("Missing mandatory parameter(s): %s" %
                               ", ".join(missing))

        # Get the Participant by name
        try:
            self.db_participant = Participant.objects.get(name=wid.bwp.name)
            self.db_participant.store(wid)
            wid.forget = True
        except Participant.DoesNotExist:
            raise RuntimeError("BOSS Web Participant: "
                               "%s not defined in django app" % name)
        except Participant.CantStoreWIP:
            raise RuntimeError("BOSS Web Participant: "
                               "Error storing workitem")
