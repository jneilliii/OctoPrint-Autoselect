# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.events
import octoprint.filemanager
from octoprint.filemanager.destinations import FileDestinations

class AutoselectPlugin(octoprint.plugin.EventHandlerPlugin):
	def on_event(self, event, payload):
		if event != octoprint.events.Events.CONNECTED:
			return

		if not self._printer.is_ready():
			self._logger.debug("Printer is not ready, not autoselecting uploaded file")
			return

		filename = "autoprint.gcode" # put your filename here.
		if not octoprint.filemanager.valid_file_type(filename, type="machinecode"):
			self._logger.debug("File is not a machinecode file, not autoselecting")
			return

		self._logger.info("Selecting {} since we just connected.".format(filename))
		path = self._file_manager.path_on_disk("local", filename)
		self._printer.select_file(path, False, False)

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			autoselect=dict(
				displayName=self._plugin_name,
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="OctoPrint",
				repo="OctoPrint-AutoSelect",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/OctoPrint/OctoPrint-AutoSelect/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "Autoselect Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = AutoselectPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
