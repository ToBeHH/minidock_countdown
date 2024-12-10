# Countdown

Countdown is a minimalist countdown timer app powered by the LVGL graphics library, allowing users to set a timer and monitor countdowns through an intuitive interface.

This app is forked from the [dock-mini-apps](https://github.com/myvobot/dock-mini-apps) repo.

In addition to the original repo, the following has changed:

 * **It correctly works as a countdown!** The original app could not reliably handle countdowns longer than 20 seconds. After that, the time displayed went out of sync with the actual time!
 * There are two ways to display the remaining time (configurable via settings):
   1. You have the remaining time shown as an arc, which also changes color to yellow and red if you are approaching the end of the countdown (at 30% and 15% respectively)
   2. You have the remaining time shown as a bar running from left to right, so that you have visual control of how much time is left. The bar also changes color according to how much time is left. 
 * Additionally the remaining time can be shown on the big clokc (configurable via settings).
 * The color for the remaining time can be shown with the ambient lights (configurable via settings).