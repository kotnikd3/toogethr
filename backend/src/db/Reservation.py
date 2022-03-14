class Reservation:
    def __init__(
        self,
        _id,
        datetime_from,
        datetime_to,
        user_id,
        parking_spot_id,
    ):
        self.id = _id
        self.datetime_from = datetime_from
        self.datetime_to = datetime_to
        self.user_id = user_id
        self.parking_spot_id = parking_spot_id
