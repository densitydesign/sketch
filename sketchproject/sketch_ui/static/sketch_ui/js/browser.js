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
    
    
    
    
    
    
    
    
    var InterfaceModel = function(){
        var self = this;
        self.serverPanel = new ServerPanelModel();
        self.queryPanel = new QueryPanelModel(self.serverPanel.databases);
        
        self.currentPanel = ko.observable('serverPanel');
        
        self.toServerPanel = function(){
            self.currentPanel('serverPanel');
        };
        self.toQueryPanel = function(){
            self.currentPanel('queryPanel');
        };
        self.toImportPanel = function(){
            self.currentPanel('importPanel');
        };
        
        self.refreshServer = function(){
            self.serverPanel.refresh();
        };
        
    }
    
    
    
    var DbModel=function(name){
        var self = this;
        self.name = name;
        self.collections = ko.observable([]);
        
        self.refresh = function(){
            sketch.getDbInfo({ database: self.name}, function(response){
                self.collections(response.results);
            
            });
            
        }
        
        
        self.refresh();
        
    }
    
    
    var ServerPanelModel = function(){

        var self = this;
        self.databases = ko.observableArray([]);
        self.mappers = ko.observableArray([]);
        self.parsers = ko.observableArray([]);
        self.formatters = ko.observableArray([]);
        self.processors = ko.observableArray([]);
        
        self.errors = ko.observableArray();
        self.currentDatabase = ko.observable(null);

        self.refresh = function(){
        
            sketch.getServerInfo(function(response){
        
                self.databases([]);
                for(var i=0,n=response.results.length;i<n;i++){
                    self.databases.push(new DbModel(response.results[i]));
                }
                
                self.errors(response.errors);
            });        
            
            sketch.getMappersInfo(function(response){
            
                self.mappers(response.results);
        
            });
            
            sketch.getParsersInfo(function(response){
        
                self.parsers(response.results);      
        
            });
            
            sketch.getFormattersInfo(function(response){
        
                self.formatters(response.results);      
        
            });
            
            sketch.getProcessorsInfo(function(response){
        
                self.processors(response.results);      
        
            });
            
        }
        
        self.refresh();
        
    }
     
    
    
    var QueryPanelModel = function(databases){

        var self = this;
        self.databases = databases;
        
        self.collectionOptions =  ko.observableArray([]);
        self.currentCollection = ko.observable(null);
        self.currentDatabase = ko.observable(self.databases()[0]);
                
        self.query = ko.observable('');
        self.results = ko.observableArray([]);
        self.errors = ko.observableArray();

        self.currentDatabase.subscribe(function(newValue){
            self.collectionOptions(newValue.collections());   
            if(!self.currentCollection()){
                self.currentCollection(newValue.collections[0]);
            }        
        });
        

        self.refresh = function(){
        
            var dbName= self.currentDatabase().name;
            var collectionName= self.currentCollection();
            var query = self.query();
            
            sketch.objects({ database: dbName}, collectionName, { query: query }, function(response){
                
                self.results(response.results);
        
            });
            
        }
        
    }
     
     
    //activating knockout
    ko.applyBindings(new InterfaceModel());
    
    
    
});     
