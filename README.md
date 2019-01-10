# Desktop-security
<h3>what this script it will do ?</h3>
After setting this up in your linux system, every time someone turn on your system it.
it's gonna send you an image of that person in your email .
so if that person it not you. or it,s someone unwanted. 
you can just send an email to back .like Shutdown or change password.
it will perform according to your command.

<h3>How to set up ?</h3>

> sudo cp -i Desktop-security.py /bin <br>
> sudo crontab -e <br>
  @reboot python /bin/Desktop-security.py &  #put this line inside crontab
