Errbot Chef Plugin
==================

Errbot Chef server integration using the familiar knife command syntax.

This plugin only performs read commands such as `list`, `show`, `search`, and `status`. It is the author's opinion that you should not make changes directly to your Chef server. Use SCM and a CI/CD process instead. ;)

Available commands for Chef
---------------------------

• !knife environment [list|show &lt;name&gt;] - Chef knife environment ops
• !knife node [list|show &lt;name&gt;] - Chef knife node ops
• !knife role [list|show &lt;name&gt;] - Chef knife role ops
• !knife search &lt;object&gt; &lt;query&gt; - Chef knife search ops
• !knife status [query] - Chef knife status with optional search query

Tip: See knife --help

Requirements
------------
- A Chef server
- Python 3.4
- pychef
- prettytable

Installation
------------

If you have the appropriate administrative privileges, you can install err-chef from chat...

    !repos install https://github.com/jgrill/err-chef.git

Use git clone into your Errbot's plugin directory. Use pip to install requirements...

    $ cd err-chef
    $ pip install -r requirements.txt

Configuration
-------------

Make sure your Errbot has a working knife.rb. That's it!


Contributing
------------

1. Fork this repository on Github
2. Create a named feature branch (like `add_component_x`)
3. Write your change
4. Submit a Pull Request

License
-------
GNU General Public License
