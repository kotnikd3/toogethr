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
businessLogic = BusinessLogic()

@app.route('/users/<int:userid>/reservations', methods=["GET"])
def getReservationForUser(userid):
    """
    Get all the reservations for user (status 200).
    Check and return for errors: user not exist (status 404).
    """
    try:
        if businessLogic.userExist(userid):
            reservations = businessLogic.getReservationByUser(userid)
            # OK
            return Response(response = reservations, status = 200, content_type = "application/json")
        else:
            # No user found
            return Response(response = json.dumps({"message": "User not found"}), status = 404, content_type = "application/json")
    except Exception as err:
        return Response(response = json.dumps({"message": "Server error: {0}".format(err)}), status = 500, content_type = "application/json")


@app.route('/parkingspots', methods=["GET"])
def getParkingSpotsWithReservations():
    """
    Get all the reservations for all the parking spots.
    """
    try:
        parkingSpotsInfo = businessLogic.getParkingSpotsWithReservations()
        # OK
        return Response(response = parkingSpotsInfo, status = 200, content_type = "application/json")
    except Exception as err:
        return Response(response = json.dumps({"message": "Server error: {0}".format(err)}), status = 500, content_type = "application/json")

@app.route('/parkingspots/<int:parkingspotid>/reservations', methods=["GET"])
def getReservationsForParkingSpot(parkingspotid):
    """
    Get all the reservations for specific parking spot.
    """
    try:
        reservationsForParkingSpot = businessLogic.getReservationsForParkingSpot(parkingspotid)
        # OK
        return Response(response = reservationsForParkingSpot, status = 200, content_type = "application/json")
    except Exception as err:
        return Response(response = json.dumps({"message": "Server error: {0}".format(err)}), status = 500, content_type = "application/json")


@app.route('/reservations/<int:reservationid>', methods=["GET"])
def getReservation(reservationid):
    """
    Returns the body containing booked reservation (status 200).
    Check and return for errors: reservation not found (status 404).
    """
    try:
        reservation = businessLogic.getReservation(reservationid)
        if not reservation is None:
            # OK
            return Response(response = reservation, status = 200, content_type = "application/json")
        else:
            # Reservation not found
            return Response(response = json.dumps({"message": "Reservation not found"}), status = 404, content_type = "application/json")
    except Exception as err:
        return Response(response = json.dumps({"message": "Server error: {0}".format(err)}), status = 500, content_type = "application/json")


@app.route('/reservations', methods=["POST"])
def insertReservation():
    """
    Returns http status 302 with the Location header containing the url of newly booked reservation.
    Check and return for errors: missing or wrong data (status 400), parking spot not available at time (status 400).
    """
    try:
        reservationJSON = request.get_json()
        print(reservationJSON)
        # Check if user and parking spot exist and if input data is OK
        if(businessLogic.insertReservationRequestValid(reservationJSON)):
            # Check if parking spot is free at time
            if(businessLogic.isAvailable(reservationJSON)):
                newId = businessLogic.insertReservation(reservationJSON)
                #OK
                return Response(response = json.dumps({"message": "Reservation created with ID: "+str(newId)}), headers = {"Location": "/reservations/"+str(newId)}, status = 302, content_type = "application/json")
            else:
                # Parking spot is not available at time
                return Response(response = json.dumps({"message": "Bad request. Time for reservation is not available."}), status = 400, content_type = "application/json")
        else:
            # Wrong or missing input data
            return Response(response = json.dumps({"message": "Bad request."}), status = 400, content_type = "application/json")
    except Exception as err:
        return Response(response = json.dumps({"message": "Server error: {0}".format(err)}), status = 500, content_type = "application/json")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')