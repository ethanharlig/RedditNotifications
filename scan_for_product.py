import smtplib
import time
import praw
import credentials


times = 0

from_address = 'some_email_address@gmail.com'
to_address = '1234567890@vtext.com'


def send_email(server, username, title, url):
    with open('addresses.txt') as f:
        plain = f.readlines()
    nums = []
    for p in plain:
        nums.append(p.rstrip('\n'))

    for num in nums:
        msg = "\r\n".join([
              "From: " + from_address,
              "To: " + to_address,
              "Subject: " + str(title),
              "",
              str(url)
              ])
        server.sendmail(username, num, msg)


def check_for_new_stuff(server, username):
    reddit = praw.Reddit(client_id=credentials.r_client_id,
            client_secret=credentials.r_client_secret,
            user_agent=credentials.r_user_agent)

    subreddit = reddit.subreddit('buildapcsales')

    sub = subreddit.new(limit=10)

    f = open('found.txt', 'r+')

    content = f.readlines()
    content = [x.strip() for x in content]

    for submission in sub:
        if '[monitor]' in (submission.title).lower():
            f.write(str(submission.id) + '\n')

            send_email(server, username, submission.title, submission.shortlink)

            global times
            times += 1
            print("Number of monitors found: %s\n" % times)


def main():
    with open('credentials.txt') as f:
        content = f.readlines()

    username = content[0].rstrip('\n')
    password = content[1].rstrip('\n')

    times = 0

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)

    while 1:
        check_for_new_stuff(server, username)

        time.sleep(60)

