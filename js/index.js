const serverAddress = "http://127.0.0.1:5000";

document.addEventListener('DOMContentLoaded', function(){
	console.log("Loaded");
	var searchField = document.getElementById("search-term");
	var submit = document.getElementById("submit");
	submit.addEventListener("click", function(){
		var searchTerm = searchField.value;
		getVideoURL(function(vidurl){
		//window.alert(serverAddress + '/download?vidurl='+vidurl);
			$.ajax({
				type: 'POST',
				url: serverAddress + '/download',
				data: {vidurl: vidurl, searchParams: searchTerm},
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
						if (timestamps.length>1){
							//window.alert(timestamps);
							for (var i = 1; i<timestamps.length; i++){
								var li = document.createElement("li");
								var a = document.createElement("a");
								var text = i + " : " + timestamps[i-1].slice(0, 8);
								seconds = timeToNum(text);
								//alert(vidurl.split("&t=").shift());
								a.setAttribute("href", vidurl.split("&t=").shift()+"&t="+seconds+"s");
								a.innerHTML = text;
								li.appendChild(a);
								ul.appendChild(li);
							}
						} else{
							var li = document.createElement("li");
							li.innerHTML = "No Timestamps Found!";
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
	hours = parseInt(hms[1], 10)*3600;
	minutes = parseInt(hms[2], 10)*60;
	seconds = parseInt(hms[3]);
	total = hours+minutes+seconds;
	return total;
}