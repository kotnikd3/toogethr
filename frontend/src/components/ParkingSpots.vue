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
                <tr v-for="parking_spot in parking_spots" :key="parking_spot.id">
                    <td>{{ parking_spot.id }}</td>
                    <td>{{ parking_spot.latitude }}</td>
                    <td>{{ parking_spot.longitude }}</td>
                    <td><router-link :to="{name: 'Reservations', params: { id: parking_spot.id }}" class="btn btn-primary">Check availability</router-link></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    data(){
        return{
            parking_spots: []
        }
    },
    created: function() {
        this.fetchItems();
    },
    methods: {
        fetchItems() {
            this.axios.get('http://localhost:5000/parkingspots')
            .then(response => {
                this.parking_spots = response.data.data;
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }
}
</script>