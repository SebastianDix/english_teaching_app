$(document).ready(function() {
	// https://www.flaskpwa.com/#_backgroundsync
	/*
		ask for hash
		check if we have a hash for mongo saved
		if we don't, save this hash
		if we do, get our hash and compare it with the new one
		if there are changes, fetch the database
		if there are no changes or if we are offline, just fetch shit from localforage

*/
	// var store = localforage.createInstance({
	// 	name: "lessonObjects"
	// });

	// console.log(store.getItem("testing"))
	// var store = localforage.createInstance({
	// 	name: "lessonObjects"
	// });
	// console.log(store.getItem("testing"))

	// // Setting the key on one of these doesn't affect the other.
	// store.setItem("key", "value");
	// otherStore.setItem("key", "value2");
	$("#lessons").on('click','span.starcontainer',function(e){
		e.stopPropagation()	
		let svg = $(this).find('svg')
		// svg.find('g path').css('fill','red')
		let lesson_id = $(this).parent().attr('data-id')
		// let classes = svg.attr('class')
		if (svg.hasClass("staractive")){
			svg.removeClass().addClass("starinactive")
		} 
		else if (svg.hasClass("starinactive")){
			svg.removeClass().addClass("staractive")
		}

		// This will be available under request.form, not request.data
		$.ajax({
			type: "POST",
			url: $SCRIPT_ROOT + '/lessons/favorite',
			data: {lesson_id:lesson_id}
		});
	})	

	$("#lessons").on('click','div.lesson_row',function(e){
		let lesson_id = $(this).attr("data-id")
		window.location.href = $SCRIPT_ROOT + '/lessons/view_feedback/' + lesson_id
	})

	// var swRegistration = null;
	// if ('serviceWorker' in navigator) {
	// 	navigator.serviceWorker
	// 		.register('/service-worker.js')
	// 		.then(function(registration) {
	// 			console.log('Service Worker Registered!');
	// 			swRegistration = registration;
	// 			console.log(swRegistration)
	// 			return registration;
	// 		})
	// 		.catch(function(err) {
	// 			console.error('Unable to register service worker.', err);
	// 		});
	// }
	// const requestNotificationPermission = async () => {
	// 	const permission = await window.Notification.requestPermission();
	// 	// value of permission can be 'granted', 'default', 'denied'
	// 	// granted: user has accepted the request
	// 	// default: user has dismissed the notification permission popup by clicking on x
	// 	// denied: user has denied the request.
	// 	if(permission !== 'granted'){
	// 		throw new Error('Permission not granted for Notification');
	// 	}
	// }
	// const permission = requestNotificationPermission();

	$('div.content .flaskmessage').delay(5000).fadeOut('slow');


	$('#write_all').on('keyup',function(event){
		let value = $(this).val()
		let date = new Date()
		year = date.getFullYear();
		month = date.getMonth() + 1;
		day = date.getDate();
		hours = date.getHours();
		minutes = date.getMinutes();
		seconds = date.getSeconds();
		date = year + "_" + month + "_" + day + "_" + hours + "_" + minutes;
		key = "SebastianAnalysis" + "_" + date
		localforage.setItem(key,value)
		if (event.which === 13){
			requestSync()
		}
	})



} );
function searchLessons(){
	// Declare variables
	var input,filter,table,tr,td,i,txtValue;
	input = document.getElementById("lessonSearchBar");
	table = document.getElementById("lessons")
	filter = input.value.toUpperCase();
	tr = table.getElementsByTagName("div");

	// Loop through tall the table rows, and hide those which don't match the search query
	for (i = 0; i < tr.length; i++) {
		td = tr[i].getElementsByTagName("div")[2];
		console.log(td)
		if (td) {
			txtValue = td.textContent || td.innerText;
			if (txtValue.toUpperCase().indexOf(filter) > -1){
				tr[i].style.display = "";
				// enableDiv.classList.remove("table-striped")
			} else {
				tr[i].style.display = "none"
			}
		}
	}
}
async function postData(url = '', data = {}) {
	// Default options are marked with *
	const response = await fetch(url, {
		method: 'POST', // *GET, POST, PUT, DELETE, etc.
		mode: 'cors', // no-cors, *cors, same-origin
		cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
		credentials: 'same-origin', // include, *same-origin, omit
		headers: {
			'Content-Type': 'application/json'
			// 'Content-Type': 'application/x-www-form-urlencoded',
		},
		redirect: 'follow', // manual, *follow, error
		referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
		body: JSON.stringify(data) // body data type must match "Content-Type" header
	});
	console.log(response)
	return //response.json(); // parses JSON response into native JavaScript objects
}
function requestSync(){
	console.log("requestSync in main.js called")
	var message = {
		text : $('#write_all').val(),
		lesson_id : $('#write_all').attr('data-lessonid'),
		topics : $('#topics').val()
	};

	localforage.setItem('analysis',message).then(function(value){console.log(value);})
	// if ('serviceWorker' in navigator) {
	// 	navigator.serviceWorker.ready.then(function(swRegistration) {
	// 		return swRegistration.sync.register('example-tag');
	// 	});
	// } else {
	postData(url = $SCRIPT_ROOT + '/lessons/sync_feedback', data=message)

	// }
}


function syncAnalysis(){
	// triggered by the button in edit_feedback
	let text = $('#write_all').val()
	let lesson_id = $('#write_all').attr('data-lessonid')
	let topics = $('#topics').val()
	$.ajax({
		type: "POST",
		url: $SCRIPT_ROOT + '/lessons/sync_feedback',
		data: {lesson_id: lesson_id, text: text, topics: topics}
	});
}




