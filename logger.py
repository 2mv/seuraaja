from datetime import datetime


start_at = datetime.now()


def info(line):
  delta = (datetime.now() - start_at)
  timestamp = str(delta.seconds) + '.' + str(delta.microseconds / 1000) + 's'
  print(timestamp.ljust(8) + ' ' + line)
