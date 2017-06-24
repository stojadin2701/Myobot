var pose_map = {
	'fingers_spread':'forward',
	'fist':'backward',
	'wave_in':'left',
	'wave_out':'right',
}

var key_map = {
	'w':'forward',
	's':'backward',
	'a':'left',
	'd':'right'
}

var myo_control = false;

var right_sidebar_opened = false;

var last_event = null;
  
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
	$('#pose').html = req.responseText;
}

function distance_handle(req) {
	document.getElementById("distance_info").innerHTML = req.responseText + " cm";
    //$('#distance_info').html = req.responseText + " cm";
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
	$('#input-toggle').bootstrapToggle('enable');
    console.log("Myo successfully connected. Data: " + JSON.stringify(data) + ". Timestamp: " + timestamp + ".");
    xml_http_post("index.html", 'armband_connected', pose_handle);
    Myo.setLockingPolicy("none");
})

Myo.on('disconnected', function(){
	$('#input-toggle').bootstrapToggle('on');
	$('#input-toggle').bootstrapToggle('disable');
    console.log("Myo disconnected.");
    xml_http_post("index.html", 'armband_disconnected', pose_handle);
	xml_http_post("index.html", 'stop', pose_handle);
})

Myo.on('pose', function(pose){
    console.log(pose);
	if(myo_control && (pose in pose_map)) {
			xml_http_post("index.html", pose_map[pose], pose_handle);
	}
    
})

Myo.on('pose_off', function(pose){
    console.log('kraj poze' + pose);
	if(myo_control && (pose in pose_map)){
		xml_http_post("index.html", 'stop', pose_handle);
	}
});

Myo.on('locked', function(){
    console.log('myo zakljucan');
    xml_http_post("index.html", 'armband_locked', pose_handle);
});

Myo.on('unlocked', function(){
    console.log('myo otkljucan');
    xml_http_post("index.html", 'armband_unlocked', pose_handle);
});

Myo.on('arm_synced', function(){
	xml_http_post("index.html", 'armband_synced', pose_handle);
});

Myo.on('arm_unsynced', function(){
	xml_http_post("index.html", 'armband_unsynced', pose_handle);
});

$('#start_stream').on('click', function(event) {
    $('#start_stream').hide();
    $('#camera').show();
    $('#stop_stream').show();
    console.log("Start stream clicked...")
    xml_http_post("index.html", 'start_stream', pose_handle);
});

$('#stop_stream').on('click', function(event) {
    $('#stop_stream').hide();
    $('#camera').hide();
    $('#start_stream').show();
    console.log("Stop stream clicked...")
    xml_http_post("index.html", 'stop_stream', pose_handle);
});

$(function() {
    $('#input-toggle').bootstrapToggle();
	$('#input-toggle').bootstrapToggle('disable');	
	$('#input-toggle').change(function() {
		xml_http_post("index.html", 'stop', pose_handle);
		myo_control = !$(this).prop('checked');     
    })
	
	/*
	$('#input-toggle-two').bootstrapToggle({
      on: 'Keyboard',
      off: 'Myo'
    });
	*/
})

/*
$(function() {
    var $checkbox = '<input type="checkbox" checked="checked" data-toggle="toggle" data-on="Keyboard" data-off="Myo" data-onstyle="warning" data-offstyle="info" />'
    $('.toggle-placeholder').html($checkbox);
    $('.toggle-placeholder').find('input[type=checkbox][data-toggle=toggle]')
                            .each(function(){
        $(this).bootstrapToggle();
    });
});
*/

document.addEventListener('keydown', (event) => {
	if(last_event && last_event.key === event.key) return;
	last_event = event;
	
	const key_name = event.key;
	if(!myo_control && (key_name === 'w' || key_name === 's' || key_name === 'a' || key_name === 'd')){
		xml_http_post("index.html", key_map[key_name], pose_handle);
		switch(key_name) {
		case 'w':
			console.log('forward');
			break;
		case 's':
			console.log('backward');
			break;
		case 'a':
			console.log('left');
			break;
		case 'd':
			console.log('right');
			break;
		}  
	}  
}, false);

$(document).ready(function () {
	$('#left_sidebar').BootSideMenu({
		side: "left",
		pushBody: false,
		remember: false,
		autoClose: true
	});
	
	$('#right_sidebar').BootSideMenu({
		side: "right",
		pushBody: false,
		remember: false,
		autoClose: true,
		onOpen: function(){
			right_sidebar_opened = true;
		},
		onClose: function(){
			right_sidebar_opened = false;
		}
	});
});

document.addEventListener('keyup', (event) => {
	last_event = null;
	const key_name = event.key;
	
	if((!myo_control && (key_name === 'w' || key_name === 's' || key_name === 'a' || key_name === 'd')) || key_name === ' '){
		xml_http_post("index.html", 'stop', pose_handle);
		console.log('Halt');
	}
	
}, false);


window.setInterval(function(){
	if(right_sidebar_opened == true && $('#distance_list').attr('aria-expanded') == "true"){
		console.log("Requesting distance");
		xml_http_post("index.html", 'distance_request', distance_handle);
	}
}, 500);
