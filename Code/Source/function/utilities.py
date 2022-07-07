def listLine2HTML(list): 
    html = """\
<html>
<body>
<p style="font-family:Consolas;">
"""
    for line in list: 
        html += line + '<br>\n'
    html += """</p>
</body>
</html>
    """
    return html

def listAP2HTML(name, ID, thread, type): 
    html = f"""\
<html>
<body>
<table style="font-family: 13px arial, sans-serif;border-collapse: collapse;">
  <tr style="background-color: #DDEFEF; color: #336B6B;">
    <th style="border: 1px solid; text-align: left; padding: 8px;">{type}</th>
    <th style="border: 1px solid; text-align: left; padding: 8px;">ID</th>
    <th style="border: 1px solid; text-align: left; padding: 8px;">Thread</th>
  </tr>
"""
    for i in range(len(name)): 
        bcolor = '#ddd' if (i % 2) else '#fff'
        html += f"""\
  <tr style="background-color: {bcolor};">
    <td style="border: 1px solid;padding: 8px;">{name[i]}</td>
    <td style="border: 1px solid;padding: 8px;">{ID[i]}</td>
    <td style="border: 1px solid;padding: 8px;">{thread[i]}</td>
  </tr>
"""
    html += """</table>
</body>
</html>"""
    return html

def listKey2HTML(ls): 
    html = f"""\
<html>
<body>
<table style="font-family: 13px arial, sans-serif;border-collapse: collapse;">
  <tr style="background-color: #DDEFEF; color: #336B6B;">
    <th style="border: 1px solid; text-align: left; padding: 8px;">Time</th>
    <th style="border: 1px solid; text-align: left; padding: 8px;">Key</th>
  </tr>
"""
    for i in range(len(ls)): 
        bcolor = '#ddd' if (i % 2) else '#fff'
        html += f"""\
  <tr style="background-color: {bcolor};">
    <td style="border: 1px solid;padding: 8px;">{ls[i][0]}</td>
    <td style="border: 1px solid;padding: 8px;">{ls[i][1]}</td>
  </tr>
"""
    html += """</table>
</body>
</html>"""
    return html
