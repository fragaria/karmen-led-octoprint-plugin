# coding=utf-8
from __future__ import absolute_import
from apa102_pi.driver import apa102


### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import flask

class AwesomeKarmenLedPlugin(octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.ShutdownPlugin,
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.EventHandlerPlugin,
):

    def on_after_startup(self):
        self.led_init()
        init_color = (0, 16, 0)
        self.set_single_color(init_color)


    def on_shutdown(self):
        self.strip.clear_strip()


    def get_api_commands(self):
        return dict(
            set_led=["color"]
        )


    def on_api_command(self, command, data):
        self._logger.debug("incoming request")
        if self._settings.get(["mode"]) == "api":
            if command == "set_led":
                try:
                    self._logger.info(f"Karmen LED request: {data}")
                    self.set_single_color(data["color"])
                    return flask.jsonify({"status": "OK"})
                except Exception as e:
                    self._logger.error(e)
                    return flask.jsonify({"error": e})


    def led_init(self):
        self.strip = apa102.APA102(num_led=int(self.led_count), order='rgb')
        self.strip.set_global_brightness(255)
        self.strip.clear_strip()


    def set_leds(self, colors):
        for i, c in enumerate(colors):
            self.strip.set_pixel(i, c[0], c[1], c[2])
            self.last_color = c
        self.strip.show()


    def set_single_color(self, color):
        for i in range(int(self.led_count)):
            self.strip.set_pixel(i, color[0], color[1], color[2])
        self.strip.show()
        self.last_color = color


    def on_api_get(self, request):
        return flask.jsonify(color=self.last_color)


    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            "ready": True,
            "mode": "api",
            "led_count": 2,
        }


    def on_settings_save(self, data):
        if data.get("led_count"):
            data["led_count"] = int(data["led_count"])
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)


    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]


    def get_template_vars(self):
        return {
            "mode": self._settings.get(["mode"]),
            "led_count": self._settings.get(["led_count"]),
        }


    @property
    def led_count(self):
        return int(self._settings.get(["led_count"]))

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/awesome_karmen_led.js"],
            "css": ["css/awesome_karmen_led.css"],
            "less": ["less/awesome_karmen_led.less"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "awesome_karmen_led": {
                "displayName": "Awesome Karmen LED Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "fragaria",
                "repo": "karmen-led-octoprint-plugin",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/fragaria/karmen-led-octoprint-plugin/archive/{target_version}.zip",
            }
        }


    @property
    def event_color_table(self):
        return {
            # "Startup": (32, 32, 0), -- emited before settings are ready, commented out for now
            "Shutdown": (32, 0, 0),
            "Connecting": (32, 16, 0),
            "Connected": (0, 64, 0),
            "Disconnecting": (32, 32, 0),
            "Disconnected": (32, 32, 0),
            "Error": (128, 0, 0),
            "PrintStarted": (0, 128, 0),
            "PrintFailed": (128, 0, 0),
            "PrintDone": (128, 128, 0),
            "PrintCancelling": (0, 0, 128),
            "PrintCancelled": (128, 128, 0),
            "PrintPaused": (128, 0, 128),
            "PrintResumed": (0, 128, 0),
        }


    def on_event(self, event, payload):
        if self._settings.get(["mode"]) == "auto":
            color = self.event_color_table.get(event)
            if color:            
                self.set_single_color(color)

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Awesome Karmen LED"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = AwesomeKarmenLedPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
