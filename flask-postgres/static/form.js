$(document).ready(function() {
  $('form').on('submit', function(event) {
    $.ajax({
      data : {
        username : $('#usernameInput').val(),
        repo : $('#repoInput').val()
      },
      type : 'POST',
      url : '/process'
    })
    .done(function(data) {
      // check for empty pull_requests
      if (data.error) {
        $('#NoPR').text(data.error).show();
				$('#PR').hide();
      }
      // non-empty pull_requests
      else {
        $('#PR').text(data.num_pr).show();
				$('#NoPR').hide();
      }
    });
    event.preventDefault();
  });
});
