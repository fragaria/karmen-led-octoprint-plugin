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
    octoprint.plugin.SimpleApiPlugin
):

    def on_after_startup(self):
        self._logger.info(self._identifier)
        self._logger.info("Hello World!")

    def get_api_commands(self):
        return dict(
            command2=["set_led"]
        )

    def on_api_command(self, command, data):
        self.logger.debug("incoming request")
        if command == "set_led":
            try:
                # con = http.client.HTTPConnection("127.0.0.1", 9091)
                # con.request('POST', '/set_led', json.dumps(data))
                self._logger.info(f"Karmen LED request: {data}")
                return flask.jsonify({"status": "OK"})
            except:
                return flask.jsonify({"status": "NOK"})

    def on_api_get(self, request):
        self._logger.debug("incoming GET request")
        return flask.jsonify(foo="bar")

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            # put your plugin's default settings here
        }

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


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Awesome Karmen LED Plugin"


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
