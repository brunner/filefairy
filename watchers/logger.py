import datetime
import slack


class Logger(object):
  """Records log entries."""

  def __init__(self):
    self.logs = []

  def timestamp(self):
    return datetime.datetime.now().strftime('%H:%M:%S')

  def log(self, message):
    t = self.timestamp()
    self.logs.append("[{0}] {1}".format(t, message))

  def dump(self):
    slack.postMessage("\n".join(self.logs), "testing")
    return self.logs


class TestLogger(Logger):
  """Test implementation of Logger."""

  def __init__(self, slack=False):
    """Initializes the TestLogger.

    Pass slack=True to interface with the testing Slack channel."""
    self.logs = []
    self.slack = slack

  def timestamp(self):
    return "0:0:0"

  def dump(self):
    if self.slack:
      slack.postMessage("\n".join(self.logs), "testing")
    return self.logs
