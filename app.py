import uuid
import json
from flask import Flask, request
from flask_cors import cross_origin
from marshmallow import Schema, fields, pprint, ValidationError

app = Flask(__name__)

class ReportSchema(Schema):
    username = fields.Str(
        required=True,
        error_messages={"required": {"message": "Username required", "code": 400}}
    )
    report = fields.Str(
        required=True,
        error_messages={"required": {"message": "Report text required", "code": 400}}
    )

reportSchema = ReportSchema()

@app.route('/report', methods=['POST'])
@cross_origin()
def saveReport():
    try:
        data = reportSchema.load(json.loads(request.data))

        report = data['report']
        username = data['username']

        # .. Process and persist data

        return {
            'report_id': str(uuid.uuid4()),
            'report': report + '__PROCESSED__',
            'username': username
        }
    except ValidationError as err:
        pprint(err.messages)
        return err.messages, 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
