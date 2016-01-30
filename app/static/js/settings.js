var update = function() {
  $("#update-btn").text("updating...");
  $.get( "/api/v1.0/bin/update", function( data ) {
    console.log(data);
    alert( "Done." );
    $("#update-btn").text("Update");
  });
}
