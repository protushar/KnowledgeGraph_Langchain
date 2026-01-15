"""
Cached Graph Documents
Pre-computed knowledge graph to avoid expensive API calls during cloud deployment
"""

# Mock graph documents structure based on the document content
class MockNode:
    def __init__(self, id, type=""):
        self.id = id
        self.type = type

class MockRelationship:
    def __init__(self, source, target, type=""):
        self.source = MockNode(source)
        self.target = MockNode(target)
        self.type = type

class MockGraphDocument:
    def __init__(self):
        # Create nodes from documents
        self.nodes = [
            MockNode("User", "Person"),
            MockNode("Salary", "Financial"),
            MockNode("1.8 Lakh", "Amount"),
            MockNode("Liabilities", "Financial"),
            MockNode("1.2 Lakh", "Amount"),
            MockNode("Savings", "Financial"),
            MockNode("60000", "Amount"),
            MockNode("Mahindra XUV 7XO", "Vehicle"),
            MockNode("16 Lakh", "Amount"),
            MockNode("Down Payment", "Financial"),
            MockNode("Loan", "Financial"),
            MockNode("End of Year", "Timeline"),
        ]
        
        # Create relationships
        self.relationships = [
            MockRelationship("User", "Salary", "EARNS"),
            MockRelationship("Salary", "1.8 Lakh", "AMOUNT"),
            MockRelationship("User", "Liabilities", "HAS"),
            MockRelationship("Liabilities", "1.2 Lakh", "AMOUNT"),
            MockRelationship("User", "Savings", "CAN_SAVE"),
            MockRelationship("Savings", "60000", "MONTHLY"),
            MockRelationship("User", "Mahindra XUV 7XO", "WANTS_TO_BUY"),
            MockRelationship("Mahindra XUV 7XO", "16 Lakh", "COSTS"),
            MockRelationship("Mahindra XUV 7XO", "Down Payment", "REQUIRES"),
            MockRelationship("Mahindra XUV 7XO", "Loan", "NEEDS"),
            MockRelationship("User", "End of Year", "TIMELINE"),
        ]

# Create cached graph documents
graph_documents = [MockGraphDocument()]
