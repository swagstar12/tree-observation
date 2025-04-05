from models import db, Tree, Question
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

    # Tree names to add
    tree_names = ['Neem Tree', 'Mango Tree', 'Banyan Tree', 'Peepal Tree', 'Gulmohar Tree']
    
    # Store tree objects
    trees = []

    for name in tree_names:
        tree = Tree(name=name)
        db.session.add(tree)
        trees.append(tree)
    
    db.session.commit()  # Commit all trees first to get their IDs

    # Define common questions
    common_questions = [
        ('What color are the leaves?', 'Green', 'Yellow', 'Red', 'Brown'),
        ('Are there any flowers visible?', 'Yes', 'No', 'Few', 'Many'),
        ('Is the tree shedding leaves?', 'Yes', 'No', 'Partially', 'Cannot say'),
        ('Do you see any insects?', 'Yes', 'No', 'Few', 'Many'),
        ('What is the moisture condition around the tree?', 'Wet', 'Dry', 'Muddy', 'Normal'),
        ('How is the sunlight exposure?', 'Full Sun', 'Partial', 'Shade', 'Varies'),
        ('Is the tree trunk healthy?', 'Yes', 'No', 'Some damage', 'Cannot say'),
        ('Any signs of animal activity?', 'Birds', 'Insects', 'Squirrels', 'None'),
        ('Are there any new buds?', 'Yes', 'No', 'Few', 'Not sure'),
        ('Are there fallen fruits?', 'Yes', 'No', 'Some', 'Many')
    ]

    # Add same questions for each tree
    for tree in trees:
        for q_text, a, b, c, d in common_questions:
            question = Question(
                tree_id=tree.id,
                question_text=q_text,
                option_a=a,
                option_b=b,
                option_c=c,
                option_d=d
            )
            db.session.add(question)

    db.session.commit()
    print("Database initialized with multiple trees and common questions.")
