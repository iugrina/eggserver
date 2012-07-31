$(function() {
  $("#add-new-button").click(function() {
    $(".alert").hide();
    $("#add-new-form").toggle('slow');
    return false;
  });
  $("#add-new-cancel").click(function() {
    $("#add-new-form").hide('slow');
    return false;
  });
  $(".table tr").hover(
    function () {
      $(this).find(".btn-danger, .btn-inverse").toggle();
    },
    function () {
      $(this).find(".btn-danger, .btn-inverse").toggle();
    }
  );
  $(".btn-delete-badge").click(function() {
    bid = "bid-" + $(this).attr("id").slice(4);
    $("#delete-badge-modal .btn-delete-badge-confirm").attr("id", bid);
    $('#delete-badge-modal').modal('show');
    return false;
  });
  $(".btn-delete-badge-confirm").click(function() {
    bid = $(this).attr("id").slice(4);
    $.get('/badges/delete/' + bid, function(data) {
      window.location = "/";
    });
    $('#delete-badge-modal').modal('hide');
    return false;
  });
  $(".home-link").click(function() {
    $("#badges-list").show();
    $(".home-link").addClass("active");
    $("#badges-tree").hide();
    $(".tree-link").removeClass("active");
    $("#add-new-form").hide('slow');
    return false;
  });
  $(".tree-link").click(function() {
    $("#badges-list").hide();
    $(".home-link").removeClass("active");
    $("#badges-tree").show();
    $(".tree-link").addClass("active");
    $("#add-new-form").hide('slow');
    return false;
  });
});