<template>
    <div class="container">
        <h1>Reservations</h1>
        <table class="table table-hover">
            <thead>
            <tr>
                <td>ID</td>
                <td>From</td>
                <td>To</td>
                <td>User ID</td>
                <td>Parking spot ID</td>
            </tr>
            </thead>

            <tbody>
                <tr v-for="reservation in reservations" :key="reservation.id">
                    <td>{{ reservation.id }}</td>
                    <td>{{ reservation.datetime_from | humanDateTime }}</td>
                    <td>{{ reservation.datetime_to | humanDateTime }}</td>
                    <td>{{ reservation.user_id }}</td>
                    <td>{{ reservation.parking_spot_id }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import moment from 'moment/moment';

export default{
    data(){
        return{
            reservations: []
        }
    },
    created: function(){
        if (this.$route.params.id) {
            this.getItem();
        }
    },
    methods: {
        getItem() {
            this.axios.get('http://localhost:5000/parkingspots/' + this.$route.params.id + '/reservations')
            .then(response => {
                this.reservations = response.data.data;
            })
            .catch(error => {
                this.error = error.response;
                console.error("Error:", error);
            });
        }
    },
    filters: {
        humanDateTime(epoch) {
            return moment.unix(epoch).format('LLLL')
        }
    }
}
</script>