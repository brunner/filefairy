import datetime


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
    return self.logs


class TestLogger(Logger):
  """Test implementation of Logger."""

  def timestamp(self):
    return "0:0:0"
