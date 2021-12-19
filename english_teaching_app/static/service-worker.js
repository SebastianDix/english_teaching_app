const CACHE_NAME = 'static-cache';

const FILES_TO_CACHE = [
	'/static/offline.html',
];

self.addEventListener('install', (evt) => {
	console.log('[ServiceWorker] Install');
	self.skipWaiting();
});

self.addEventListener('activate', (evt) => {
	console.log('[ServiceWorker] Activate');
});

// Sending and receiving data in JSON format using POST method
// Example POST method implementation:
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
	return //response.json(); // parses JSON response into native JavaScript objects
}


function syncAnalWrapper(){
	var request = indexedDB.open("localforage", 3); // first step is opening the database
	request.onsuccess = function(e) {
		var db =  e.target.result;
		var trans = db.transaction(["keyvaluepairs"], 'readwrite'); //second step is opening the object store
		var store = trans.objectStore("keyvaluepairs");

		var request = store.get('analysis'); //getting single object by id from object store

		request.onsuccess = function(e) {
			let analysis = request.result
			console.log("REQUEST SUCCESS")
			console.log(analysis)
			// if (analysis === {}){console.log("Empty object [[[ SERVICE WORKER ]]] " + analysis)}
			// if (analysis === ""){console.log("Empty string[[[ SERVICE WORKER ]]] " + analysis)}
			// if (analysis === false){console.log("False analysis[[[ SERVICE WORKER ]]] " + analysis)}
			// if (analysis === undefined){console.log("Undefined analysis[[[ SERVICE WORKER ]]] " + analysis)}
			// if (analysis === null){console.log("Null analysis[[[ SERVICE WORKER ]]] " + analysis)}

			postData('lessons/sync_feedback', analysis)
			db.close();
		};

		request.onerror = function(e) {
			console.log("[[[ SERVICE WORKER ]]] Error Getting: ", e);
		};
	};
}

self.addEventListener('sync', function(event) {
	if (event.tag == 'example-tag') {
		event.waitUntil(syncAnalWrapper());
		console.log("synced")
	}
});
