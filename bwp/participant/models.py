from django.db import models

# class BOSS(models.Model):
#     """The BOSS instance a Participant is connected to.
#     """
#     name = models.CharField(
#         help_text="Name of the BOSS instance",
#         max_length=80)
#     config_name = models.CharField(
#         help_text="Section name of the BOSS connection details in skynet.conf",
#         max_length=80)


class Participant(models.Model):
    """A participant that can interact with BOSS

    An instance of a Participant defines the amqp queue used and the
    class that provides the consume """

    name = models.CharField(
        help_text="Name",
        max_length=80)
    queue = models.CharField(
        help_text="AMQP message queue being monitored",
        max_length=80)
    # boss = models.ForeignKey(BOSS)

    def store(self, wid):
        self.db_participant.job_set.create(
            workitem=wid)


class Job(models.Model):
    """Stores a job for a Participant interaction with BOSS
    """
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    workitem = models.JSONField(
        help_text="process workitem for a Participant interaction")
