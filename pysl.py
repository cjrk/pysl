import sublime
import sublime_plugin

from .java_layout import transform as java_layout


class PyslCommand(sublime_plugin.TextCommand):
	def run(self, edit, dsl):
		selection = self.view.sel()
		for region in selection:
			newText = java_layout(self.view.substr(region))
			self.view.replace(edit, region, newText)
