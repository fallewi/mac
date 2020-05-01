odoo.define('website_product_attribute_filter.attribute', function (require) {
    "use strict";
		$(document).on('change','.mt-checkbox input[name="attrib"]',function(event){
			// code here
			        console.log("vsdsd");
        if (!event.isDefaultPrevented()) {
                console.log("dsadad");
                event.preventDefault();
                $(this).closest("form").submit();
            }
		});
        
})
