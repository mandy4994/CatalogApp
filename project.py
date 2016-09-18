from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
app = Flask(__name__)


engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def categoryMenu(category_id):
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

@app.route('/categories/<int:category_id>/')
def categoryMenu(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return render_template('index.html', category=category, items=items)

# Route for new category item function


@app.route('/category/<int:category_id>/new', methods=['GET', 'POST'])
def newCategoryItem(category_id):
	if request.method == 'POST':
		print "In post method"
		newItem = Item(name=request.form['name'], category_id=category_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('categoryMenu', category_id=category_id))
	else:
		return render_template('newmenuitem.html', category_id=category_id)
# Route for edit category item function
@app.route('/category/<int:category_id>/<int:itemID>/edit', methods=['GET', 'POST'])
def editCategoryItem(category_id, itemID):
	editedItem = session.query(Item).filter_by(id = itemID).one()
	if request.method == 'POST':
		print "Inside Post"
		if request.form['name']:
			editedItem.name = request.form['name']
			session.add(editedItem)
			session.commit()
			return redirect(url_for('categoryMenu', category_id = category_id))
	else:
		print "inside else"
		return render_template('editmenuitem.html', category_id=category_id, itemID=itemID, item = editedItem)
# Route for deleting category item function
@app.route('/category/<int:category_id>/<int:item_id>/delete')
def deleteCategoryItem(category_id, item_id):
	return "page to delete an item!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
