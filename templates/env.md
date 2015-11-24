name:                {{ env.name }}
description:         {{ env.description }}
chef_type:           environment
json_class:          Chef::Environment
cookbook_versions:
  {%- for cookbook, version in env.cookbook_versions.items() %}
  {{ cookbook.ljust(19) }} {{ version }}
  {%- endfor %}
default_attributes:
{%- if default_attributes %}
{% for key, val in env.default_attributes.items() recursive %}
{{ '  ' * (loop.depth -1) }}{{ key }}: {% if val is not mapping %}{{ val }}{% else %}{{ loop(val.items()) }}{% endif %}{% endfor %}
{%- endif %}
override_attributes:
{% for key, val in env.override_attributes.items() recursive %}
{{ '  ' * (loop.depth -1) }}{{ key }}:{% if val is not mapping %} {{ val }}{% else %}{{ loop(val.items()) }}{% endif %}{% endfor %}
