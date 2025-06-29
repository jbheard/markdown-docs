# {{ title }}

## Classes
{% for class in classes %}
**[{{class.name}}]({{class.href}})**: {{ class.description }}
{% endfor %}

## Functions
{% for function in functions %}
### {{ function.name }}
{% if function.authors %}Authors: **{{ function.authors | join(', ') }}**{% endif %}

{{ function.description }}
{% if function.params %}#### Parameters
name | description | default
--- | --- | ---
{% for param in function.params %}{{ param.name }} | {{ param.description }} | {{ param.default }}
{% endfor %}
{% endif %}

{% if function.throws %}
#### Throws
{% for throw in throws %}**{{ throw.type }}**: {{ throw.message }}  
{% endfor %}
{% endif %}
{% endfor %}
