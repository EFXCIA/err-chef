Errbot Chef Plugin
==================

Errbot Chef server integration using the familiar knife command syntax. Multiple Chef servers/orgs is supported.

This plugin only performs read commands such as `list`, `show`, `search`, and `status`. It is the author's opinion that you should not make changes directly to your Chef server. Use SCM and a CI/CD process instead. ;)

Available commands for Chef
---------------------------

• !chef config - Chef config [list|set &lt;config&gt;]
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
- pychef ~> 0.2.3
- prettytable ~> 0.7.2

Installation
------------

If you have the appropriate administrative privileges, you can install err-chef from chat...

    !repos install https://github.com/jgrill/err-chef.git

Use git clone into your Errbot's plugin directory. Use pip to install requirements...

    $ cd /path/to/errbot/plugins
    $ git clone https://github.com/jgrill/err-chef.git
    $ cd err-chef
    $ pip install -r requirements.txt

Configuration
-------------

#### Single Chef server

Create a `.err-chef` directory in the Errbot user's home directory. Place a working `knife.rb` in `~/.err-chef` along with any required `*.pem` files.

(see: https://docs.chef.io/config_rb_knife.html)

#### Multiple Chef servers

To setup Errbot with access to multiple Chef servers, simply place mutliple `knife.rb` files in `~/.err-chef` and name them according to the following pattern: `knife-*.rb` where `*` is any unique name you like.

e.g.

    $ ls -1 ~/.err-chef
    errbot.pem
    knife-org1.rb
    knife-org2.rb

Errbot will need each user to choose which knife.rb they wish to use. A list of knife.rb files can be had by issuing the command `!chef config list` into chat. To select a knife.rb, issue the command `!chef config set <name>`.

e.g.

    !chef config list

      knife-org1.rb
      knife-org2.rb

    !chef config set knife-org1.rb

      /me Selected knife.rb knife-cia-prod.rb for someuser@chat.btf.hipchat.com

Typing `!chef config` with no arguments will return the name of the currently selected knife.rb

    !chef config

      Current knife config: /home/errbot/.err-chef/knife-org1.rb

Errbot will remember this selection for each user.

Contributing
------------

1. Fork this repository on Github
2. Create a named feature branch (like `add_component_x`)
3. Write your change
4. Submit a Pull Request

License
-------
GNU General Public License
