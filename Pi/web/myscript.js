
function xml_http_post(url, data, callback) {
	var req = false;
	try {
		// Firefox, Opera 8.0+, Safari
		req = new XMLHttpRequest();
	}
	catch (e) {
		// Internet Explorer
		try {
			req = new ActiveXObject("Msxml2.XMLHTTP");
		}
		catch (e) {
			try {
				req = new ActiveXObject("Microsoft.XMLHTTP");
			}
			catch (e) {
				alert("Your browser does not support AJAX!");
				return false;
			}
		}
	}
	req.open("POST", url, true);
	req.onreadystatechange = function() {
		if (req.readyState == 4) {
			callback(req);
		}
	}
	req.send(data);
}

function test_handle(req) {
	var elem = document.getElementById('pose')
		elem.innerHTML =  req.responseText
}



Myo.connect('test.test.test');

Myo.on('connected', function(data, timestamp){
	console.log("Myo successfully connected. Data: " + JSON.stringify(data) + ". Timestamp: " + timestamp + ".");
    xml_http_post("index.html", 'Armband connected', test_handle);
})


//Whenever we get a pose event, we'll update the image sources with the active version of the image
Myo.on('pose', function(pose){
	console.log(pose);
	xml_http_post("index.html", pose, test_handle);
})

//Opposite of above. We also revert the main img to the unlocked state
Myo.on('pose_off', function(pose){
	console.log('kraj poze' + pose);
    xml_http_post("index.html", pose, test_handle);
});


//Whenever a myo locks we'll switch the main image to a lock image
Myo.on('locked', function(){
	console.log('zakljucan myo');
});

//Whenever a myo unlocks we'll switch the main image to a unlock image
Myo.on('unlocked', function(){
	console.log('otkljucan myo');
});
