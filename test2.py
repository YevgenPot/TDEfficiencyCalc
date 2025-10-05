from jinja2 import Template
import os
import webbrowser

template_str = """
<html>
<head><title>{{ title }}</title></head>
<body>
<h1>{{ title }}</h1>
<ul>
{% for tower in towers %}
<details>
  <li>{{ tower.name }}
    <ul>
    {% for path in tower.paths %}
      <li>{{ path.name }}
        <ul>
        {% for upgrade in path.upgrades %}
          <li>Level {{ upgrade.level }}: 
            {% for k,v in upgrade.data.items() %}
              {{ k }} = {{ v }}; 
            {% endfor %}
          </li>
        {% endfor %}
        </ul>
      </li>
    {% endfor %}
    </ul>
  </li>
</details>
{% endfor %}
</ul>
</body>
</html>
"""

data = {
    "title": "Tower Upgrade States",
    "towers": [
        {
            "name": "Tower A",
            "paths": [
                {
                    "name": "Path 1",
                    "upgrades": [
                        {"level": 1, "data": {"cost": 100, "power": 5}},
                        {"level": 2, "data": {"cost": 200, "power": 10}},
                    ],
                },
                {
                    "name": "Path 2",
                    "upgrades": [
                        {"level": 1, "data": {"cost": 150, "power": 6}},
                    ],
                },
            ],
        },
    ],
}

template = Template(template_str)
output_html = template.render(**data)

filePath = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(filePath, "dataDir" , "output.html")

with open(path, "w", encoding="utf-8") as f:
    f.write(output_html)

webbrowser.open(path)
