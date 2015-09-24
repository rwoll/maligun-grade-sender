Mailgun Email Sender
========

A proof of concept CLI emailer using the Mailgun API. This script will
automate the process of sending emails with attachments to various recipients.

## Getting Setup

This script relies on the python `requests` package. To install it, run:
```bash
$ pip install requests
```

1. Download the `grade-sender.py` and add the script to your PATH.
2. Create a directory for the script to work in.
  1. Make a `csv` file for recipients named `students.csv` in the
     working directory.  
    
     It should look something like this:
     ```csv
     USER,EMAIL
     aUser,example@example.com
     bUser,example2@example.com
     ```   
     where the entries in the `USER` column should match the name of the
     directory that persons files will be in, and the `EMAIL` column is
     their email address.
  2. Add a `config.json` file to the working directory. ([See a template here](/working_directory/config_template.json).)
     
     > [You will need a free Mailgun account for the API credentials.](https://mailgun.com/)
     >
     > **Tip:** In the `config.json` file for the `"SENDER"` field, provide it in the
     > following format: `Your Name <example@example.com>` (including the pointy brackets).
  3. Add a `message.txt` whose contents will be copied into the body of each'
     sent email.
  4. Add a folder for each student with a standard naming convention. Here is
     where you will put all of that student's assignments. ([See below](#sample-directory-layout).)
3. Run the script.

## Usage

```
usage: grade-sender.py [-h] [--config CONFIG] [--roster ROSTER]
                       [--message MESSAGE]
                       subject file

positional arguments:
  subject            subject of email to be sent to all students
  file               name of file to be sent to all students with ext.

optional arguments:
  -h, --help         show this help message and exit
  --config CONFIG    path to config file
  --roster ROSTER    path to csv file with roser
  --message MESSAGE  path to .txt file with message for everyone
```

1. `cd` into the directory that contains one folder per person.
2. Run
   ```bash
   $ grade-sender <email subject> <desired filename>
   ```

   > By default the script expects `config.json`, `message.txt`, and
   > `students.csv` file in the working directory. If any of these files are
   > located in a different place, use the optional parameters to specify their
   > location.

## Sample Directory Layout

```
working_directory
├── config.json
├── message.txt
├── students.csv
│
├── aUser
│   ├── assignment01.pdf
│   ├── assignment02.pdf
│   ├── assignment03.pdf
│   └── assignment04.pdf
│
├── bUser
│   ├── assignment01.pdf
│   ├── assignment02.pdf
│   ├── assignment03.pdf
│   └── assignment04.pdf
.
/
.
└── zUser
    ├── assignment01.pdf
    ├── assignment02.pdf
    ├── assignment03.pdf
    └── assignment04.pdf
```
