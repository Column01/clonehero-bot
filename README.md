# Clone Hero Bot

A bot using Python and OpenCV to detect notes from clone hero and play the game for you.

## Installing

- Install Python 3.8 or newer
- Install requirements: `python -m pip install -r requirements.txt`
- Run with `python ch_bot.py`

## Configuring OBS

You must use the plugin OBS virtual cam, using the build in camera system with OBS breaks openCV (gives garbage input)
You can download and install it [here](https://obsproject.com/forum/resources/obs-virtualcam.949/)

Once installed, you need to open the settings for the obs camera. Click `Tools > VirtualCam` and make sure `Horizontal Flip` is unchecked and `Keep Aspect Ratio` is checked. Once that is done, you can click the `Start` button to start the virtual camera.

Now to configure OBS scenes.

- Create a new scene and call it `CH`.  
- Inside the `CH` scene, add a new game capture **source** and call it `CH Game`. Make sure it captures Clone Hero.  
- Right click the `CH` scene and click `Filters`. Click the `+` at the bottom left and add a new `Image Mask/Blend`. Point it to the `ch_bot mask.png` file from the repository.

It should now update in the preview to only see a small portion of the highway. No star power bar or fail bar or the note "plungers" at the bottom of the highway.

Now that you have the note cutout setup, you need to ensure that the hit window is set properly to allow the bot to hit notes inside it.

- Enable the setting "Show Hit Window"
- Start a song and subtract 10ms from your current Video calibration offset (should be negative) until the hit window fills your cutout space.
- Write down your old value somewhere in case you want to play normally, its usually 0ms anyways.

A value of -50 worked for me.  
The bot uses this hit window configuration to ensure that it doesn't have interference from the "plungers" in the note finding process.
