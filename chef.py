'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from errbot import BotPlugin, botcmd
import chef
from chef.api import ChefAPI
import datetime
from time import time
import requests
from prettytable import PrettyTable
import jinja2
import os
import glob

CONFIG_DIR = os.path.expanduser('~/.err-chef')

# disable SSL certificate warnings if using a snakeoil cert
requests.packages.urllib3.disable_warnings()

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'templates')
jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class Chef(BotPlugin):
    '''Chef plugin for Errbot.

    This module is designed to be similar to using the Chef CLI tool, knife, in
    that arguments follow the same noun->verb paradigm.
    '''
    STALE_TIME = 60 * 60
    OBJECTS = ['node', 'role', 'environment']
    VERBS = ['list', 'show']
    USER_CONF = {}

    def get_api(self, mess):
        '''Check to see if the user has selected a knife.rb. If there is only
        one, it will be selected automatically

        :param mess: Errbot message object
        '''
        configs = self.get_config_files()
        if len(configs) == 1:
            # there is only one config, so auto-select it
            self.set_config(mess, list(configs)[0])

        if self.USER_CONF.get(mess.frm.person):
            self.send(mess.frm,
                      '/me Chef knife.rb: {}'
                      .format(self.USER_CONF[mess.frm.person]['knife_file']),
                      message_type=mess.type)
        else:
            raise Exception('You have not selected a knife.rb. Run "chef '
                            'config list" to see a list of available '
                            'configs and then use "chef config set '
                            '<name>" to select one')

        return ChefAPI.from_config_file(
                       self.USER_CONF[mess.frm.person]['knife_file']
                   )

    def get_config_files(self):
        '''Get knife.rb config(s)

        :returns: result: dictionary of knife.rb name as key and path as value
        '''
        conf = glob.glob(os.path.join(CONFIG_DIR, 'knife*.rb'))
        if len(conf) < 1:
            raise Exception('No knife.rb files found at: {}'
                            .format(os.path.join(CONFIG_DIR, 'knife-*.rb')))

        return {os.path.basename(c): c for c in conf}

    def set_config(self, mess, file_name):
        '''Sets config to selected knife file

        :param mess: Errbot message object
        :param project_name: file name of knife.rb
        '''
        config_file = self.get_config_files()[file_name]
        self.USER_CONF[mess.frm.person] = {'knife_file': config_file}

        self.send(mess.frm,
                  '/me Selected knife.rb {} for {}'
                  .format(file_name, mess.frm.person),
                  message_type=mess.type)

    @botcmd(split_args_with=None)
    def chef_config(self, mess, args):
        '''Chef config [list|set <name>]'''
        if len(args) == 0:
            self.get_api(mess)
            return ('Current knife config: {}'
                    .format(self.USER_CONF[mess.frm.person]['knife_file']))
        if args[0] == 'list':
            return '\n'.join([k for k in self.get_config_files().keys()])
        elif args[0] == 'set':
            try:
                self.set_config(mess, args[1])
            except IndexError:
                raise Exception('missing required argument!')

    @botcmd(split_args_with=None)
    def knife_node(self, mess, args):
        '''Chef knife node ops. Params: [list|show <name>]'''
        try:
            verb = args.pop(0)
        except IndexError:
            raise Exception('Missing required verb. Choices are {}'
                            .format(', '.join(self.VERBS)))
        if verb not in self.VERBS:
            raise Exception('verb must be one of {}'
                            .format(', '.join(self.VERBS)))

        if verb == 'list':
            return self.node_list(mess)
        else:
            try:
                node_name = args.pop(0)
            except IndexError:
                raise Exception('Node name required')
            return self.node_show(mess, node_name)

    def node_list(self, mess):
        '''Get a list of nodes from Chef

        :param mess: Errbot message object
        '''
        self.send(mess.frm, '/me is getting the list of nodes from Chef... ',
                  message_type=mess.type)

        api = self.get_api(mess)

        pt = PrettyTable(['Node'])
        pt.align = 'l'

        for node in chef.Node.list(api=api):
            pt.add_row([node])

        return '/code {}'.format(pt)

    def node_show(self, mess, node_name):
        '''Show a Chef node

        :param mess: Errbot message object
        :param node_name: name of node to show
        '''
        self.send(mess.frm, (u'/me is getting node "{}" from '
                             'Chef...'.format(node_name)),
                  message_type=mess.type)

        api = self.get_api(mess)

        node = chef.Node(node_name, api)

        ret = jinja.get_template('node.md').render({'node': node})

        return '/code {}'.format(ret)

    @botcmd(split_args_with=None)
    def knife_environment(self, mess, args):
        '''Chef knife environment. Params [list|show <name>]'''
        try:
            verb = args.pop(0)
        except IndexError:
            raise Exception('Missing required verb. Choices are {}'
                            .format(', '.join(self.VERBS)))
        if verb not in self.VERBS:
            raise Exception('verb must be one of {}'
                            .format(', '.join(self.VERBS)))

        if verb == 'list':
            return self.env_list(mess)
        else:
            try:
                env_name = args.pop(0)
            except IndexError:
                raise Exception('Environment name required')
            return self.env_show(mess, env_name)

    def env_list(self, mess):
        '''Get a list of environments form Chef

        :param mess: Errbot mesasage object
        '''
        self.send(mess.frm, u'/me is getting the list of environments from '
                  'Chef... ', message_type=mess.type)

        pt = PrettyTable(['Environment'])
        pt.align = 'l'

        api = self.get_api(mess)

        for env in chef.Environment.list(api=api):
            pt.add_row([env])

        return '/code {}'.format(pt)

    def env_show(self, mess, env_name):
        '''Show a Chef environment

        :param mess: Errbot message object
        :param env_name: name of environment to show
        '''
        self.send(mess.frm, u'/me is getting the details for Chef environment '
                  '{} from Chef...'.format(env_name), message_type=mess.type)

        api = self.get_api(mess)

        env = chef.Environment(env_name, api=api)

        ret = jinja.get_template('env.md').render({'env': env})

        return '/code {}'.format(ret)

    @botcmd(split_args_with=None)
    def knife_role(self, mess, args):
        '''Chef knife role ops. Params: [list|show <name>]'''
        try:
            verb = args.pop(0)
        except IndexError:
            raise Exception('Missing required verb. Choices are {}'
                            .format(', '.join(self.VERBS)))
        if verb not in self.VERBS:
            raise Exception('verb must be one of {}'
                            .format(', '.join(self.VERBS)))

        if verb == 'list':
            return self.role_list(mess)
        else:
            try:
                role_name = args.pop(0)
            except IndexError:
                raise Exception('Role name required')
            return self.role_show(mess, role_name)

    def role_list(self, mess):
        '''List Chef roles

        :param mess: Errbot message object
        '''
        self.send(mess.frm, u'/me is getting the list of roles from Chef... ',
                  message_type=mess.type)

        pt = PrettyTable(['Role'])
        pt.align = 'l'

        api = self.get_api(mess)

        for role in chef.Role.list(api=api):
            pt.add_row([role])

        return '/code {}'.format(pt)

    def role_show(self, mess, role_name):
        '''Show a Chef role

        :param mess: Errbot message object
        :param role_name: name of role to show
        '''
        self.send(mess.frm, u'/me is getting the details for Chef environment '
                  '{} from Chef...'.format(role_name), message_type=mess.type)

        api = self.get_api(mess)

        role = chef.Role(role_name, api=api)

        ret = jinja.get_template('role.md').render({'role': role})

        return '/code {}'.format(ret)

    @botcmd
    def knife_status(self, mess, args=None):
        '''Chef knife status with optional search query. Params: [query]'''
        if not args:
            args = '*:*'

        self.send(mess.frm, (u'/me is getting the list of stale nodes from '
                             'Chef...'), message_type=mess.type)

        api = self.get_api(mess)

        results = chef.Search('node', args, api=api)

        # sort most stale first
        results = sorted(results,
                         key=lambda r: r.object.attributes['ohai_time'])

        pt = PrettyTable(['Node', 'Last Run'])
        pt.align = 'l'

        for node in results:
            if node.object.attributes['ohai_time']:
                last_run = int(time() - node.object.attributes['ohai_time'])

                if last_run >= self.STALE_TIME:
                    pt.add_row([node.object.name,
                               str(datetime.timedelta(seconds=last_run))])

        return '/code {}'.format(pt)

    @botcmd(split_args_with=None)
    def knife_search(self, mess, args):
        '''Chef knife search. Params: <object> <query>'''
        try:
            obj = args.pop(0)
            qry = args.pop(0)
        except IndexError:
            raise Exception('Two arguments required: <object> <query>')

        if obj not in self.OBJECTS:
            raise Exception('Invalid search object. Chose on of {}'
                            .format(', '.join(self.OBJECTS)))

        self.send(mess.frm, (u'/me is searching Chef server for {} '
                  'matching "{}"...'.format(obj, qry)), message_type=mess.type)

        api = self.get_api(mess)

        results = chef.Search(obj, qry, api=api)

        pt = PrettyTable(['Matches'])
        pt.align = 'l'

        for item in results:
            pt.add_row([item.object.name])

        return '/code {}'.format(pt)

