const serverAddress = "http://127.0.0.1:5000";

document.addEventListener('DOMContentLoaded', function(){
	console.log("Loaded");
	var searchField = document.getElementById("search-term");
	//var select = document.getElementById("search-choose");
	var submit = document.getElementById("submit");
	submit.addEventListener("click", function(){
		var searchTerm = searchField.value.split(" ");
		//var selectedOption = select.options[select.selectedIndex].value;
		getVideoURL(function(vidurl){
		//window.alert(serverAddress + '/download?vidurl='+vidurl);
			$.ajax({
				type: 'POST',
				url: serverAddress + '/download',
				data: {vidurl: vidurl, searchParams: searchTerm.toString()},
				beforeSend: function(){
					var loader = document.getElementById("loader");
					var results_display = document.getElementById("results-display");
					loader.style.display = "block";
					results_display.style.display = "none";
				},
				success: function(result){
					var loader = document.getElementById("loader");
					var results_display = document.getElementById("results-display");
					loader.style.display = "none";
					results_display.style.display = "block";
					$.ajax({url: serverAddress+'/timestamps', success: function(result){
						var ul = document.getElementById("time-list");
						while (ul.firstChild) {
    						ul.removeChild(ul.firstChild);
						}
						timestamps = result.split(" ");
						if (timestamps.length>2){
							//window.alert(timestamps);
							for (var i = 1; i<timestamps.length; i++){
								var li = document.createElement("li");
								var a = document.createElement("a");
								var text = "";
								var timestamp = timestamps[i-1];
								if(timestamp.split(":").length > 2){
									timestamp = timestamps[i-1].slice(0, 8);
									text = timestamp;
									seconds = timeToNum(text);
									text = timestamp + "<span style='padding-left:15px;color:lightgray;font-size:14px;font-weight:600;'>(subtitles)</span>";
								}
								else {
									seconds = timestamp;
									timestamp = numToTime(seconds);
									text = timestamp + "<span style='padding-left:15px;color:lightgray;font-size:14px;font-weight:600;'>(video)</span>";
								}
								if (seconds != 0){
									a.setAttribute("href", vidurl.split("&t=").shift()+"&t="+seconds+"s");
									a.innerHTML = text;
									li.appendChild(a);
									ul.appendChild(li);
								}
								//alert(vidurl.split("&t=").shift());
							}
						} else{
							var li = document.createElement("li");
							li.innerHTML = "<p style='font-weight:600;font-size:16px;'>No Timestamps Found!</p>";
							ul.appendChild(li);
						}
					}});
					console.log("Successfully sent data to server");
				}
			});
		});
	});
});

$(document).ready(function(){
   $('body').on('click', 'a', function(){
     chrome.tabs.update({url: $(this).attr('href')});
     return false;
   });
});

function getVideoURL(callback){
	var queryInfo = {
		active: true,
		currentWindow: true
	};

	chrome.tabs.query(queryInfo, function(tabs){
		var tab = tabs[0]
		var vidurl = tab.url;
		//window.alert(vidurl);
		callback(vidurl);
	});
}

function timeToNum(text){
	hms = text.split(":");
	hours = parseInt(hms[0], 10)*3600;
	minutes = parseInt(hms[1], 10)*60;
	seconds = parseInt(hms[2]);
	total = hours+minutes+seconds;
	return total;
}

function numToTime(seconds){
	total_minutes = Math.floor(seconds/60);
	remaining_secs = seconds-(total_minutes*60);
	hours = Math.floor(total_minutes/60);
	remaining_minutes = total_minutes-(hours*60);
	timestamp = Math.floor(hours/10)+(hours-(10*Math.floor(hours/10)))+":"+Math.floor(remaining_minutes/10)+(remaining_minutes-(10*Math.floor(remaining_minutes/10)))+":"+Math.floor(remaining_secs/10)+(remaining_secs-(10*Math.floor(remaining_secs/10)));
	return timestamp;
}