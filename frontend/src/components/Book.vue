<template>
  <div class="container">
        <div class="card">
            <div class="card-header">
                <h3>Book reservation</h3>
            </div>
            <div class="card-body">
                <form v-on:submit.prevent="bookReservation">
                    <div class="form-group">
                        <label>User ID:</label>
                        <input type="text" class="form-control" v-model="user_id" placeholder="1"/>
                    </div>
                    <div class="form-group">
                        <label>Parking spot ID:</label>
                        <input type="text" class="form-control" v-model="parking_spot_id" placeholder="1"/>
                    </div>
                    <div class="form-group">
                        <label>From:</label>
                        <input type="text" class="form-control" v-model="datetime_from" placeholder="10/15/2021 9:00"/>
                    </div>
                    <div class="form-group">
                        <label>To:</label>
                        <input type="text" class="form-control" v-model="datetime_to" placeholder="10/15/2021 9:00"/>
                    </div>
                    <br>
                    <input type="submit" class="btn btn-success" value="Book reservation"/>
                    <div v-if="alert_visible" :class="alert_color" role="alert">{{ alert_message }}</div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import moment from 'moment/moment';
export default {
    data() {
        return {
            user_id: null,
            parking_spot_id: null,
            datetime_from: null,
            datetime_to: null,
            alert_visible: false,
            alert_message: '',
            alert_color: ''
        }
    },
    methods: {
        bookReservation() {
            this.axios.post('http://localhost:5000/reservations', {
                'user_id' : parseInt(this.user_id),
                'parking_spot_id' : parseInt(this.parking_spot_id),
                'datetime_from' : moment(this.datetime_from).unix(),
                'datetime_to' : moment(this.datetime_to).unix()
            })
            .then(response => {
                if (response.status == 200) {
                    this.alert_message = "Booked reservation with ID " + response.data.data.id;
                    this.alert_color = "alert alert-success";
                    this.alert_visible = true;
                }
            })
            .catch(error => {
                console.error("Error:", error);
                this.alert_message = error.response.data.message;
                this.alert_color = "alert alert-danger";
                this.alert_visible = true;
            });
        }
    }
}
</script>