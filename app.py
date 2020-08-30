from flask_restful import Resource, Api
from resource.events import *
from resource.register import *

app = Flask(__name__)
api = Api(app)

## API endpoints of events management
api.add_resource(Event, '/event/<string:event_id>')
api.add_resource(EventList, '/events')

## API endpoints of user view
api.add_resource(RegisteredUser, '/user/<string:user_mail>')
## API endpoints of event register
api.add_resource(Register, '/register/<string:event_id>')
## API endpoints of register delete
api.add_resource(DeleteRegister, '/delete/')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
