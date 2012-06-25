var sketchjs = sketchjs || {};


//TODO: use a more robust pattern for object creation
sketchjs.Sketch = function(url){

    this.url = url;
    return this;


};


/* query function */
sketchjs.Sketch.prototype.query = function(){
    console.log("query called");
}



