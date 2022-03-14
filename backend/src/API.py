"""
Python challenge.
Author: Denis Kotnik, May 2021
"""

# Frameworks
from flask import Flask, request, Response, json
from flask_cors import CORS
# Other
from service.BusinessLogic import BusinessLogic


app = Flask(__name__)
CORS(app)
business_logic = BusinessLogic()


@app.route('/users/<int:user_id>/reservations', methods=["GET"])
def get_reservation_for_user(user_id):
    """
    Get all the reservations for user (status 200).
    Check and return for errors: user not exist (status 404).
    """
    try:
        if business_logic.user_exist(user_id):
            reservations = business_logic.get_reservation_by_user(user_id)
            # OK
            return Response(
                response=reservations,
                status=200,
                content_type='application/json',
            )
        else:
            # No user found
            return Response(
                response=json.dumps({'message': 'User not found'}),
                status=404,
                content_type='application/json',
            )
    except Exception as err:
        return Response(
            response=json.dumps({'message': 'Server error: {0}'.format(err)}),
            status=500,
            content_type='application/json',
        )


@app.route('/parkingspots', methods=["GET"])
def get_parking_spots_with_reservations():
    """
    Get all the reservations for all the parking spots.
    """
    try:
        parking_spots_info = business_logic.get_parking_spots_with_reservations()
        # OK
        return Response(
            response=parking_spots_info,
            status=200,
            content_type='application/json'
        )
    except Exception as err:
        return Response(
            response=json.dumps({'message': 'Server error: {0}'.format(err)}),
            status=500,
            content_type='application/json'
        )


@app.route('/parkingspots/<int:parking_spot_id>/reservations', methods=["GET"])
def get_reservations_for_parking_spot(parking_spot_id):
    """
    Get all the reservations for specific parking spot.
    """
    try:
        reservations_for_parking_spot = business_logic.get_reservations_for_parking_spot(
            parking_spot_id
        )
        # OK
        return Response(
            response=reservations_for_parking_spot,
            status=200,
            content_type='application/json'
        )
    except Exception as err:
        return Response(
            response=json.dumps({'message': 'Server error: {0}'.format(err)}),
            status=500,
            content_type='application/json'
        )


@app.route('/reservations/<int:reservation_id>', methods=["GET"])
def get_reservation(reservation_id):
    """
    Returns the body containing booked reservation (status 200).
    Check and return for errors: reservation not found (status 404).
    """
    try:
        reservation = business_logic.get_reservation(reservation_id)
        if reservation is not None:
            # OK
            return Response(
                response=reservation,
                status=200,
                content_type='application/json'
            )
        else:
            # Reservation not found
            return Response(
                response=json.dumps({'message': 'Reservation not found'}),
                status=404,
                content_type='application/json'
            )
    except Exception as err:
        return Response(
            response=json.dumps({'message': 'Server error: {0}'.format(err)}),
            status=500,
            content_type='application/json'
        )


@app.route('/reservations', methods=["POST"])
def insert_reservation():
    """
    Returns http status 302 with the Location header containing the url of
    newly booked reservation. Check and return for errors: missing or wrong
    data (status 400), parking spot not available at time (status 400).
    """
    try:
        reservation_json = request.get_json()
        print(reservation_json)
        # Check if user and parking spot exist and if input data is OK
        if business_logic.insert_reservation_request_valid(reservation_json):
            # Check if parking spot is free at time
            if business_logic.is_available(reservation_json):
                new_id = business_logic.insert_reservation(reservation_json)
                # OK
                return Response(
                    response=json.dumps(
                        {'message': 'Reservation created with ID: '+str(new_id)}
                    ),
                    headers={'Location': '/reservations/'+str(new_id)},
                    status=302,
                    content_type='application/json'
                )
            else:
                # Parking spot is not available at time
                return Response(
                    response=json.dumps(
                        {'message': 'Bad request. '
                                    'Time for reservation is not available.'}
                    ),
                    status=400,
                    content_type='application/json'
                )
        else:
            # Wrong or missing input data
            return Response(
                response=json.dumps({'message': 'Bad request.'}),
                status=400,
                content_type='application/json'
            )
    except Exception as err:
        return Response(
            response=json.dumps({'message': 'Server error: {0}'.format(err)}),
            status=500,
            content_type='application/json'
        )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
