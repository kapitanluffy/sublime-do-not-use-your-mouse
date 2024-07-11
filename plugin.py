import sublime
import sublime_plugin

import math

EXTERMINATION_TIMEOUT = 60000
RAT_COUNT = 0
RAT_MAX = 100

class DoNotUseYourMouseListener(sublime_plugin.EventListener):
	count = 0
	exterminating = False
	
	def on_text_command(self, view, command, args):
		global RAT_COUNT, EXTERMINATION_TIMEOUT
		if command != "drag_select":
			return
		RAT_COUNT = RAT_COUNT + 1
		self.show_rats(RAT_COUNT)
		sublime.set_timeout_async(self.start_extermination, EXTERMINATION_TIMEOUT)

	def show_rats(self, count, is_kill=False):
		global RAT_MAX
		if count <= 0:
			return

		nummsg = count
		msg = ""
		total = min(count, RAT_MAX)

		for c in range(total):
			img = "💀" if c == total and is_kill is True else "🐁"
			msg = msg + img

		sublime.status_message("{} {}".format(msg, nummsg))

	def start_extermination(self):
		if self.exterminating is True:
			return
		self.exterminating = True
		self.exterminate_rats()

	def exterminate_rats(self):
		global RAT_COUNT, EXTERMINATION_TIMEOUT
		if RAT_COUNT <= 0:
			self.exterminating = False
			sublime.status_message("💀")
			return
		
		RAT_COUNT = RAT_COUNT - 1
		self.show_rats(RAT_COUNT, True)
		sublime.set_timeout_async(self.exterminate_rats, EXTERMINATION_TIMEOUT)