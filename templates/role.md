name:                {{ role.name }}
description:         {{ role.description }}
chef_type:           role
json_class:          Chef::Role
run_list:
{%- for item in role.run_list %}
  {{ item }}
{%- endfor %}
default_attributes:
{%- if role.default_attributes %}
{%- for key, val in role.default_attributes.items() recursive %}
{{ '  ' * (loop.depth -1) }}{{ key }}:{% if val is not mapping %} {{ val }}{% else %}{{ loop(val.items()) }}{% endif %}{% endfor %}
{%- endif %}
env_run_lists:
{%- for env, run_list in role.env_run_lists.items() %}
  {{ env }}:
{%- for item in run_list %}
      {{ item }}
{%- endfor %}
{%- endfor %}
override_attributes:
{%- if role.override_attributes %}
{% for key, val in role.override_attributes.items() recursive %}
{{ '  ' * (loop.depth -1) }}{{ key }}:{% if val is not mapping %} {{ val }}{% else %}{{ loop(val.items()) }}{% endif %}{% endfor %}
{%- endif %}
