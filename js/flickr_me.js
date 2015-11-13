"use strict"
/*
*	This module is a wrapper for the Flickr API
* 	To see all API, visit https://www.flickr.com/services/api/
* 	Note: This module requires jquery
* 	Methods:
* 		search() - see function description for usage
*/
var FlickrMe = (function($){
	var apiKey = "37b008c37e61a536200947c81c78dc87";
	var method = "flickr.photos.search"; //static api key
	var returnFormat = "json";
	var sort = "relevance";
	var rootAPIUrl = "https://www.flickr.com/services/rest/?jsoncallback=?"; 


	function _createUrls(response,size) {
		var photo = response.photos.photo;
		// console.log(photo);
		var urls = new Array();

		$.each(photo, function( key,val ){
			console.log(_constructUrl(val,size));
		});
	}

	function _constructUrl(options,size) {
		var farmId = options.farm;
		var serverID = options.server;
		var id = options.id;
		var secret = options.secret;
		var size = (size == undefined) ? "" : '_'+size;

		var urlBase = 'https://farm' + farmId + '.staticflickr.com/' + serverID + '/' + id + '_' + secret + size + '.jpg';
		return { title: options.title, 
				 url: urlBase
		};
	}

	return {
		/*
		* Get the URL of images
		* @param searchKey - the search key
		* @param size key word
		    s	small square 75x75
			q	large square 150x150
			t	thumbnail, 100 on longest side
			m	small, 240 on longest side
			n	small, 320 on longest side
			-	medium, 500 on longest side
			z	medium 640, 640 on longest side
			c	medium 800, 800 on longest side†
			b	large, 1024 on longest side*
			h	large 1600, 1600 on longest side†
			k	large 2048, 2048 on longest side†
			
			Example: FlickrMe.search("hello world",'n');

		* @return {title:sometime,url:someurl}	
		*/
		search: function(searchKey,size) {
			
			$.ajax({
				url: rootAPIUrl,
				data: {
					text: searchKey,
					api_key: apiKey,
					format: returnFormat,
					sort: sort,
					method: method,
				},
				dataType: "jsonp",
				error: function(XMLHttpRequest, textStatus, errorThrown) { 
					console.log(textStatus);
					console.log(errorThrown);
			    }
			}).done(function(data) {
				if(data.stat == 'ok') {
					console.log(data);

					//create urls
					return _createUrls(data,size);
				} else {
					//broken
					console.log("error");
					console.log(data);
				}
			}); 
		}
	}


})(jQuery);

