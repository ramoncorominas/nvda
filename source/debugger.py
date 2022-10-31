# -*- coding: UTF-8 -*-
# Remote debugging module for Python applications
# Copyright (C) 2022 Ramón Corominas
# This file is covered by the GNU General Public License.

"""Module for remote debugging of Python applications.
Use debugger.start() to launch the debug server with default arguments. Debug port: 2633
"""


import os
import logging
logging.basicConfig(
		filename = f"{__name__}.log",
		level=logging.INFO,
		format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
debug = logging.getLogger(__name__)


# Default debug port
DEBUG_PORT = 2633

# base directory of installed (system) python (v3.7)
USER_HOME_DIRECTORY = os.path.expanduser("~")
PYTHON_EXE = rf"{USER_HOME_DIRECTORY}\AppData\Local\Programs\Python\Python37-32\python.exe"  # global environment python executable

# Default log directory for debugger
DEBUG_LOG_DIRECTORY = r"C:\logsDebugpy"


def start(
			port: int = DEBUG_PORT,
			log_to: str =DEBUG_LOG_DIRECTORY,
			python: str = PYTHON_EXE,
			wait: bool = True
	):
	"""Start debugger"""

	try:
		import debugpy
	except ImportError as exc:
		debug.exception(f"Debugpy not imported. {exc}")
	
	try:
		if not debugpy.is_client_connected():
			debugpy.log_to(log_to)
			debug.info(f"Saving debugpy logs in '{log_to}'")
			debugpy.configure(python=python)
			debug.info(f"External Python assigned to '{python}'")
			debugpy.listen(("0.0.0.0", port))
			debug.info(f"Listening in port {port}")
			if wait:
				debugpy.wait_for_client()
				debug.info("Continued after wairting for client")
		else:
			debug.warning("Debug session already connected.")
	except Exception as exc:
		debug.exception(f"Something went wrong. {exc}")


