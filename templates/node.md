Node Name:   {{ node.name }}
Environment: {{ node.chef_environment }}
FQDN:        {{ node.attributes['fqdn'] }}
IP:          {{ node.attributes['ipaddress'] }}
Run List:    {{ ', '.join(node.run_list) }}
Recipes:     {{ ', '.join(node.recipes) }}
Roles:       {{ ', '.join(node.roles) }}
Platform:    {{ node.attributes.platform }} {{ node.attributes.platform_version }}
Tags:        {{ ', '.join(node.attributes.tags) }}
