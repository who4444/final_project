from graphviz import Digraph

# Create a BPMN diagram
bpmn = Digraph('Library_Management_BPMN', format='png')

# Define styles for elements
bpmn.attr('node', shape='ellipse', style='filled', fillcolor='lightblue')  # Events
bpmn.node('Start', 'Start', fillcolor='green')
bpmn.node('End', 'End', fillcolor='red')

# User actions
bpmn.attr('node', shape='rectangle', style='filled', fillcolor='lightyellow')  # Tasks
bpmn.node('Register', 'Register Account')
bpmn.node('Browse', 'Browse Books')
bpmn.node('Borrow', 'Borrow Book (Max 10)')
bpmn.node('ViewHistory', 'View Borrow History')
bpmn.node('SubmitReview', 'Submit Review')
bpmn.node('ReceiveNotif', 'Receive Notification')

# Admin actions
bpmn.node('AddBook', 'Add New Book')
bpmn.node('ManageReviews', 'Manage/Delete Reviews')

# Decision points
bpmn.attr('node', shape='diamond', style='filled', fillcolor='lightgrey')  # Gateways
bpmn.node('ReviewDeleted?', 'Review Deleted?')

# User process flow
bpmn.edge('Start', 'Register')
bpmn.edge('Register', 'Browse')
bpmn.edge('Browse', 'Borrow')
bpmn.edge('Borrow', 'ViewHistory')
bpmn.edge('ViewHistory', 'SubmitReview')
bpmn.edge('SubmitReview', 'End')

# Notification flow
bpmn.edge('ReceiveNotif', 'End')

# Admin process flow
bpmn.edge('AddBook', 'End')
bpmn.edge('ManageReviews', 'ReviewDeleted?')
bpmn.edge('ReviewDeleted?', 'ReceiveNotif', label='Yes')
bpmn.edge('ReviewDeleted?', 'End', label='No')

# Connect Borrow and Admin actions separately
bpmn.edge('Browse', 'AddBook', constraint='false')

# Render the BPMN diagram
bpmn_path = "/mnt/data/library_bpmn"
bpmn.render(bpmn_path, format='png', cleanup=True)

bpmn_path + ".png"
