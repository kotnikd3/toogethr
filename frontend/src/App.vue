<template>
	<div id="app" class="container">
		<nav class="navbar navbar-expand-sm bg-light">
			<a class="navbar-brand" href="https://toogethr.com">
				<img src="./assets/toogethr_logo.svg" alt="Logo" style="width:60px;">
			</a>
			<ul class="navbar-nav">
				<li class="nav-item">
					<router-link :to="{ name: 'ParkingSpots' }" class="nav-link">Parking spots</router-link>
				</li>
				<li class="nav-item">
					<router-link :to="{ name: 'Book' }" class="btn btn-outline-success my-2 my-sm-0" tag="button">Book</router-link>
				</li>
			</ul>
		</nav>
		<transition name="fade">
		<div class="gap">
			<router-view></router-view>        
		</div>
		</transition>
	</div>
</template>

<script>
export default {
}
</script>

<style>
    .fade-enter-active, .fade-leave-active {
      transition: opacity .5s
    }
    .fade-enter, .fade-leave-active {
      opacity: 0
    }
    .gap {
      margin-top: 50px;
    }
</style>