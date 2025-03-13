from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

# contains definitions of tables and associated schema constructs
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

# create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# define a model class by inheriting from db.Model.
class Hotel(db.Model, SerializerMixin):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # 1-to-Many Relationship data - 1 Hotel has many Customers
    # db.relationships aren't columns... but gives us a way to access associated data** 
    # "hotel" is the other side of the relationship to a review
    # if we want to automatically have a hotel delete its reviews when it's deleted, cascade will take care of that
    reviews = db.relationship('Review', back_populates='hotel', cascade ='all')

    # The many-to-many relationship data - the 1 Hotel has many Customers side of the relationship
    #**missed what the first two things passed into association_proxy are** 
    # a review instance is going to have a customer variable
    # "creator=lambda c:Review(customer=c)" is how are these things added to the list --- "c" is just a parameter (stands for customer)
    customers = association_proxy('reviews', 'customer', creator=lambda c:Review(customer=c))

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    # The 1-to-Many relationship data - 1 Customer has many Reviews
    # the cascade will delete the reviews for that customer if the customer is deleted
    reviews = db.relationship('Review', back_populates='customer', cascade='all')

    # The 1-to-Many relationship data - 1 Customer has many Hotels
    # second argument is what we're trying to fill in (i.e., hotels)
    hotels = association_proxy('reviews', 'hotel', creator=lambda h: Review(hotel=h))

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    text = db.Column(db.String)

    # Makes the database look in a particular table in a specific column for a specific id:
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    # Without foreign key you can't have relationships between tables
    # Foreign key data type must be the same as the data type of that table's id's data type (so integer)

    # reviews is the other side of the relationship for a hotel
    # "reviews" is the variable that references the reviews (not the table name reviews)
    hotel = db.relationship('Hotel', back_populates='reviews')
    customer = db.relationship('Customer', back_populates='reviews')
