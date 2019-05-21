(function($){
"use strict"; // Start of use strict
//Popup Wishlist
function popup_wishlist(){
	$('.wishlist-link').on('click',function(event){
		event.preventDefault();
		$('.wishlist-mask').fadeIn();
		var counter = 10;
		var popup;
		popup = setInterval(function() {
			counter--;
			if(counter < 0) {
				clearInterval(popup);
				$('.wishlist-mask').hide();
			} else {
				$(".wishlist-countdown").text(counter.toString());
			}
		}, 1000);
	});
}
popup_wishlist();
//Menu Responsive
function rep_menu(){
	$('.toggle-mobile-menu').on('click',function(event){
		event.preventDefault();
		$(this).parents('.main-nav').toggleClass('active');
	});
	if($(window).width()<768){
		$('.main-nav li.menu-item-has-children>a').on('click',function(event){
			let link = document.getElementsByClassName('tag').getAttribute('href')  //edited
			window.open(link) //edited
			event.preventDefault();
			$(this).next().stop(true,false).slideToggle();
		});
	}
}
//Offset Menu
function offset_menu(){
	if($(window).width()>767){
		$('.main-nav .sub-menu').each(function(){
			var wdm = $(window).width();
			var wde = $(this).width();
			var offset = $(this).offset().left;
			var tw = offset+wde;
			if(tw>wdm){
				$(this).addClass('offset-right');
			}
		});
	}
}
//Fixed Header
function fixed_header(){
	if($('.header-ontop').length>0){
		if($(window).width()>767){
			var ht = $('#header').height();
			var st = $(window).scrollTop();
			if(st>ht){
				$('.header-ontop').addClass('fixed-ontop');
			}else{
				$('.header-ontop').removeClass('fixed-ontop');
			}
		}
	}
}
//Slider Background

function background(){

	$('.bg-slider .item-banner').each(function(){
		var src=$(this).find('.banner-thumb a img').attr('src');
		$(this).css('background-image','url("'+src+'")');
	});
}
function animated(){
	$('.banner-slider .owl-item').each(function(){
		var check = $(this).hasClass('active');
		if(check==true){
			$(this).find('.animated').each(function(){
				var anime = $(this).attr('data-animated');
				$(this).addClass(anime);
			});
		}else{
			$(this).find('.animated').each(function(){
				var anime = $(this).attr('data-animated');
				$(this).removeClass(anime);
			});
		}
	});
}
//Detail Gallery
function detail_gallery(){
	setTimeout(function() {
		if($('.detail-gallery').length>0){
				$('.detail-gallery').each(function(){
				$(this).find(".carousel").jCarouselLite({
					btnNext: $(this).find(".gallery-control .next"),
					btnPrev: $(this).find(".gallery-control .prev"),
					speed: 800,
					visible:3,
				});
				//Elevate Zoom
				$(this).find('.mid img').elevateZoom({
					zoomType: "inner",
					cursor: "crosshair",
					zoomWindowFadeIn: 500,
					zoomWindowFadeOut: 750
				});
				$(this).find(".carousel a").on('click',function(event) {
					event.preventDefault();
					$(this).parents('.detail-gallery').find(".carousel a").removeClass('active');
					$(this).addClass('active');
					$(this).parents('.detail-gallery').find(".mid img").attr("src", $(this).find('img').attr("src"));
					var z_url = $(this).parents('.detail-gallery').find('.mid img').attr('src');
					$('.zoomWindow').css('background-image','url("'+z_url+'")');
				});
			});
		}
	},1000);
}
//Document Ready
jQuery(document).ready(function(){
	//Switch Register

	// $('.login-to-register').on('click',function(event){
	// 	event.preventDefault();
	// 	$(this).toggleClass('login-status');
	// 	console.log($(this).hasClass('login-status'));
	// 	if($(this).hasClass('login-status')){
	// 		$(this).text($(this).attr('data-login'));
	// 		$(this).parents('.register-content-box').find('.block-login').hide();
	// 		$(this).parents('.register-content-box').find('.block-register').show();
	// 	}else{
	// 		$(this).text($(this).attr('data-register'));
	// 		$(this).parents('.register-content-box').find('.block-login').show();
	// 		$(this).parents('.register-content-box').find('.block-register').hide();
	// 	}
	// });

	//Drop Box Hover
	$('.dropdown-box').on('mouseover',function(){
		$('body').addClass('overlay');
		$(this).addClass('active');
	});
	$('.dropdown-box').on('mouseout',function(){
		$('body').removeClass('overlay');
		$(this).removeClass('active');
	});
	//Menu Responsive
	rep_menu();
	//Offset Menu
	offset_menu();
	//Animate
	if($('.wow').length>0){
		new WOW().init();
	}
	//Search Ajax
	$('.ajax-search input[type="text"]').on('blur',function(){
		$('.list-product-search').removeClass('active');
	});
	$('.ajax-search input[type="text"]').on('keydown',function(){
		if($(this).val()==""){
			$('.list-product-search').removeClass('active');
		}else{
			$('.list-product-search').addClass('active');
		}
	});
	//Coupon Index
	$('.list-coupon li').each(function(){
		var index = $(this).index()+1;
		$(this).prepend('<span class="coupon-index">'+index+'</span>');
	});
	//Control Category Banner
	if($('.cat-pro3').length>0){
		$('.cat-pro3').each(function(){
			$(this).find('.hide-cat-banner').on('click',function(event){
				event.preventDefault();
				$(this).parents('.cat-pro3').addClass('hidden-banner');
			});
			$(this).find('.show-cat-banner').on('click',function(event){
				event.preventDefault();
				$(this).parents('.cat-pro3').removeClass('hidden-banner');
			});
		});
	}
	//Detail Gallery
	detail_gallery();
	//Product Quick View
	$('.quickview-link').fancybox({
		afterShow: detail_gallery
	});
	//Product compare
	$('.compare-link').fancybox({
		width: 1170
	});
	//img Light Box
	$('.post-zoom-link').fancybox();
	//Add Cart Special
	$('.addcart-special,.btn-get-coupon').fancybox({
		'closeBtn' : false
	});
	//Get Coupon
	$('.btn-get-coupon').fancybox({
		'closeBtn' : false
	});
	$('.close-light-box').on('click',function(event){
		event.preventDefault();
		$.fancybox.close();
	})
	//Blog Masonry
	if($('.list-post-masonry').length>0){
		$('.list-post-masonry').masonry({
			// options
			itemSelector: '.item-post-masonry',
		});
	}
	//Back To Top
	$('.scroll-top').on('click',function(event){
		event.preventDefault();
		$('html, body').animate({scrollTop:0}, 'slow');
	});
	//Gallery Color
	$('.item-pro-color').each(function(){
		$(this).find('.list-color a').on('click',function(event){
			event.preventDefault();
			var data_color=$(this).attr('data-color');
			$(this).parents('.item-pro-color').find('.product-thumb-link img').each(function(){
				if($(this).attr('data-color')==data_color){
					$(this).addClass('active');
				}else{
					$(this).removeClass('active');
				}
			});
		});
	});
	//Widget Toggle
	$('.widget-title').on('click',function(){
		$(this).toggleClass('active');
		$(this).next().slideToggle();
	});
	//Tag Toggle
	if($('.toggle-tab').length>0){
		$('.toggle-tab').each(function(){
			$(this).find('.item-toggle-tab').first().find('.toggle-tab-content').show();
			$('.toggle-tab-title').on('click',function(){
				$(this).parent().siblings().removeClass('active');
				$(this).parent().toggleClass('active');
				$(this).parents('.toggle-tab').find('.toggle-tab-content').slideUp();
				$(this).next().stop(true,false).slideToggle();
			});
		});
	}
	//Widget Product Category
	$('.widget-product-cat li.has-sub-cat').first().find('ul').show();
	$('.widget-product-cat ul li.has-sub-cat>a').on('click',function(event){
		event.preventDefault();
		$(this).parent().toggleClass('active');
		$(this).next().slideToggle();
	});
	//Arrt Color
	$('.attr-detail.attr-color td a').on('click',function(event){
		event.preventDefault();
		$(this).toggleClass('active');
	});
	//Filter Price
	if($('.range-filter').length>0){
		$( ".range-filter #slider-range" ).slider({
			range: true,
			min: 0,
			max: 700,
			values: [ 50, 500 ],
			slide: function( event, ui ) {
				$( "#amount" ).html( "<span class='number'>" + ui.values[ 0 ] + "</span>" + "<span class='separate'> - </span>" + "<span class='number'>" + ui.values[ 1 ] + "</span>" );
			}
		});
		$( ".range-filter #amount" ).html( "<span class='number'>" + $( "#slider-range" ).slider( "values", 0 )+ "</span>" + " <span class='separate'> - </span> " + "<span class='number'>" + $( "#slider-range" ).slider( "values", 1 ) + "</span>" );
	}
	//Filter color/Size
	$('.list-filter').each(function(){
		$(this).find('a').on('click',function(event){
			event.preventDefault();
			$(this).parent().siblings().removeClass('active');
			$(this).parent().toggleClass('active');
			$(this).parents('.attr-detail').find('.current-size').text($(this).text());
			$(this).parents('.attr-detail').find('.current-color').text($(this).attr('data-color'));
		});
	});

	//Deal Count Down
	if($('.detail-countdown').length>0){
		$(".detail-countdown").TimeCircles({
			fg_width: 0.01,
			bg_width: 1.2,
			text_size: 0.07,
			circle_bg_color: "#ffffff",
			time: {
				Days: {
					show: true,
					text: "",
					color: "#f9bc02"
				},
				Hours: {
					show: true,
					text: "",
					color: "#f9bc02"
				},
				Minutes: {
					show: true,
					text: "",
					color: "#f9bc02"
				},
				Seconds: {
					show: true,
					text: "",
					color: "#f9bc02"
				}
			}
		});
	}
	if($('.deals-cowndown').length>0){
		$(".deals-cowndown").TimeCircles({
			fg_width: 0.01,
			bg_width: 1.2,
			text_size: 0.07,
			circle_bg_color: "#ffffff",
			time: {
				Days: {
					show: true,
					text: "روز",
					color: "#f9bc02"
				},
				Hours: {
					show: true,
					text: "ساعت",
					color: "#f9bc02"
				},
				Minutes: {
					show: true,
					text: "دقیقه",
					color: "#f9bc02"
				},
				Seconds: {
					show: true,
					text: "ثانیه",
					color: "#f9bc02"
				}
			}
		});
	}
	//Flash Count Down
	// if($('.flash-countdown').length>0){
	// 	$(".flash-countdown").TimeCircles({
	// 		count_past_zero: false,
  //     direction:"both",
	// 		fg_width: 0.01,
	// 		bg_width: 1.2,
	// 		text_size: 0.07,
	// 		circle_bg_color: "#ffffff",
	// 		time: {
	// 			Days: {
	// 				show: false,
	// 				text: "روز",
	// 				color: "#f9bc02"
	// 			},
	// 			Hours: {
	// 				show: true,
	// 				text: "ساعت",
	// 				color: "#f9bc02"
	// 			},
	// 			Minutes: {
	// 				show: true,
	// 				text: "دقیقه",
	// 				color: "#f9bc02"
	// 			},
	// 			Seconds: {
	// 				show: true,
	// 				text: "ثانیه",
	// 				color: "#f9bc02"
	// 			}
	// 		}
	// 	});
	// }

	if($('.countdown-master').length>0){
		$('.countdown-master').each(function(){
			$(this).FlipClock(65100,{
				clockFace: 'HourlyCounter',
				countdown: true,
				autoStart: true,
			});
		});
	}
});
//Window Load

jQuery(window).on('load',function(){
	//Custom ScrollBar
	if($('.custom-scroll').length>0){
		$('.custom-scroll').each(function(){
			$(this).mCustomScrollbar({
				scrollButtons:{
					enable:true
				}
			});
		});
	}
	//Owl Carousel


		if($('.wrap-item').length>0){

				$('.wrap-item').each(function() {
					setTimeout(function() {
						var data = $(this).data();
						$(this).owlCarousel({

								addClassActive:true,
								stopOnHover:true,
								itemsCustom:data.itemscustom,
								autoPlay:data.autoplay,
								transitionStyle:data.transition,
								beforeInit:background,
								afterAction:animated,
								navigationText:['<i class="fa fa-angle-left" aria-hidden="true"></i>','<i class="fa fa-angle-right" aria-hidden="true"></i>'],


						});
						$(this).find('.owl-controls').css('left',data.control+'px');
					},Math.floor(Math.random() * 1000) + 500 );
				});
		}




	//BxSlider
	if($('.bxslider-banner').length>0){
		$('.bxslider-banner').each(function(){
			$(this).find('.bxslider').bxSlider({
				controls:false,
				pagerCustom: $(this).find('.bx-pager')
			});
		});
	}
	//Detail Gallery Widthout sidebar
	if($('.gallery-without-sidebar').length>0){
		$('.gallery-without-sidebar').each(function(){
			if($(window).width()>1200){
				$(this).find('.carousel').flexslider({
					animation: "slide",
					controlNav: false,
					animationLoop: false,
					slideshow: false,
					itemWidth: 80,
					minItems: 6,
					maxItems: 6,
					move: 1,
					direction: "vertical",
					directionNav: false,
					asNavFor: $(this).find('.slider')
				});
				$(this).find('.slider').flexslider({
					animation: "slide",
					controlNav: false,
					animationLoop: false,
					slideshow: false,
					prevText: '<i class="fa fa-angle-left"></i>',
					nextText: '<i class="fa fa-angle-right"></i>',
					sync: $(this).find('.carousel')
				});
			}else{
				$(this).find('.carousel').flexslider({
					animation: "slide",
					controlNav: false,
					animationLoop: false,
					slideshow: false,
					itemWidth: 80,
					minItems: 3,
					maxItems: 6,
					move: 1,
					direction: "horizontal",
					directionNav: false,
					asNavFor: $(this).find('.slider')
				});
				$(this).find('.slider').flexslider({
					animation: "slide",
					controlNav: false,
					animationLoop: false,
					slideshow: false,
					prevText: '<i class="fa fa-angle-left"></i>',
					nextText: '<i class="fa fa-angle-right"></i>',
					sync: $(this).find('.carousel')
				});
			}
		});
	}
});
//Window Resize
jQuery(window).resize(function(){
	offset_menu();
});
//Window Scroll
jQuery(window).scroll(function(){
	//Scroll Top
	if($(this).scrollTop()>$(this).height()){
		$('.scroll-top').addClass('active');
	}else{
		$('.scroll-top').removeClass('active');
	}
	//Fixed Header
	fixed_header();
});
})(jQuery); // End of use strict

// FAQ
$(".open").click(function() {
	var container = $(this).parents(".topic");
	var answer = container.find(".answer");
	var trigger = container.find(".faq-t");

	answer.slideToggle(200);

	if (trigger.hasClass("faq-o")) {
	  trigger.removeClass("faq-o");
	} else {
	  trigger.addClass("faq-o");
	}

	if (container.hasClass("expanded")) {
	  container.removeClass("expanded");
	} else {
	  container.addClass("expanded");
	}
  });

  jQuery(document).ready(function($) {
	$('.question').each(function() {
	  $(this).attr('data-search-term', $(this).text().toLowerCase() + $(this).find("ptag").text().toLowerCase());

	});

	$('.live-search-box').on('keyup', function() {

	  var searchTerm = $(this).val().toLowerCase();

	  $('.question').each(function() {

		if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
		  $(this).parent().parent().show();
		} else {
		  $(this).parent().parent().hide();
		}

	  });

	});

  });


// avatar
$('.avatarUser img').click( function(){
	  alert('clicked')
    if ( $(this).hasClass('current') ) {
    } else {
        $('img.current').removeClass('current');
        $(this).addClass('current');
    }
});

// file upload
var inputs = document.querySelectorAll( '.inputfile' );
Array.prototype.forEach.call( inputs, function( input )
{
	var label	 = input.nextElementSibling,
		labelVal = label.innerHTML;

	input.addEventListener( 'change', function( e )
	{
		var fileName = '';
		if( this.files && this.files.length > 1 )
			fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
		else
			fileName = e.target.value.split( '\\' ).pop();

		if( fileName )
			label.querySelector( 'span' ).innerHTML = fileName;
		else
			label.innerHTML = labelVal;
	});
});
//test
// table

// $(function(){
// $(".fold-table tr.view").on("click", function(){
// 	if($(this).hasClass("open")) {
// 	$(this).removeClass("open").next(".fold").removeClass("open");
// 	} else {
// 	$(".fold-table tr.view").removeClass("open").next(".fold").removeClass("open");
// 	$(this).addClass("open").next(".fold").addClass("open");
// 	}
// });
// });

// login
// $('.message a').click(function(){
// 	$('.clickopen').animate({height: "toggle", opacity: "toggle"}, "slow");
//  });
//
//  $('.clickactions').click(function(){
// 	$('.clickopen2').animate({height: "toggle", opacity: "toggle"}, "slow");
//  });
