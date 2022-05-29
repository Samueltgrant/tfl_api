function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function (e) {
    var a,
      b,
      i,
      val = this.value;
    /*close any already open lists of autocompleted values*/
    closeAllLists();
    if (!val) {
      return false;
    }
    currentFocus = -1;
    /*create a DIV element that will contain the items (values):*/
    a = document.createElement("DIV");
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items");
    /*append the DIV element as a child of the autocomplete container:*/
    this.parentNode.appendChild(a);
    /*for each item in the array...*/
    for (i = 0; i < arr.length; i++) {
      /*check if the item starts with the same letters as the text field value:*/
      if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        /*create a DIV element for each matching element:*/
        b = document.createElement("DIV");
        /*make the matching letters bold:*/
        b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
        b.innerHTML += arr[i].substr(val.length);
        /*insert a input field that will hold the current array item's value:*/
        b.innerHTML += `<input type='hidden' value="${arr[i]}">`;
        /*execute a function when someone clicks on the item value (DIV element):*/
        b.addEventListener("click", function (e) {
          /*insert the value for the autocomplete text field:*/
          inp.value = this.getElementsByTagName("input")[0].value;
          /*close the list of autocompleted values,
        (or any other open lists of autocompleted values:*/
          closeAllLists();
        });
        a.appendChild(b);
      }
    }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function (e) {
    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      /*If the arrow DOWN key is pressed,
  increase the currentFocus variable:*/
      currentFocus++;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 38) {
      //up
      /*If the arrow UP key is pressed,
  decrease the currentFocus variable:*/
      currentFocus--;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 13) {
      /*If the ENTER key is pressed, prevent the form from being submitted,*/
      e.preventDefault();
      if (currentFocus > -1) {
        /*and simulate a click on the "active" item:*/
        if (x) x[currentFocus].click();
      }
    }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = x.length - 1;
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
    closeAllLists(e.target);
  });
}

/*An array containing all the country names in the world:*/
var countries = [
  "Baker Street Underground Station",
  "Charing Cross Underground Station",
  "Elephant & Castle Underground Station",
  "Embankment Underground Station",
  "Edgware Road (Bakerloo) Underground Station",
  "Harrow & Wealdstone Underground Station",
  "Harlesden Underground Station",
  "Kenton Underground Station",
  "Kilburn Park Underground Station",
  "Kensal Green Underground Station",
  "Lambeth North Underground Station",
  "Maida Vale Underground Station",
  "Marylebone Underground Station",
  "North Wembley Underground Station",
  "Oxford Circus Underground Station",
  "Paddington Underground Station",
  "Piccadilly Circus Underground Station",
  "Queen's Park Underground Station",
  "Regent's Park Underground Station",
  "Stonebridge Park Underground Station",
  "South Kenton Underground Station",
  "Willesden Junction Underground Station",
  "Warwick Avenue Underground Station",
  "Waterloo Underground Station",
  "Wembley Central Underground Station",
  "Barkingside Underground Station",
  "Buckhurst Hill Underground Station",
  "Bethnal Green Underground Station",
  "Bond Street Underground Station",
  "Bank Underground Station",
  "Chancery Lane Underground Station",
  "Chigwell Underground Station",
  "Debden Underground Station",
  "East Acton Underground Station",
  "Ealing Broadway Underground Station",
  "Epping Underground Station",
  "Fairlop Underground Station",
  "Greenford Underground Station",
  "Grange Hill Underground Station",
  "Gants Hill Underground Station",
  "Holborn Underground Station",
  "Hanger Lane Underground Station",
  "Hainault Underground Station",
  "Holland Park Underground Station",
  "Loughton Underground Station",
  "Lancaster Gate Underground Station",
  "Liverpool Street Underground Station",
  "Leyton Underground Station",
  "Leytonstone Underground Station",
  "Marble Arch Underground Station",
  "Mile End Underground Station",
  "North Acton Underground Station",
  "Newbury Park Underground Station",
  "Notting Hill Gate Underground Station",
  "Northolt Underground Station",
  "Perivale Underground Station",
  "Queensway Underground Station",
  "Redbridge Underground Station",
  "Ruislip Gardens Underground Station",
  "Roding Valley Underground Station",
  "Shepherd's Bush (Central) Underground Station",
  "Snaresbrook Underground Station",
  "St. Paul\'s Underground Station",
  "South Ruislip Underground Station",
  "Stratford Underground Station",
  "South Woodford Underground Station",
  "Tottenham Court Road Underground Station",
  "Theydon Bois Underground Station",
  "White City Underground Station",
  "Woodford Underground Station",
  "West Ruislip Underground Station",
  "Wanstead Underground Station",
  "West Acton Underground Station",
  "Aldgate (City of London)",
  "Barbican Underground Station",
  "Blackfriars Underground Station",
  "Bayswater Underground Station",
  "Cannon Street Underground Station",
  "Edgware Road (Circle Line) Underground Station",
  "Euston Square Underground Station",
  "Farringdon Underground Station",
  "Goldhawk Road Underground Station",
  "Great Portland Street Underground Station",
  "Gloucester Road Underground Station",
  "Hammersmith (H&C Line) Underground Station",
  "High Street Kensington Underground Station",
  "Kings Cross (London)",
  "Ladbroke Grove Underground Station",
  "Latimer Road Underground Station",
  "Moorgate Underground Station",
  "Monument Underground Station",
  "Mansion House Underground Station",
  "Paddington (H&C Line)-Underground",
  "Royal Oak Underground Station",
  "Shepherd's Bush Market Underground Station",
  "St. James's Park Underground Station",
  "South Kensington Underground Station",
  "Sloane Square Underground Station",
  "Temple Underground Station",
  "Tower Hill Underground Station",
  "Victoria Underground Station",
  "Wood Lane Underground Station",
  "Westminster Underground Station",
  "Westbourne Park Underground Station",
  "Acton Town Underground Station",
  "Aldgate East Underground Station",
  "Bromley-by-Bow Underground Station",
  "Becontree Underground Station",
  "Barking Underground Station",
  "Barons Court Underground Station",
  "Bow Road Underground Station",
  "Chiswick Park Underground Station",
  "Dagenham East Underground Station",
  "Dagenham Heathway Underground Station",
  "Ealing Common Underground Station",
  "Earl's Court Underground Station",
  "East Ham Underground Station",
  "Elm Park Underground Station",
  "East Putney Underground Station",
  "Fulham Broadway Underground Station",
  "Gunnersbury Underground Station",
  "Hornchurch Underground Station",
  "Hammersmith (Dist&Picc Line) Underground Station",
  "Kensington (Olympia) Underground Station",
  "Kew Gardens Underground Station",
  "Plaistow Underground Station",
  "Parsons Green Underground Station",
  "Putney Bridge Underground Station",
  "Richmond Underground Station",
  "Ravenscourt Park Underground Station",
  "Stamford Brook Underground Station",
  "Southfields Underground Station",
  "Stepney Green Underground Station",
  "Turnham Green Underground Station",
  "Upminster Bridge Underground Station",
  "Upton Park Underground Station",
  "Upminster Underground Station",
  "Upney Underground Station",
  "West Brompton Underground Station",
  "West Ham Underground Station",
  "Wimbledon Underground Station",
  "Wimbledon Park Underground Station",
  "West Kensington Underground Station",
  "Whitechapel Underground Station",
  "Bermondsey Underground Station",
  "Canning Town Underground Station",
  "Canons Park Underground Station",
  "Canada Water Underground Station",
  "Canary Wharf Underground Station",
  "Dollis Hill Underground Station",
  "Finchley Road Underground Station",
  "Green Park Underground Station",
  "Kilburn Underground Station",
  "Kingsbury Underground Station",
  "London Bridge Underground Station",
  "Neasden Underground Station",
  "North Greenwich Underground Station",
  "Queensbury Underground Station",
  "St. John's Wood Underground Station",
  "Stanmore Underground Station",
  "Swiss Cottage Underground Station",
  "Southwark Underground Station",
  "West Hampstead Underground Station",
  "Willesden Green Underground Station",
  "Wembley Park Underground Station",
  "Amersham Underground Station",
  "Chalfont & Latimer Underground Station",
  "Chesham Underground Station",
  "Croxley Underground Station",
  "Chorleywood Underground Station",
  "Eastcote Underground Station",
  "Hillingdon Underground Station",
  "Harrow-on-the-Hill Underground Station",
  "Ickenham Underground Station",
  "Moor Park Underground Station",
  "North Harrow Underground Station",
  "Northwick Park Underground Station",
  "Northwood Underground Station",
  "Northwood Hills Underground Station",
  "Pinner Underground Station",
  "Preston Road Underground Station",
  "Rickmansworth Underground Station",
  "Ruislip Manor Underground Station",
  "Ruislip Underground Station",
  "Rayners Lane Underground Station",
  "Uxbridge Underground Station",
  "Watford Underground Station",
  "West Harrow Underground Station",
  "Battersea Power Station Underground Station",
  "Archway Underground Station",
  "Angel Underground Station",
  "Balham Underground Station",
  "Borough Underground Station",
  "Burnt Oak Underground Station",
  "Brent Cross Underground Station",
  "Belsize Park Underground Station",
  "Chalk Farm Underground Station",
  "Colindale Underground Station",
  "Clapham Common Underground Station",
  "Clapham North Underground Station",
  "Clapham South Underground Station",
  "Colliers Wood Underground Station",
  "Camden Town Underground Station",
  "East Finchley Underground Station",
  "Edgware Underground Station",
  "Euston Underground Station",
  "Finchley Central Underground Station",
  "Goodge Street Underground Station",
  "Golders Green Underground Station",
  "High Barnet Underground Station",
  "Hendon Central Underground Station",
  "Highgate Underground Station",
  "Hampstead Underground Station",
  "Kennington Underground Station",
  "Kentish Town Underground Station",
  "Leicester Square Underground Station",
  "Morden Underground Station",
  "Mill Hill East Underground Station",
  "Mornington Crescent Underground Station",
  "Old Street Underground Station",
  "Oval Underground Station",
  "Stockwell Underground Station",
  "South Wimbledon Underground Station",
  "Totteridge & Whetstone Underground Station",
  "Tooting Bec Underground Station",
  "Tooting Broadway Underground Station",
  "Tufnell Park Underground Station",
  "West Finchley Underground Station",
  "Woodside Park Underground Station",
  "Warren Street Underground Station",
  "Nine Elms Underground Station",
  "Alperton Underground Station",
  "Arnos Grove Underground Station",
  "Arsenal Underground Station",
  "Bounds Green Underground Station",
  "Boston Manor Underground Station",
  "Caledonian Road Underground Station",
  "Covent Garden Underground Station",
  "Cockfosters Underground Station",
  "Finsbury Park Underground Station",
  "Hatton Cross Underground Station",
  "Hyde Park Corner Underground Station",
  "Heathrow Terminal 5 Underground Station",
  "Heathrow Terminals 2 & 3 Underground Station",
  "Hounslow Central Underground Station",
  "Hounslow East Underground Station",
  "Hounslow West Underground Station",
  "Holloway Road Underground Station",
  "Knightsbridge Underground Station",
  "Manor House Underground Station",
  "North Ealing Underground Station",
  "Northfields Underground Station",
  "Oakwood Underground Station",
  "Osterley Underground Station",
  "Park Royal Underground Station",
  "Russell Square Underground Station",
  "South Ealing Underground Station",
  "Southgate Underground Station",
  "South Harrow Underground Station",
  "Sudbury Hill Underground Station",
  "Sudbury Town Underground Station",
  "Turnpike Lane Underground Station",
  "Wood Green Underground Station",
  "Blackhorse Road Underground Station",
  "Brixton Underground Station",
  "Highbury & Islington Underground Station",
  "Pimlico Underground Station",
  "Seven Sisters Underground Station",
  "Tottenham Hale Underground Station",
  "Vauxhall Underground Station",
  "Walthamstow Central Underground Station",
];

/*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
autocomplete(document.getElementById("station-1"), countries);
autocomplete(document.getElementById("station-2"), countries);

// var elms = document.querySelectorAll("[id='station']");
// for (var i = 0; i < elms.length; i++) {
//   console.log(elms[i]);
//   autocomplete(elms[i], countries);
// }
