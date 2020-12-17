from flask import Flask
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
# # A secret key is required to use CSRF

# CSRF protection requires a secret key 
# to securely sign the token. 
# By default this will use 
# the Flask app's SECRET_KEY . 

app.config['SECRET_KEY'] = '323b22caac41acbf'
app.config['SQLALCHEMY'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from flaskinventory import routes

db.create_all()
db.session.commit()


# if __name__ == '__main__':
    
#     app.run()


    # Object Relational Mapper (ORM) 
    # tool that translates Python classes to 
    # tables on relational databases
    #  and automatically converts function calls to SQL statements.