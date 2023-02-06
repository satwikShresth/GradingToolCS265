import subprocess

recipient = 'ss5278@drexel.edu'
sender = 'noreply@CS265.drexel.edu'
subject = 'Test Email'
message = 'This is a test email sent using Python.'

mail_command = f"echo '{message}' | mail -s '{subject}' -r '{sender}' {recipient}"

result = subprocess.run(mail_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if result.returncode == 0:
    print('Email sent successfully.')
else:
    print('An error occurred while sending the email:', result.stderr.decode().strip())
