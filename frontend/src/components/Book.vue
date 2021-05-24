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
                        <input type="text" class="form-control" v-model="userId" placeholder="1"/>
                    </div>
                    <div class="form-group">
                        <label>Parking spot ID:</label>
                        <input type="text" class="form-control" v-model="parkingSpotId" placeholder="1"/>
                    </div>
                    <div class="form-group">
                        <label>From:</label>
                        <input type="text" class="form-control" v-model="dateTimeFrom" placeholder="10/15/2021 9:00"/>
                    </div>
                    <div class="form-group">
                        <label>To:</label>
                        <input type="text" class="form-control" v-model="dateTimeTo" placeholder="10/15/2021 9:00"/>
                    </div>
                    <br>
                    <input type="submit" class="btn btn-success" value="Book reservation"/>
                    <div v-if="alertVisible" :class="alertColor" role="alert">{{ alertMessage }}</div>
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
            userId: null,
            parkingSpotId: null,
            dateTimeFrom: null,
            dateTimeTo: null,
            alertVisible: false,
            alertMessage: '',
            alertColor: ''
        }
    },
    methods: {
        bookReservation() {
            this.axios.post('http://localhost:5000/reservations', {
                'userId' : parseInt(this.userId),
                'parkingSpotId' : parseInt(this.parkingSpotId),
                'dateTimeFrom' : moment(this.dateTimeFrom).unix(),
                'dateTimeTo' : moment(this.dateTimeTo).unix()
            })
            .then(response => {
                if (response.status == 200) {
                    this.alertMessage = "Booked reservation with ID " + response.data.data.id;
                    this.alertColor = "alert alert-success";
                    this.alertVisible = true;
                }
            })
            .catch(error => {
                console.error("Error:", error);
                this.alertMessage = error.response.data.message;
                this.alertColor = "alert alert-danger";
                this.alertVisible = true;
            });
        }
    }
}
</script>