(function($, window) {
    "use strict";

    
  $(document).ready(function() {
    $(".alert").fadeTo(2000, 500).slideUp(500, function(){
      $(".alert").alert('close');
    });
  });
}).call(this, jQuery, window);
