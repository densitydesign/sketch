var sketchjs = sketchjs || {};


//TODO: use a more robust pattern for object creation
sketchjs.Sketch = function(url, database){
    var self = this;
    this.url = url;
    if(database){
        this.database = database;
    } else {
        this.database = 'sketchdb';
    }

    self.setDb = function(dbName){
        self.database = dbName;
    }

    return this;

};


/* login function */
sketchjs.Sketch.prototype.login = function(username, pwd, successCallback){

    var loginUrl = this.url + "/sketch/ajaxlogin/";
    var data = {username : username, password : pwd };

    $.ajax({
        type: 'POST',
        url: loginUrl,
        data: data,
        success: successCallback,
        dataType: 'json'
    });   
};





sketchjs.Sketch.prototype.getServerInfo = function(successCallback){

    var url = this.url + "/sketch/server/";
    
    $.ajax({
        type: 'GET',
        url: url,
        success: successCallback,
        dataType: 'json'
    });   
    
};


sketchjs.Sketch.prototype.getDbInfo = function(options, successCallback){

    var db = options.database || this.database;

    var url = this.url + "/sketch/db/" + db + "/";
    
    $.ajax({
        type: 'GET',
        url: url,
        success: successCallback,
        dataType: 'json'
    });   
    
};


sketchjs.Sketch.prototype.getParsersInfo = function(successCallback){

    var url = this.url + "/sketch/parsers/";
    
    $.ajax({
        type: 'GET',
        url: url,
        success: successCallback,
        dataType: 'json'
    });   
    
};


sketchjs.Sketch.prototype.getFormattersInfo = function(successCallback){

    var url = this.url + "/sketch/formatters/";
    
    $.ajax({
        type: 'GET',
        url: url,
        success: successCallback,
        dataType: 'json'
    });   
    
};

sketchjs.Sketch.prototype.getMappersInfo = function(successCallback){

    var url = this.url + "/sketch/mappers/";
    
    $.ajax({
        type: 'GET',
        url: url,
        success: successCallback,
        dataType: 'json'
    });   
    
};


sketchjs.Sketch.prototype.getProcessorsInfo = function(successCallback){

    var url = this.url + "/sketch/processors/";
    
    $.ajax({
        type: 'GET',
        url: url,
        success: successCallback,
        dataType: 'json'
    });   
    
};



/* query function */
sketchjs.Sketch.prototype.query = function(collection, command, data, successCallback){

    var url = this.url + "/sketch/query/" + this.database + "/" + collection + "/" + command + "/";
    console.log("query", url);
    
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: successCallback,
        dataType: 'json'
    });
    
    
};


/* objects function */
sketchjs.Sketch.prototype.objects = function(options, collection, data, successCallback){

    var db = options.database || this.database;

    var url = this.url + "/sketch/objects/" + db + "/" + collection + "/";
    console.log("objects", url);
    //#TODO: this should be a GET
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: successCallback,
        dataType: 'json'
    });
    
    
};




/* import function */
//TODO: add mapping
sketchjs.Sketch.prototype.import = function(options, collection, parser, data, commit, successCallback){

    var db = options.database || this.database;

    var url = this.url + "/sketch/import/" + db + "/" + collection + "/";
    var commitInteger = 0;
    if(Boolean(commit)){
        commitInteger = 1;
    } 
    postData = {data : data, parser : parser, commit : commitInteger };
    
    $.ajax({
        type: 'POST',
        url: url,
        data: postData,
        success: successCallback,
        dataType: 'json'
    });
    
    
};




/*
  from: https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
  basically it adds the crsf token to every post request.
  notes:
  * requires jquery
  * works only from the browser
*/

jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
