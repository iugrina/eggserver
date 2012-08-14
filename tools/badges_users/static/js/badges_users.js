$(function() {
  $(".add-new-button").click(function() {
    $(".alert").hide();
    $(".add-new-form").toggle('slow');
    return false;
  });
  
  $(".add-new-cancel").click(function() {
    $(".add-new-form").hide('slow');
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
      window.location = "/badges";
    });
    $('#delete-badge-modal').modal('hide');
    return false;
  });
  
  $(".btn-delete-user").click(function() {
    bid = "bid-" + $(this).attr("id").slice(4);
    $("#delete-user-modal .btn-delete-user-confirm").attr("id", bid);
    $('#delete-user-modal').modal('show');
    return false;
  });
  
  $(".btn-delete-user-confirm").click(function() {
    bid = $(this).attr("id").slice(4);
    $.get('/users/delete/' + bid, function(data) {
      window.location = "/users";
    });
    $('#delete-user-modal').modal('hide');
    return false;
  });
  
  $(".home-link").click(function() {
    $("#badges-list").show();
    $("#badges-tree").hide();
    $(".active").removeClass("active");
    $(this).addClass("active");
    $(".add-new-form").hide('slow');
  });
  
  $(".tree-link").click(function() {
    if ($(this).hasClass("active")) {
      $("#badges-list").show();
      $("#badges-tree").hide();
      $(this).removeClass("active");
      $(this).text(" Show Tree");
      $(".add-new-form").hide('slow');
    } else {
      $("#badges-list").hide();
      $(".home-link").removeClass("active");
      $("#badges-tree").show();
      $(this).addClass("active");
      $(this).text(" Hide Tree");
      $(".add-new-form").hide('slow');
    
      // Render tree
      $.get('tree/get', function(data) {
        renderTree(data);
      });
    }
    return false;
  });
});

function renderTree(data) {
  var iter = 0;
  var badges = $.parseJSON(data);
  var tbody = $("#badges-tree tbody");
  
  for (x in badges) {
    createRow(badges[x], tbody, iter);
  }
  
  renderBadgeDetails();
}

function createRow(badge, tbody, iter) {
  var padding = 'padding-left: 15px;';
  var childImg = '';
  if (badge.node.parent != 0) {
    padding = 'padding-left: ' + (10 + iter * 20) + 'px;';
    childImg = '<img src="static/img/tree.gif" class="hierarchy-tree-line">';
  }
  
  iter++;
  tbody.append('<tr><td style="' + padding + '" id="badge-row-' + badge.node.badge_id + '">' + childImg + badge.node.name + '</td></tr>');
  if (badge.children) {
    for (x in badge.children) {
      createRow(badge.children[x], tbody, iter);
    }
  }
}

function renderBadgeDetails() {
  $("#badges-tree td").hover(
    function () {
      $("#badge-details-container").remove();
      bid = $(this).attr("id").slice(10);
      $.get('/badges/get/' + bid, function(data) {
        var badge = $.parseJSON(data);
        var container = $("#badges-container");
        var badgeDetails = '';
        
        badgeDetails += '<div id="badge-details-container">';
        badgeDetails += '<h2>' + badge[0].name + '</h2>';
        badgeDetails += '<p><strong>id: </strong>' + badge[0].badge_id + '</p>';
        badgeDetails += '<p><strong>description: </strong>' + badge[0].description + '</p>';
        badgeDetails += '<p><strong>type: </strong>' + badge[0].type + '</p>';
        badgeDetails += '</div>';
        
        container.append(badgeDetails);
        $("#badge-details-container").css("top", $(window).scrollTop() + 200 + 'px');
      });
    },
    function () {
      $("#badge-details-container").remove();
    }
  );
}