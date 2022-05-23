# @timed
# def shortlisted_journeys(user_data:list, return_number: int, df) -> dict:
#     """Takes the input_stations and the shortest stations to get to from the get_total_times func and returns the
#     updated times, as well as the journey information from each input station."""
#     input_stations, users, colours = user_data
#     suggested_stations = get_total_times(df, input_stations, return_number)
#
#     journey_dict = {}
#     for index, suggested_station in enumerate(suggested_stations):
#         local_dict = {'suggested_station': suggested_station, 'routes': {}}
#         for route_index, input_station in enumerate(input_stations):
#             local_dict['routes'][f'route_{route_index + 1}'] = route_details(input_station, suggested_station,
#                                                                    user=users[route_index], colour=colours[route_index])
#
#         duration_list = [value['total_duration'] for key, value in local_dict['routes'].items() if key.startswith("route_")]
#         local_dict['avg_duration'] = int(sum(duration_list) / len(duration_list))
#
#         cost_list = [value['total_cost'] for key, value in local_dict['routes'].items() if key.startswith("route_")]
#         local_dict['avg_cost'] = sum(cost_list) / len(cost_list) / 100
#
#         local_dict['equality_duration'] = int(variance(duration_list))
#         local_dict['equality_cost'] = int(variance(cost_list))
#
#         journey_dict[f'option_{index + 1}'] = local_dict
#     return journey_dict