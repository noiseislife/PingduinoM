I never appreciated my internet connection enough when I lived in the city.  Now that I'm a
country mouse I think it really IS a series of tubes. Reliable it's not.  So I thought it
would be fun to use an Arduino, my BlinkM and a bit of python to create a visual network monitor.

Here are the steps:

1. Plug your BlinkM into analog ports 2-5 (the standard way instructed by ThingM).

2. Load the Communicator sketch from ThingM onto your arduino.

3. Run the python script. This must be run as Administrator on windoze and although I haven't
tried it yet I believe it must be run as root on Linux.  The code should be safe, but review
it anyway for your own piece of mind.

Here's the python script, this includes ping.py <http://svn.pylucid.net/pylucid/CodeSnippets/ping.py> 
which is a pure python module I use for ping functionality.  I also hacked code from 
John Tokash <http://johntokash.com/2009/03/23/python-os-x-arduino-blinkm/> for talking to the BlinkM.
You will also need the pySerial <http://pyserial.sourceforge.net/> module installed.

Pat Arneson
<http://noiseislife.tumblr.com>
<http://twitter.com/noise_is_life>
