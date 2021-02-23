$(function () {
    const text = $(".text");
    $(window).scroll(function () {
      const scroll = $(window).scrollTop();

      if (scroll >= 150) {
        text.removeClass("hidden");
      } else {
        text.addClass("hidden");
      }
    });
  });
