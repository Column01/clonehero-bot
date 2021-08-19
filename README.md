# Clone Hero Bot

A bot using Python and OpenCV to detect notes from clone hero and play the game for you.

Note: This is a WIP, current performance over-strums alot but [can get 99% on TTFATF](https://youtu.be/UjaKSFdEPBg)

## Installing

- Install Python 3.8 or newer
- Install requirements: `python -m pip install -r requirements.txt`

## Configuring OBS

You must use the plugin OBS virtual cam, using the build in camera system with OBS breaks openCV (gives garbage input)
You can download and install it [here](https://obsproject.com/forum/resources/obs-virtualcam.949/)

Once installed, you need to open the settings for the obs camera. Click `Tools > VirtualCam` and make sure `Horizontal Flip` is unchecked and `Keep Aspect Ratio` is checked. Once that is done, you can click the `Start` button to start the virtual camera.

Now to configure OBS scenes.

- Create a new scene and call it `CH`.  
- Inside the `CH` scene, add a new game capture **source** and call it `CH Game`. Make sure it captures Clone Hero.  
- Right click the `CH` scene and click `Filters`. Click the `+` at the bottom left and add a new `Image Mask/Blend`. Point it to the `ch_bot mask.png` file from the repository.

It should now update in the preview to only see a small portion of the highway. No star power bar or fail bar or the note "plungers" at the bottom of the highway.

Now that you have the note cutout setup, you should be able to test the bot.

## Running the bot

First you will need to ensure you have clone hero running. Once you do, start OBS and start the virtual cam (covered in the section above, do not use the included virtual camera!)

Once you have that done, you may need to run the code a few times changing the line that has `camera = cv2.VideoCapture(0)` and change the `0` to whatever camera number your obs virtual camera is.

To test the bot, start a song, pause it and then run the bot in a command line using `python ch_bot.py`. This will start printing some empty boxes to the screen occasionally, this is to test that it's detecting things. Unpause the game and see if the bot starts to recognize notes and playing poorly (overstrummign alot)
