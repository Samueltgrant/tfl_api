// $(document).ready(function () {
//   var add_input = $(".add-input");
//   var input_wrapper = $(".input-wrapper");
//   var new_input =
//     '<div><input type="text" id="station" class="new_row" name="field[]" value=""/><a href="javascript:void(0);" class="remove-input" title="Remove input"><svg xmlns="http://www.w3.org/2000/svg" class="icon-remove-input" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 000 2h6a1 1 0 100-2H7z" clip-rule="evenodd" /></svg></a></div>';

//   $(add_input).click(function () {
//     $(input_wrapper).append(new_input);
//   });
//   $(input_wrapper).on("click", ".remove-input", function (e) {
//     e.preventDefault();
//     $(this).parent("div").remove();
//   });
// });

const colours = [
  "mediumpurple",
  "cadetblue",
  "rosybrown",
  "mediumaquamarine",
  "cyan",
  'palevioletred',
  'crimson',
  'sienna',
  'darkslategrey'
];

add_more_fields.onclick = function () {
  var fieldNum = container_form.getElementsByClassName("entry-row").length + 1;
  // CONTAINER STUFF
  var entry_row_div = document.createElement("div");
  entry_row_div.setAttribute("class", "entry-row");

  var entry_row_details_div = document.createElement("div");
  entry_row_details_div.setAttribute("class", "entry-row-details");

  // COLOUR CIRCLE
  var colour_circle_span = document.createElement("span");
  colour_circle_span.setAttribute("class", "colour-circle");

  colour_circle_span.style.backgroundColor = colours[fieldNum];

  var entry_user_input_div = document.createElement("div");
  entry_user_input_div.setAttribute("class", "entry-input entry-user");

  var entry_station_input_div = document.createElement("div");
  entry_station_input_div.setAttribute("class", "entry-input entry-user");

  var autocomplete_div = document.createElement("div");
  autocomplete_div.setAttribute("class", "autocomplete");

  // USER
  var user_input_input = document.createElement("input");
  user_input_input.setAttribute("class", "login-input username-input");
  user_input_input.setAttribute("id", "user-" + fieldNum);
  user_input_input.setAttribute("name", "user_list");
  user_input_input.setAttribute("placeholder", "User " + fieldNum);
  user_input_input.setAttribute("type", "text");

  // STATION
  var station_input_input = document.createElement("input");

  station_input_input.setAttribute(
    "class",
    "login-input station-input new_role"
  );
  station_input_input.setAttribute("id", "station-" + fieldNum);
  station_input_input.setAttribute("name", "station_list");
  station_input_input.setAttribute("placeholder", "Station ");
  station_input_input.setAttribute("type", "text");

  // remove button
  //   var remove_button = document.createElement("a");
  //   remove_button.setAttribute("href", "javascript:void(0);");
  //   remove_button.setAttribute("class", "remove-input");
  //   remove_button.setAttribute("title", "remove-input");

  //   var remove_button_img = document.createElement("svg");
  //   remove_button_img.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  //   remove_button_img.setAttribute("class", "icon-remove-input");
  //   remove_button_img.setAttribute("viewBox", "0 0 20 20");
  //   remove_button_img.setAttribute("fill", "currentColor");

  //   var remove_button_path = document.createElement("path");
  //   remove_button_path.setAttribute("fill-rule", "evenodd");
  //   remove_button_path.setAttribute(
  //     "d",
  //     "M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z"
  //   );
  //   remove_button_path.setAttribute("clip-rule", "evenodd");

  //   remove_button_img.appendChild(remove_button_path);
  //   remove_button.appendChild(remove_button_img);

  // ADD TOGETHER
  autocomplete_div.appendChild(station_input_input);
  entry_user_input_div.appendChild(autocomplete_div);
  entry_station_input_div.appendChild(user_input_input);

  entry_row_details_div.appendChild(colour_circle_span);
  entry_row_details_div.appendChild(entry_station_input_div);
  entry_row_details_div.appendChild(entry_user_input_div);

  entry_row_div.appendChild(entry_row_details_div);
  //   entry_row_div.appendChild(remove_button);

  // newInput.setAttribute("rows", "3");
  container_form.appendChild(entry_row_div);

  autocomplete(document.getElementById("station-" + fieldNum), countries);
  fieldNum++;
};

remove_fields.onclick = function () {
  var input_tags = container_form.getElementsByClassName("entry-row");
  if (input_tags.length > 2) {
    container_form.removeChild(input_tags[input_tags.length - 1]);
  }
};
