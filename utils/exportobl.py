#!/usr/bin/env python

import datetime
import getpass
import os
import smtplib

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.MIMEText import MIMEText

# Replace these values with your own information.
leaguefile = "orangeandblue.lg"
teamfile = "team_47.ootp"
sender = "brunnerj16@gmail.com"
teamname = "Twins"
 
def main():
  password = getpass.getpass("Password for {0}: ".format(sender))
  recipient = "commissioner@orangeandblueleaguebaseball.com"
  subject = "{0} Export".format(teamname)
  exportpath = ("{0}/.Out of the Park Developments/OOTP Baseball 16/custdata/saved_games/" +
                "{1}/import_export/{2}").format(os.path.expanduser("~"), leaguefile, teamfile)

  session = smtplib.SMTP("smtp.gmail.com", 587)
  session.ehlo()
  session.starttls()
  session.ehlo
  session.login(sender, password)

  msg = MIMEMultipart()
  msg["Subject"] = subject
  msg["To"] = recipient
  msg["From"] = sender
  
  with open(exportpath, "rb") as fp:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(fp.read())

  encoders.encode_base64(part)
  part.add_header("Content-Transfer-Encoding", "base64")
  part.add_header("Content-Disposition", "attachment; filename=team_47.ootp")
  msg.attach(part)

  qwertyuiop = msg.as_string()
  session.sendmail(sender, [recipient, "", sender], qwertyuiop)
  session.quit()
 
if __name__ == "__main__":
  main()