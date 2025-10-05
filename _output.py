
from jinja2 import Template
import os
import webbrowser

'''
def mainOutput(linkedList):
    for i in range(len(linkedList)):
        print(f"     Path {i+1}")
        for node in linkedList[i]:
            print(f"{node.name}: {node.data['EfficiencyCost']} , {node.data['DMG']}")
            if node.data.get("DPS") != None:
                print(f"    DPS: {node.data['DPS']}")
'''

    

def mainOutput(dictoflinkedList):

    data_render = []
    columns = []
    row_keys = []
    for list_name, paths in dictoflinkedList.items():
        tower_title = list_name
        for path in paths:
            columns.append(path.head)


        data_render.append({"list_name": list_name,
                             "paths": paths})


    template_str = """
    <html>
        <head><title>Test Name</title></head>
        <body>
            {% for dict in data %}
            <h1>{{ dict.list_name }}</h1>
                <details>
                {% for path in dict.paths %}

                <table style="border-collapse: collapse; border: 1px solid black; table-layout: fixed; width: 1480px;">>
                    <tr>
                    {% for item in path %}
                        <th style="border: 1px solid #000; padding: 10px;overflow: hidden; text-overflow: ellipsis">{{ item.name }}</th>
                    {% endfor %}
                    </tr>
                    <tr>
                    {% for item in path %}
                        <td style="border: 1px solid #000; padding: 10px;overflow: hidden; text-overflow: ellipsis">{{ item.data['EfficiencyCost'] }}</td>
                    {% endfor %}
                    </tr>                    
                    <tr>
                    {% for item in path %}
                        <td style="border: 1px solid #000; padding: 10px;overflow: hidden; text-overflow: ellipsis">{{ item.data['DMG'] }}</td>
                    {% endfor %}
                    </tr> 
                    <tr>
                    {% for item in path %}
                        <td style="border: 1px solid #000; padding: 10px;overflow: hidden; text-overflow: ellipsis">{{ item.data['DPS'] }}</td>
                    {% endfor %}
                    </tr> 
                    
                </table>

                {% endfor %}
                </details>
            {% endfor %}
        </body>
    </html>
    """


    template = Template(template_str)
    output_html = template.render(data=data_render)

    filePath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(filePath, "dataDir" , "output.html")

    with open(path, "w", encoding="utf-8") as f:
        f.write(output_html)

    webbrowser.open(path)