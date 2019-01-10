# Desktop-security
what this script it will do ?
After setting this up in your linux system, every time someone turn on your system it.
it's gonna send you an image of that person in your email .
so if that person it not you. or it,s someone unwanted. 
you can just send an email to back .like Shutdown or change password.
it will perform according to your command.

How to set up ?
> sudo cp -i Desktop-security.py /bin
> sudo crontab -e 
  @reboot python /bin/Desktop-security.py &  #put this line inside crontab
