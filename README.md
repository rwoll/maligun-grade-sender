Mailgun Email Sender
========

## Usage

1. Setup config file with appropriate credentials and rename `config.json`.
   (You'll need a a free mailgun account.)[https://mailgun.com/]

   > Tip: In the config file for the sender email, provide it in the
   > following format: `Your Name <example@example.com>`.
   
2. Edit `message.txt/message.txt` to contain a message to appear in the body
   of each email.
3. Make a `csv` file for recipients named `students.csv` in the
   `working_directory`  
    
   It should look something like this:
   ```csv
   USER,EMAIL
   aUser,example@example.com
   bUser,example2@example.com
   ```   
   where the entries in the `USER` column should match the name of the
   directory that persons files will be in, and the `EMAIL` column is
   their email address.
4. `cd` into the working directory.
5. Run the script.
6. Enter the information it prompts you for and watch it send emails.

> NOTE: The script will tell you to whom it will send and to who it will not
> send. Then it will confirm that you want to send. It is recommended that
> do not confirm (and send) until all users are queued. Running the script
> twice with the same `csv` will send an email twice.


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
