(function($) 
//http://www.sitepoint.com/5-ways-declare-functions-jquery/ -> Using existing Jquery namespace to define new funstion
{
  // jQuery detects this state of readiness for you. Code included inside $( document ).
  //ready() will only run once the page Document Object Model (DOM) is ready for JavaScript code to execute.
  //Also Refer -> http://cssmenumaker.com/blog/flat-jquery-accordion-menu-tutorial
  $(document).ready( function() 
  {
    $('#cssmenu > ul > li > a').click ( function() 
      //The bulk of our code is wrapped in the .click() function. 
      //Any code inside this .click() function will run each time a link from the first level of our menu is clicked
      //every time a link is clicked we need to check whether it has a sub menu and then apply 
      //the appropriate functionality. We use the function .next() to grab the immediate sibling of the link when it is clicked. 
      //If the clicked link has a sub menu, then this value will be a Ul element (http://api.jquery.com/next/)
    {
      $('#cssmenu li').removeClass('active');
      $(this).closest('li').addClass('active'); 
      var checkElement = $(this).next();
      if((checkElement.is('ul')) && (checkElement.is(':visible')))
      //The next two lines of code after we grab our .next() element will add an .active class to the element that was clicked.
      //Condition 1 - first if statements checks to see if our checkElement is a UL and if it is visible. 
      //If so, it will remove the active class and then slide the sub menu up.
      {
        $(this).closest('li').removeClass('active');
        checkElement.slideUp('normal');
      }
      //condition 2 - second IF statement will expand a sub menu when its parent item is clicked. 
      //The IF statement checks to see if our checkElement is a UL element and if it is not visible. 
      //If these two conditions are true, then that means the menu item we clicked has a collapsed sub menu and that we need to expanded it.
      // We first collapse all the other sub menus that are visible with the .slideUp() function and then expand the current sub menu with the 
      //.slideDown() function.
      if((checkElement.is('ul')) && (!checkElement.is(':visible'))) 
      {
        $('#cssmenu ul ul:visible').slideUp('normal');
        checkElement.slideDown('normal');
        //(http://api.jquery.com/slideDown/)
      }
      if($(this).closest('li').find('ul').children().length == 0) 
      // Our final IF statement will determine whether to return TRUE or FALSE. 
      //Since we are clicking an link (A) element the browser naturally will want to follow the link inside the HREF to another page. 
      //When we return false we are telling the browser not to do this.
      {
        return true;
      } 
        else 
      {
        return false; 
      }   
    });
  });
})(jQuery);
