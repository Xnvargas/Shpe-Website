import sys
import xml.dom.minidom
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="newuser",
  passwd="password",
  database="corona"
)
mycursor = mydb.cursor()
if sys.argv[1] == "coronastats0.xhtml":
    now= datetime.now()
    day = now.strftime("%d")
    document = xml.dom.minidom.parse(sys.argv[1])
    tableElements = document.getElementsByTagName("tbody")
    for tr in tableElements[0].getElementsByTagName("tr"):
        data = []
        for td in tr.getElementsByTagName("td"):
            for node in td.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    data.append(node.nodeValue.strip("\n"))
                else:
                    break
            for a in td.getElementsByTagName("a"):
                for node in a.childNodes:
                    if node.nodeType == node.TEXT_NODE:
                        data.append(node.nodeValue.replace("\n","").strip(''))


        if data[0] != "":
            state = data[0].strip()
            cases = data[1].replace(',','')
            dead = data[3].replace(',','')
        else :
            state = data[1].strip()
            cases = data[2].replace(',', '')
            dead = data[4].replace(',', '')
        if "District Of Columbia"!= state and ""!= state:
            sql = "INSERT INTO UnitedStates (name, cases, dead, day) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s,cases=%s, dead=%s, day=%s"
            val = (state, int(cases),int(dead), day, state, int(cases),int(dead), day)
            mycursor.execute(sql, val)
if sys.argv[1] == "coronastats1.xhtml":
    document = xml.dom.minidom.parse(sys.argv[1])  # node object: document
    now = datetime.now()
    day = now.strftime("%d")
    tableElements = document.getElementsByTagName("ul")
    elements = tableElements.length
    for element in range(elements):
        data = []
        for li in tableElements[element].getElementsByTagName("li"):
            for node in li.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    if "case" in node.nodeValue:
                        data.append(node.nodeValue)
        for dat in data:
            newdata = []
            datt = dat.replace(u"\xa0", u'')
            newdatt = datt.split('-')
            newdata.append(newdatt[0].strip(" "))
            rest = newdatt[1].split('|')
            for i in range(2):
                pop = rest[i].split(" ")
                newdata.append(pop[1])
            sql = "INSERT INTO LouisianaCounties (name, cases, dead, day) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s,cases=%s,dead=%s, day=%s"
            val = (newdata[0], int(newdata[1].replace(',','')), int(newdata[2].replace(',','')), day,newdata[0],int(newdata[1].replace(',','')),int(newdata[2].replace(',','')), day)
            mycursor.execute(sql, val)
mydb.commit()
mycursor.close()
mydb.close()