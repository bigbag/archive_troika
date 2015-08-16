(function($, window) {
    "use strict";

  var hideAlertBLock = function() {
    // Close alert block
    var $alert = $(".alert");
    var slideDuration = 500;
    var fadeDuration = 2000;

    $alert.fadeTo(fadeDuration, 500).slideUp(slideDuration, function(){
      $alert.alert('close');
    });
  };

  var toggleFilterBlock = function() {
    // Show and hide filter block
    var $showFilter = $('#show-filters');
    var $filterBlock = $('.filters-block');
    var toggleSpeed = 'fast';

    $showFilter.on( "click", function() {
      $filterBlock.slideToggle(toggleSpeed);
    });
  };

  $(document).ready(function() {
    hideAlertBLock();
    toggleFilterBlock();
  });
}).call(this, jQuery, window);
