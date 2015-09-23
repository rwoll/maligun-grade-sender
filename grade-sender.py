#! /usr/bin/env python

import requests
import json
import csv

def main():

    # preliminary settings
    cur_dir = '.'
    message_text = cur_dir + '/message.txt'
    csv_path = cur_dir + '/students.csv'
    desired_file = raw_input('Desired File (including extension): ')
    subject = raw_input('Email Subject: ')
    recipients = {}

    # get config file
    with open(cur_dir + '/config.json') as config_file:
         data = json.load(config_file)

    # get standard message to be included in body of email
    with open (message_text, "r") as message_file:
        message_text = message_file.read().replace('\n', '')
    
    # get students and emails
    recipients = csv_parser(csv_path)

    # check to see if the files are going to be good
    recipients = check_batch(recipients, desired_file, cur_dir)[0]

    # send emails if user confirms
    if (raw_input('Type confirm to send emails:') == 'confirm'):
        send_all(data, recipients, subject, message_text, desired_file, cur_dir)

# generate file path for directory structure
def make_path(the_file, user, directory):
    return directory + '/' + user + '/' + the_file

# get user and email addresses form CSV into a dictionary
def csv_parser(file_path):
    csv_file = open(file_path, 'r')
    dictionary = {}
    with csv_file as emails:
        reader = csv.DictReader(emails)
        for row in reader:
            dictionary[row['USER']] = row['EMAIL']
    return dictionary

def check_batch(recipients, desired_file, parent_directory):
    succeed_recipients = {}
    failed_recipients = {}

    # try opening each file that we are going to send
    for user, email in recipients.iteritems():
        try: 
            with open(make_path(desired_file, user, parent_directory)) as attachment:
                succeed_recipients[user] = email
        except IOError:
            failed_recipients[user] = email

    # print results
    print "Files found for the following students:"
    for usr, eml in succeed_recipients.iteritems():
        print '\033[92m' + usr + '<'+ eml + '>' + '\033[0m'

    print "Files NOT found for the following student:"
    for usr, eml in failed_recipients.iteritems():
        print '\033[91m' + usr + '<'+ eml + '>' + '\033[0m'

    return [succeed_recipients, failed_recipients]

# send personalized email to student with grade
def send_grade(sender_info, recipient, subject, message, attachment):
    return requests.post(
        sender_info['MAIL_URL'],
        auth=('api', sender_info['MG_API']),
        files=[("attachment",attachment)],
        data={'from': sender_info['SENDER'],
              'to': recipient,
              'subject': subject,
              'text': message})
    
# send emails to all students
def send_all(sender_info, recipients, subject, message, desired_file, parent_directory):
    print "Sending..."
    for user, email in recipients.iteritems():
            with open(make_path(desired_file, user, parent_directory)) as attachment:
                r = send_grade(sender_info, email, subject, message, attachment)
                if (r.status_code != 200):
                    # mailgun server regected
                    print '\033[91m'+ 'FAILED ' + user + '<' + email + '>' + '\033[0m'
                else:
                    print '\033[92m' + 'SENT  ' + user + '<' + email + '>' + '\033[0m'
    print "Complete."

if __name__ == "__main__": main()
