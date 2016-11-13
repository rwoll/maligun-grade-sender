#! /usr/bin/env python

import requests
import json
import csv
import argparse
import os

def main():
    # CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("subject",
                        help="subject of email to be sent to all students")
    parser.add_argument("file",
                        help="name of file to be sent to all students with ext.")
    parser.add_argument("--config",
                        help="path to config file")
    parser.add_argument("--roster",
                        help="path to csv file with roster")
    parser.add_argument("--message",
                        help="path to .txt file with message for everyone")
    parser.add_argument("--directory",
                        help="directory to look for files")

    args = parser.parse_args()

    # preliminary settings
    cur_dir = os.getcwd()
    message_text = os.path.join(cur_dir, '/message.txt')
    csv_path = os.path.join(cur_dir, '/students.csv')
    config_path = os.path.join(cur_dir, '/config.json')
    file_directory = cur_dir
    desired_file = args.file
    subject = args.subject
    recipients = {}



    # check optional arguments
    if (args.config != None):
        config_path = args.config
    if (args.roster != None):
        csv_path = args.roster
    if (args.message != None):
        message_text = args.message
    if (args.directory != None):
        file_directory = args.directory

    # get config file
    with open(config_path) as config_file:
         data = json.load(config_file)

    # get standard message to be included in body of email
    with open (message_text, "r") as message_file:
        message_text = message_file.read().replace('\n', '')

    # get students and emails
    recipients = csv_parser(csv_path)

    # check to see if the files are going to be good
    recipients = check_batch(recipients, desired_file, file_directory)[0]

    # send emails if user confirms
    if (raw_input('Type confirm to send emails:').lower() == 'confirm'):
        print "confirm"
        send_all(data, recipients, subject, message_text, desired_file, file_directory)

# generate file path for directory structure
def make_path(the_file, user, directory):
    return os.path.join(directory, user, the_file)

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
