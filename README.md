Errbot Chef Plugin
==================

Errbot Chef server integration using the familiar knife command syntax. Multiple Chef servers/orgs is supported.

This plugin only performs read commands such as `list`, `show`, `search`, and `status`. It is the author's opinion that you should not make changes directly to your Chef server. Use SCM and a CI/CD process instead. ;)

#### Example

    !knife node list

      /me is getting the list of nodes from Chef...
      /me Chef knife.rb: /home/errbot/.err-chef/knife.rb

      +----------------------------------+
      | Node                             |
      +----------------------------------+
      | webserver01                      |
      | supermarket                      |
      | jenkins_slave_01                 |
      | jenkins_slave_04                 |
      | jenkins_slave_02                 |
      +----------------------------------+

    !knife node show supermarket

      /me is getting node "supermarket" from Chef...
      /me Chef knife.rb: /home/errbot/.err-chef/knife.rb

      Node Name:   supermarket
      Environment: supermarket_env_prod
      FQDN:        supermarket.example.org
      IP:          10.10.10.10
      Run List:    recipe[supermarket_env]
      Recipes:     supermarket_env::default, base::default, chef-client::delete_validation, chef-client::config, logrotate::default, chef-client::default, chef-client::service, chef-client::init_service, supermarket::default
      Roles:
      Platform:    centos 6.6
      Tags:

Available commands for Chef
---------------------------

• !chef config - Chef config [list|set &lt;config&gt;]
• !knife environment [list|show &lt;name&gt;] - Chef knife environment ops
• !knife node [list|show &lt;name&gt;] - Chef knife node ops
• !knife role [list|show &lt;name&gt;] - Chef knife role ops
• !knife search &lt;object&gt; &lt;query&gt; - Chef knife search ops
• !knife status [query] - Chef knife status with optional search query

(see: https://docs.chef.io/knife.html)

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

##### ...OR...

Git clone into your Errbot's plugin directory. Use pip to install requirements...

    $ cd /path/to/errbot/plugins
    $ git clone https://github.com/jgrill/err-chef.git
    $ cd err-chef
    $ pip install -r requirements.txt

Configuration
-------------

#### Single Chef server

Create a `.err-chef` directory in the Errbot user's(1)(2) home directory. Place a working `knife.rb` in `~/.err-chef` along with any required `*.pem` files.

(see: https://docs.chef.io/config_rb_knife.html)

1. The Errbot user is the user Errbot is running under
2. Don't run Errbot as root, m'kay? ;)

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
