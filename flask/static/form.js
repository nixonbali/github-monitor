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
				$('#PRCount').hide();
        $('#PRMergeRate').hide();
        $('#PRAdditions').hide();
        $('#PRDeletions').hide();
        $('#PRCommits').hide();
        $('#PRChangedFiles').hide();
        $('#PRMeanDays').hide();
        $('#PRMeanHours').hide();
        $('#PRMeanMinutes').hide();
      }
      // non-empty pull_requests + user-only input
      else {
				$('#NoPR').hide();
        $('#PRCount').text(data.num_pr).show();
        $('#PRMergeRate').text(data.merge_rate).show();
        $('#PRAdditions').text(data.additions).show();
        $('#PRDeletions').text(data.deletions).show();
        $('#PRCommits').text(data.commits).show();
        $('#PRChangedFiles').text(data.changed_files).show();
        $('#PRMeanDays').text(data.days).show();
        $('#PRMeanHours').text(data.hours).show();
        $('#PRMeanMinutes').text(data.minutes).show();
        d = document.getElementById('users')
        d.innerHTML = ""
        for (i = 0; i < data.users.length; i++) {
          newUser = document.createElement("tr")
          // console.log(data.users[i])

          newUser.innerHTML = data.users[i]['login'];
          d.appendChild(newUser);
        }
        r = document.getElementById('repos')
        r.innerHTML = ""
        for (i = 0; i < data.repos.length; i++) {
          newRepo = document.createElement("tr")
          // console.log(data.repos[i])

          newRepo.innerHTML = data.repos[i]['name'];
          r.appendChild(newRepo);
        }
      }
    });
    event.preventDefault();
  });
});
