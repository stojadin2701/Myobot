/*var command_map = { 
    'fingers_spread':1,
    'wave_in':2,
    'wave_out':3,
    'fist':4,
    'double_tap':5,
    'fingers_spread_off':6,
    'wave_in_off':7,
    'wave_out_off':8,
    'fist_off':9,
    'double_tap_off':10
}
*/

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

function pose_handle(req) {
	var elem = document.getElementById('pose')
	elem.firstChild.data = req.responseText
}

function distance_handle(req) {
	var elem = document.getElementById('distance')
	elem.firstChild.data = req.responseText
}

$('#start_stream').on('click', function(event) {
    console.log("Start stream clicked...");
    xml_http_post("index.html", 'Start stream', pose_handle);
});

$('#stop_stream').on('click', function(event) {
    console.log("Stop stream clicked...");
    xml_http_post("index.html", 'Stop stream', pose_handle);
});

Myo.connect('test.test.test');

Myo.on('connected', function(data, timestamp){
    console.log("Myo successfully connected. Data: " + JSON.stringify(data) + ". Timestamp: " + timestamp + ".");
    xml_http_post("index.html", 'Armband connected', pose_handle);
    Myo.setLockingPolicy("none");
})

Myo.on('disconnected', function(){
    console.log("Myo disconnected.");
    xml_http_post("index.html", 'Armband disconnected', pose_handle);
})

Myo.on('pose', function(pose){
	console.log(pose);
	xml_http_post("index.html", pose, pose_handle);
})

Myo.on('pose_off', function(pose){
	console.log('kraj poze' + pose);
    xml_http_post("index.html", pose + '_off', pose_handle);
});

Myo.on('locked', function(){
	console.log('zakljucan myo');
    xml_http_post("index.html", 'Armband locked', pose_handle);
});

Myo.on('unlocked', function(){
	console.log('otkljucan myo');
    xml_http_post("index.html", 'Armband unlocked', pose_handle);
});
