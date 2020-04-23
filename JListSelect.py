from javax.swing import JFrame, JPanel, JLabel, JList, JButton, ListSelectionModel
from java.awt import BorderLayout

frame = JFrame("JList Example")
frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
frame.setLocation(100,100)
frame.setSize(300,250)

frame.setLayout(BorderLayout())

def listSelect(event):
   index = lst.selectedIndex
   lbl1.text = "Hello" + lang[index]

def clickhere(event):
   lst.selectionMode = ListSelectionModel.MULTIPLE_INTERVAL_SELECTION
   print "clicked"
   print lst.selectedValues[:]
   #upon clicking, ask 'are you sure?' and then close

#frame.setDefaultCloseOperation(clickhere)

lang = ("C", "C++", "Java", "Python", "Perl", "C#", "VB", "PHP", "Javascript", "Ruby")
lst = JList(lang, valueChanged = listSelect)
lbl1 = JLabel("box1 not selected box2 not selected")
frame.add(lst, BorderLayout.NORTH)
frame.add(lbl1, BorderLayout.SOUTH)
lst.selectionMode = ListSelectionModel.MULTIPLE_INTERVAL_SELECTION
button = JButton('Select item(s)', actionPerformed = clickhere)
print clickhere
frame.add(button, BorderLayout.SOUTH)
frame.setVisible(True)


print "list = ", lst