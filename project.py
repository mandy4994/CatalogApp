from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
app = Flask(__name__)


engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/categories/<int:category_id>/')
def CategoryMenu():
    category = session.query(Category).first()
    items = session.query(Item).filter_by(category_id=category.id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'
    return output

# Route for new category item function

@app.route('/category/<int:category_id>/new')
def newCategoryItem(category_id):
	return "page to create a new item!"
# Route for edit category item function
@app.route('/category/<int:category_id>/<int:item_id>/edit')
def editCategoryItem(category_id, item_id):
	return "page to edit item!"
# Route for deleting category item function
@app.route('/category/<int:category_id>/<int:item_id>/delete')
def deleteCategoryItem(category_id, item_id):
	return "page to delete an item!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
