$(document).ready(function(){

    var sketch = new sketchjs.Sketch("http://localhost:8000", 'sketchdb');  
    
    //Helper function to log errors and results to our console div
    
    function logErrorsAndResults(response){
        var errors = response.errors;
        var results = response.results;
        if(results && results.length){
            $("#console-div").append("results:<br/>");
            var l = results.length;
            for(var i=0;i<l;i++){
                result = results[i];
                $("#console-div").append(JSON.stringify(result, null, 1) + "<br/>");
            }
        }
        
        $("#console-div").append("errors:" + errors + "<br/>");

    }
    
    

    $("#test-meta-server").click(function(){

        sketch.getServer(function(response){
        
            $("#console-div").append("getServer called<br/>");
            logErrorsAndResults(response);
        
        });
    
    });
    
    
    $("#test-meta-db").click(function(){

        sketch.getDb(function(response){
        
            $("#console-div").append("getDb called<br/>");
            logErrorsAndResults(response)
        
        });
    
    });
    
    $("#test-meta-parsers").click(function(){

        sketch.getParsers(function(response){
        
            $("#console-div").append("getParsers called<br/>");
            logErrorsAndResults(response);
        
        });
    
    });
    

    
    
    $("#test-query").click(function(){
    
        var collection = $("#query-collection").val()
        var command = $("#query-command").val()
        var query = $("#query-query").val();
        

        
        //todo: check args...
        var data = {query: query};
        
        console.log("query:", collection, command, data);

        sketch.query(collection, command, data, function(response){
            console.log("response", response);
            $("#console-div").append("query called<br/>");
            logErrorsAndResults(response)
        
        });
    
    });
    
    
    $("#test-objects").click(function(){
    
        var collection = $("#objects-collection").val()
        var query = $("#objects-query").val();
        

        
        //todo: check args...
        var data = {query: query};
        
        console.log("objects:", collection, data);

        sketch.objects(collection, data, function(response){
            console.log("response", response);
            $("#console-div").append("query called<br/>");
            logErrorsAndResults(response)
        
        });
    
    });

    
    
    
    $("#test-import").click(function(){
    
        var collection = $("#import-collection").val()
        var format = $("#import-format").val()
        var data = $("#import-data").val();
        var commit = $("#import-commit").attr('checked');
        commit = Boolean(commit);
        
        console.log("import:", collection, format, data, commit);
        
        //todo: check args...

        sketch.import(collection, format, data, commit, function(response){
            console.log("response", response);
            $("#console-div").append("import called<br/>");
            logErrorsAndResults(response)
        
        });

    
    });
    
});     
