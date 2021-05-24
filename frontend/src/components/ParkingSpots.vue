<template>
    <div>
        <h1>Parking spots</h1>

        <table class="table table-hover">
            <thead>
            <tr>
                <td>ID</td>
                <td>Latitude</td>
                <td>Longitude</td>
                <td></td>
            </tr>
            </thead>

            <tbody>
                <tr v-for="parkingSpot in parkingSpots" :key="parkingSpot.id">
                    <td>{{ parkingSpot.id }}</td>
                    <td>{{ parkingSpot.latitude }}</td>
                    <td>{{ parkingSpot.longitude }}</td>
                    <td><router-link :to="{name: 'Reservations', params: { id: parkingSpot.id }}" class="btn btn-primary">Check availability</router-link></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    data(){
        return{
            parkingSpots: []
        }
    },
    created: function() {
        this.fetchItems();
    },
    methods: {
        fetchItems() {
            this.axios.get('http://localhost:5000/parkingspots')
            .then(response => {
                this.parkingSpots = response.data.data;
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }
}
</script>