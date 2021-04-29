#!/usr/bin/python

"""This is the BOSS Web Participant

It takes a workitem and stores it until a web interaction provides
data to continue the process.

Example::

Ruote.process_definition :name => 'ask_someone', :revision => '0.1' do
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
import os
import django
# Setup django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bwp.settings')
django.setup()
from participant.models import Participant


class ParticipantHandler:
    def __init__(self):
        print("Created a ParticipantHandler")

    def handle_wi_control(self, ctrl):
        "Handle any special control actions"
        # Cancel should remove this from the DB
        pass

    def handle_lifecycle_control(self, ctrl):
        """ participant control thread """
        print(f"Lifecycle {ctrl}")
        if ctrl.message == "start":
            print("Participant started")
            self.db_participant = Participant.objects.get(name="thefirstone")
            print(self.db_participant)
            # NB: Ensure that a re-connecting DB is being used

    def handle_wi(self, wid):
        """Accept the WI and write it to Django for handling
        """

        # Fail by default
        wid.result = False

        if wid.fields.msg is None:
            wid.fields.msg = []

        print(f"Fields {wid.fields}")

        missing = [name for name in ["bwp"]
                   if not (getattr(wid.params, name, None) or getattr(wid.fields, name, None))]
        if missing:
            raise RuntimeError("Missing mandatory parameter(s): %s" %
                               ", ".join(missing))

        # Get the Participant by name
        try:
            print(f"Getting Participant({wid.fields.bwp})")
            self.db_participant = Participant.objects.get(name=wid.fields.bwp)
            self.db_participant.store(wid)
            wid.forget = True
        except Participant.DoesNotExist:
            raise RuntimeError("BOSS Web Participant: "
                               "%s not defined in django app" % name)
        except Participant.CantStoreWIP:
            raise RuntimeError("BOSS Web Participant: "
                               "Error storing workitem")
