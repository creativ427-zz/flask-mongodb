from flask import Flask
from flask_restful import Resource,Api,reqparse,abort,fields,marshal_with
from flask_mongoengine import MongoEngine

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'db':'school',
    'host':'localhost',
    'port': 27017
}
db = MongoEngine()
db.__init__(app)

class School(db.Document):
    _id = db.IntField()
    name = db.StringField(required=True)
    email = db.StringField(required=True)

student_post_args = reqparse.RequestParser()
student_post_args.add_argument("name", type=str, help="name required", required=True)
student_post_args.add_argument("email", type=str, help="email required", required=True)

student_put_args = reqparse.RequestParser()
student_put_args.add_argument("name", type=str)
student_put_args.add_argument("email", type=str)

resource_fields = {
"_id" : fields.Integer,
"name" : fields.String,
"email" : fields.String,
}


'''
class Students(Resource):
    def get(self):
        students = School.objects.get().all()
        return students
'''

class Student(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        student = School.objects.get(_id=id)
        if not student:
            abort(404, message="no such student")
        return student
    
    @marshal_with(resource_fields)
    def post(self,id):
        args = student_post_args.parse_args()
        student= School(_id=id,name=args["name"],email=args["email"]).save()
        return student, 201

    @marshal_with(resource_fields)
    def put(self,id):
        args = student_put_args.parse_args()
        if args["name"]:
            School.objects.get(_id=id).update(name=args["name"])
        if args["email"]:
            School.objects.get(_id=id).update(email=args["email"])
        return f" Student {id} updated",200

    def delete(self,id):
        School.objects.get(_id=id).delete()
        return students

    
#api.add_resource(Students, '/students') 
api.add_resource(Student,'/students/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)