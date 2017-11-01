from marrow.mailer import Mailer as MarrowMailer
from marrow.mailer import Message

import sys
import os
import pwd
import socket


class Mailer:

  MAILER = MarrowMailer(dict(manager=dict(use='immediate'), transport=dict(use='sendmail')))
  DEFAULT_USER = pwd.getpwuid(os.getuid()).pw_name
  DEFAULT_AUTHOR = DEFAULT_USER + '@' + socket.getfqdn()

  @staticmethod
  def send(message):
    Mailer.MAILER.send(message)

  @staticmethod
  def start():
    Mailer.MAILER.start()

  @staticmethod
  def stop():
    Mailer.MAILER.stop()

  @staticmethod
  def send_recommendations(changed_recommendations, new_recommendations, to_addr):
    Mailer.start()

    message = Message(
        author=Mailer.DEFAULT_AUTHOR,
        to=to_addr,
        subject='New/changed recommendations',
        plain=Mailer.get_recommendations_str(changed_recommendations, new_recommendations)
    )
    message.sendmail_f = Mailer.DEFAULT_USER
    Mailer.send(message)

    Mailer.stop()

  @staticmethod
  def get_recommendations_str(changed_recommendations, new_recommendations):
    message_str = ""
    if len(new_recommendations) > 0:
      message_str = "New recommendations:\n"
      message_str += "\n".join([str(r) for r in new_recommendations])
    if len(changed_recommendations) > 0:
      message_str = "Changed recommendations:\n"
      message_str += "\n".join([str(r) for r in changed_recommendations])
    return message_str
