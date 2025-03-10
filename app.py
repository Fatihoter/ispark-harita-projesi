from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from geoalchemy2 import Geometry
from sqlalchemy import func
import requests
import locale

locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Tarik.2712@localhost:5432/ispark'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# İSPARK API URL'leri
ISPARK_LIST_URL = 'https://api.ibb.gov.tr/ispark/Park'

class IsparkData(db.Model):
    __tablename__ = 'ispark_data'
    id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, unique=True, nullable=False)
    park_name = db.Column(db.String(), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    empty_capacity = db.Column(db.Integer, nullable=False)
    work_hours = db.Column(db.String(), nullable=False)
    park_type = db.Column(db.String(), nullable=False)
    free_time = db.Column(db.Integer, nullable=False)
    district = db.Column(db.String(), nullable=False)
    is_open = db.Column(db.Integer, nullable=False)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

@app.route('/fetch_and_store', methods=['GET'])
def fetch_and_store():
    response = requests.get(ISPARK_LIST_URL)
    parks = response.json()

    for park in parks:
        existing_park = IsparkData.query.filter_by(park_id=park['parkID']).first()
        geom = f'SRID=4326;POINT({park["lng"]} {park["lat"]})'
        if existing_park is None:
            new_park = IsparkData(
                park_id=park['parkID'],
                park_name=park['parkName'],
                latitude=float(park['lat']),
                longitude=float(park['lng']),
                capacity=park['capacity'],
                empty_capacity=park['emptyCapacity'],
                work_hours=park['workHours'],
                park_type=park['parkType'],
                free_time=park['freeTime'],
                district=park['district'],
                is_open=park['isOpen'],
                geom=geom
            )
            db.session.add(new_park)
        else:
            existing_park.park_name = park['parkName']
            existing_park.latitude = float(park['lat'])
            existing_park.longitude = float(park['lng'])
            existing_park.capacity = park['capacity']
            existing_park.empty_capacity = park['emptyCapacity']
            existing_park.work_hours = park['workHours']
            existing_park.park_type = park['parkType']
            existing_park.free_time = park['freeTime']
            existing_park.district = park['district']
            existing_park.is_open = park['isOpen']
            existing_park.geom = geom

    db.session.commit()
    return jsonify({'message': 'Data fetched and stored successfully'})

@app.route('/counties', methods=['GET'])
def get_counties():
    counties = db.session.query(IsparkData.district.distinct()).all()
    counties = [county[0] for county in counties]
    counties = sorted(counties, key=locale.strxfrm)
    return jsonify(counties)

@app.route('/data', methods=['GET'])
def get_data():
    county = request.args.get('county', '')
    park_name = request.args.get('parkName', '')

    query = db.session.query(
        IsparkData.park_id,
        IsparkData.park_name,
        IsparkData.latitude,
        IsparkData.longitude,
        IsparkData.capacity,
        IsparkData.empty_capacity,
        IsparkData.work_hours,
        IsparkData.park_type,
        IsparkData.free_time,
        IsparkData.district,
        IsparkData.is_open,
        func.ST_AsGeoJSON(IsparkData.geom).label('geom')
    )

    if county:
        query = query.filter(IsparkData.district == county)

    if park_name:
        query = query.filter(IsparkData.park_name.ilike(f'%{park_name}%'))

    data = query.all()

    result = []
    for park in data:
        geom = eval(park.geom)
        result.append({
            'ParkID': park.park_id,
            'ParkName': park.park_name,
            'Latitude': park.latitude,
            'Longitude': park.longitude,
            'Capacity': park.capacity,
            'EmptyCapacity': park.empty_capacity,
            'WorkHours': park.work_hours,
            'ParkType': park.park_type,
            'FreeTime': park.free_time,
            'District': park.district,
            'IsOpen': park.is_open,
            'geom': {
                'type': geom['type'],
                'coordinates': geom['coordinates']
            }
        })
    return jsonify(result)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/isparks')
def isparks_view():
    return render_template('isparks.html')

if __name__ == '__main__':
    app.run(debug=True)
