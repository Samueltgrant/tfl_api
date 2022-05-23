var survey_options = document.getElementById("survey_options");
// var add_more_fields = document.getElementById("add_more_fields");
var remove_fields = document.getElementById("remove_fields");

var container_form = document.getElementById("container_form");
var fieldset = document.getElementsByClassName("fieldset");

add_more_fields.onclick = function () {
  var myDiv = document.createElement("div");
  myDiv.className = "entry";

  var nameField = document.createElement("input");
  nameField.setAttribute("type", "text");
  nameField.setAttribute("name", "name_input");
  nameField.setAttribute("class", "entry-form entry-name");
  nameField.setAttribute("siz", 50);
  nameField.setAttribute("placeholder", "Name");

  var stationField = document.createElement("input");
  stationField.setAttribute("type", "text");
  stationField.setAttribute("name", "station_input");
  stationField.setAttribute("class", "entry-form entry-station");
  stationField.setAttribute("siz", 50);
  stationField.setAttribute("placeholder", "Station");

  myDiv.appendChild(nameField);
  myDiv.appendChild(stationField);
  survey_options.appendChild(myDiv);
};

remove_fields.onclick = function () {
  var input_tags = survey_options.getElementsByClassName("entry");
  console.log(input_tags);
  if (input_tags.length > 2) {
    survey_options.removeChild(input_tags[input_tags.length - 1]);
  }
};

const colours = [
  "mediumpurple",
  "cadetblue",
  "rosybrown",
  "mediumaquamarine",
  "cyan",
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

  // USER
  var login_input_input = document.createElement("input");
  login_input_input.setAttribute("class", "login-input username-input");
  login_input_input.setAttribute("id", "user-" + fieldNum);
  login_input_input.setAttribute("name", "user-" + fieldNum);
  login_input_input.setAttribute("placeholder", "User " + fieldNum);
  login_input_input.setAttribute("type", "text");

  var invalid_feedback_div = document.createElement("div");
  invalid_feedback_div.setAttribute("class", "invalid-feedback");

  // STATION
  var station_input_input = document.createElement("input");
  station_input_input.setAttribute("class", "login-input station-input");
  station_input_input.setAttribute("id", "station-" + fieldNum);
  station_input_input.setAttribute("name", "station-" + fieldNum);
  station_input_input.setAttribute("placeholder", "Station ");
  station_input_input.setAttribute("type", "text");

  // ADD TOGETHER
  entry_user_input_div.appendChild(station_input_input);
  entry_user_input_div.appendChild(invalid_feedback_div);

  entry_station_input_div.appendChild(login_input_input);
  entry_station_input_div.appendChild(invalid_feedback_div);

  entry_row_details_div.appendChild(colour_circle_span);
  entry_row_details_div.appendChild(entry_station_input_div);
  entry_row_details_div.appendChild(entry_user_input_div);

  entry_row_div.appendChild(entry_row_details_div);

  // newInput.setAttribute("rows", "3");
  container_form.appendChild(entry_row_div);
  fieldNum++;
};

remove_fields.onclick = function () {
  var input_tags = container_form.getElementsByClassName("entry-row");
  if (input_tags.length > 2) {
    container_form.removeChild(input_tags[input_tags.length - 1]);
  }
};
