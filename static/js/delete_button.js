$(document).ready(function(){
  $(".button_delete").click(function(e) {
    e.preventDefault();
    let _this_ = $(this);
    let _url_ = _this_.attr("post_url");

    if (confirm("Are you sure you want to delete this post")) {
      $.ajax({
        url: _url_,
        method: "GET",
        data: {},
        success: function(data) {
          location.reload(true);
        },
        error: function(error) {
          console.log("error");
          console.log(error);
        }
      })
    }
  })
})
