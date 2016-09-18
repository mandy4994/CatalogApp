from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item

engine = create_engine('sqlite:///catalogapp.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
restaurant1 = Category(name="Food")

session.add(restaurant1)
session.commit()

menuItem2 = Item(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$7.50", category=restaurant1)

session.add(menuItem2)
session.commit()


menuItem1 = Item(name="French Fries", description="with garlic and parmesan",
                     price="$2.99", category=restaurant1)

session.add(menuItem1)
session.commit()



print "added menu items!"
