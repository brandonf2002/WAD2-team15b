$(document).ready(function(){
  $(".button_dislike").click(function(e) {
    e.preventDefault();
    let _this_ = $(this);
    let _url_ = _this_.attr("post_url");
    let logged_in = _this_.attr("logged_in");
    let hasClicked = _this_.attr("clicked");
    let thisImg = _this_.find("img").first();

    let likeBtn = $(".button_like[post="+_this_.attr("post"));
    let hasClickedLike = likeBtn.attr("clicked");
    let likeImg = likeBtn.find("img").first();

    let countText = $(".like_count[post="+_this_.attr("post"));
    let textValue = parseInt(countText.html());
    $.ajax({
      url: _url_,
      method: "GET",
      data: {},
      success: function(data) {
        if (logged_in === "True") {
          if (hasClicked === "False") {
            countText.text(textValue - (hasClickedLike === "True" ? 2 : 1));
            _this_.attr("clicked", "True");
            likeBtn.attr("clicked", "False");
            thisImg.attr("src", "/static/images/forum/dislike.png");
            likeImg.attr("src", "/static/images/forum/like-grey.png");
          }
          else {
            countText.text(textValue + 1);
            thisImg.attr("src", "/static/images/forum/dislike-grey.png");
            _this_.attr("clicked", "False");
          }
        }
      },
      error: function(error) {
        console.log("error");
        console.log(error);
      }
    })
  })

  $(".button_like").click(function(e) {
    e.preventDefault();
    let _this_ = $(this);
    let _url_ = _this_.attr("post_url");
    let logged_in = _this_.attr("logged_in");
    let hasClicked = _this_.attr("clicked");
    let thisImg = _this_.find("img").first();

    let dislikeBtn = $(".button_dislike[post="+_this_.attr("post"));
    let hasClickedDisike = dislikeBtn.attr("clicked");
    let dislikeImg = dislikeBtn.find("img").first();

    let countText = $(".like_count[post="+_this_.attr("post"));
    let textValue = parseInt(countText.html());
    $.ajax({
      url: _url_,
      method: "GET",
      data: {},
      success: function(data) {
        if (logged_in === "True") {
          if (hasClicked === "False") {
            countText.text(textValue + (hasClickedDisike === "True" ? 2 : 1));
            _this_.attr("clicked", "True");
            dislikeBtn.attr("clicked", "False");
            thisImg.attr("src", "/static/images/forum/like.png");
            dislikeImg.attr("src", "/static/images/forum/dislike-grey.png");
          }
          else {
            countText.text(textValue - 1);
            thisImg.attr("src", "/static/images/forum/like-grey.png");
            _this_.attr("clicked", "False");
          }
        }
      },
      error: function(error) {
        console.log("error");
        console.log(error);
      }
    })
  })
})
