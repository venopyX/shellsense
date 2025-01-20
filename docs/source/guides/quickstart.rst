Quickstart Guide
==============

This guide will help you get started with ShellSense quickly.

Installation
-----------

Install ShellSense using pip:

.. code-block:: bash

   pip install shellsense

Configuration
------------

1. Run the setup command:

   .. code-block:: bash

      shellsense --setup

2. Edit your configuration file with your API keys.

Basic Usage
----------

Ask ShellSense a question:

.. code-block:: bash

   shellsense -q "What is the current weather in New York?"

Choose a specific AI provider:

.. code-block:: bash

   shellsense -p gemini -q "What is the current weather in New York?"
