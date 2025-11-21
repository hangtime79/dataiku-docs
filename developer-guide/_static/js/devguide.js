$(document).ready(function () {

    // Enlarge images that have the image-popup class
    $(document).on("click", ".image-popup", function () {
        // Get the source of the clicked image
        var imgSrc = $(this).attr("src");

        // Create the overlay element and append it to the body
        if ($(".popup-overlay").length === 0) {
            $("body").append("<div class='popup-overlay' style='background-image: url(\"" +
                imgSrc + "\")'></div>");
        }

        var overlay = $(".popup-overlay");

        // Check if the image is already enlarged
        if ($(this).hasClass("enlarged")) {
            // If enlarged, reduce it back to normal size
            $(this).removeClass("enlarged");
            overlay.remove(); // Remove overlay when closing the popup
        } else {
            // If not enlarged, show the enlarged version in the popup
            $(this).addClass("enlarged");
            overlay.show();
        }
    });

    // Close the popup and overlay when clicking on it or outside the image
    $(document).on("click", function (event) {
        var popup = $(".popup");
        if (!$(event.target).closest(".popup").length && !$(event.target).hasClass("image-popup")) {
            popup.hide();
            $(".popup-overlay").remove(); // Remove overlay when closing the popup
            $(".image-popup.enlarged").removeClass("enlarged");
        }
    });

    // Additional code to hide overlay when the popup is closed
    $(document).on("click", ".popup", function (event) {
        // Prevent the event from propagating to the document click handler
        event.stopPropagation();

        $(".popup").hide();
        $(".popup-overlay").remove(); // Remove overlay when closing the popup
        $(".image-popup.enlarged").removeClass("enlarged");
    });

    // Check summary tags used for dropdown effects and remove the div that adds extra space
    $("summary").each(function () {
        $(this).next(".line-block").find(".line").remove();
    });

    // // Get the current URL
    var currentUrl = window.location.href;
    if (currentUrl === 'https://developer.dataiku.com/latest/') {
        $('.breadcrumbs').hide();
    }

    // Rules only for the academy website
    if (window.location.href.includes("academy")) {
        // Modify behavior for external links in a frame
        $("a").each(function () {
            var link = $(this);
            var isExternal = link.attr("href") && !link.attr("href").startsWith(window.origin);

            if (isExternal) {
                link.attr("target", "_blank");
            }
        });

        // Hide elements with class .alert-uptodate and ul.breadcrumbs
        $(".alert-uptodate").hide();
        $(".breadcrumbs").css({display: 'none'});
    }

    // Rules when the document is in a frame or in the academy website
    // Some dev-guide content will soon be iframed in academy

    if (window.self !== window.top || window.location.href.includes("academy.dataiku")) {
        // If inside an iframe, force light mode by setting data-theme attribute to "light"
        const body = $('body');
        const currentTheme = body.attr('data-theme');

        if (currentTheme === 'dark' || currentTheme === 'auto') {
            body.attr('data-theme', 'light');
        }

        // Wrap images with a link using src as href in a frame
        $("img.image-popup").each(function () {
            var imgSrc = $(this).attr("src");
            $(this).wrap('<a href="' + imgSrc + '" target="_blank"></a>');
        });

        // Remove image-popup class from images in a frame
        $(".image-popup").removeClass("image-popup");

        // Check the class of the link and modify behavior accordingly

        $("a.reference").each(function () {
            var link = $(this);
            if (link.hasClass("internal")) {
                var href = link.attr("href");
                // Checks if the URL contains the specified hosts
                if (href.includes("academy-content.dataiku.com")) {
                    // Replaces the host with developer.dataiku.com
                    href = href.replace("academy-content.dataiku.com", "developer.dataiku.com/latest");
                    // Updates the href attribute of the link
                    link.attr("href", href);
                    // Opens the link in a new tab with the modified URL
                    link.attr("target", "_blank");
                }
            } else if (link.hasClass("external")) {
                // External links without opals open in a new tab
                link.attr("target", "_blank");
            }
        });


        // Attach click event handler to internal links
        $("a.reference.internal").click(function (event) {
            var href = $(this).attr("href");
            // Checks if the URL contains the specified hosts
            if (href.includes("academy-content.dataiku.com")) {
                event.preventDefault(); // Prevents default link behavior
                // Replaces the host with developer.dataiku.com
                href = href.replace("academy-content.dataiku.com", "developer.dataiku.com");
                // Opens link in new tab with modified URL
                window.open(href, "_blank");
            }
        });

    }
});