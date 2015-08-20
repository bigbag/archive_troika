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
  
  var toggleStatusBlock = function() {
    // Show and hide status block
    var $showStatuses = $('#show-statuses');
    var $statusBlock = $('.statuses-block');
    var toggleSpeed = 'fast';

    $showStatuses.on( "click", function() {
      $statusBlock.slideToggle(toggleSpeed);
    });
  };
  
  var selectCard = function() {
    // Добавляет или удаляет карту из формы изменения статуса
    var $cardsCheckboxes = $("input.card-checkbox")
    var $selectedCards = $("#selected_cards");
    $cardsCheckboxes.prop( "checked", false );
    $selectedCards.val("{}");

    $cardsCheckboxes.on( "change", function() {
      var cards = jQuery.parseJSON($selectedCards.val());
      var card_id = this.getAttribute("card_id");
      var row = $(this).parents('tr');
      
      if (this.checked) {
        cards[card_id] = card_id;
        $selectedCards.val(JSON.stringify(cards));
        row.addClass("active");
      }
      else {
        delete(cards[card_id]);
        $selectedCards.val(JSON.stringify(cards));
        row.removeClass("active");
      }
    });
  }
  
  var setStatus = function() {
    //груповое редактирование статуса выбранных карт
    var $btnSubmit = $("#save_statuses");
    var $selectedCards = $("#selected_cards");
    var $setTroikaStatus = $("#set_troika_status");
    var $setStatus = $("#set_status");

    $btnSubmit.on( "click", function(event) {
      if (('-1' == $setStatus.val() && '-1' == $setTroikaStatus.val()) 
          || '{}' == $selectedCards.val()) {
        event.preventDefault();
      }
    });
  }
  
  
  $(document).ready(function() {
    hideAlertBLock();
    toggleFilterBlock();
    toggleStatusBlock();
    selectCard();
    setStatus();
  });
}).call(this, jQuery, window);
