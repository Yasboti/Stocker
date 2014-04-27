%
% given raw volume data, transcode to a colour range s.t:
%
%  median volume corresponds to 50% colour intensity
%  majority* of samples fall within [25% ~ 75%] intensity range
%  (majority: 90% of samples / 1 std.dev. from mean / decide)
%

-module(process).
-compile(export_all).

-import(eredis, [start_link/0, q/1]).
-import(csv, [dateToEpoch/1]).

% retrieve range of samples for symbol
retrieve_data(Symbol, Start, End) ->
   {ok, C} = eredis:start_link(),
   {ok, Data} = eredis:q(C, ["ZRANGEBYSCORE", Symbol, Start, End]),
   % parse a list of binary blobs into a list of tuples
   [list_to_tuple(string:tokens(binary_to_list(Row), ", ")) || Row <- Data].

% this can go away once data is stored properly
to_numbers(Tuples) ->
   lists:map(fun(T) -> {
      element(1,T),
      element(1, string:to_float(element(2,T))),
      element(1, string:to_float(element(3,T))),
      element(1, string:to_float(element(4,T))),
      element(1, string:to_float(element(5,T))),
      element(1, string:to_integer(element(6,T)))
   } end, Tuples).


% find median, min and max volume samples
% (slow, do parsing on data acquisition)
quantify(Tuples) ->
   Sorted = lists:keysort(6, to_numbers(Tuples)),
   Median = lists:nth(round(length(Sorted)/2), Sorted),
   Min = lists:nth(1, Sorted),
   Max = lists:last(Sorted),
   {
      element(6,Min),
      element(6,Median),
      element(6,Max)
   }.

% map colour gradient onto volume data
map_colour(Tuple, Moments) -> 
   % this is awkward
   V = element(6, Tuple),
   Min = element(1, Moments),
   Med = element(2, Moments),
   Max = element(3, Moments),
   % if volume below median, use lower range
   if V < Med ->
      setelement(6, Tuple, 
         trunc(128 * (V - Min) / (Med - Min)));
   % otherwise use upper range
   true ->
      setelement(6, Tuple, 
         trunc(128 * (V - Med) / (Max - Med) + 128))
   end.

map_tuples(Tuples, Moments) ->
   lists:map(fun(Tuple) ->
      map_colour(Tuple, Moments)
   end, to_numbers(Tuples)).


% output list of samples w/colour data added
output_data(Symbol, Start, End) ->
   StartEpoch = calendar:datetime_to_gregorian_seconds({Start, {0,0,0}}) - 62167219200,
   EndEpoch = calendar:datetime_to_gregorian_seconds({End, {0,0,0}}) - 62167219200,
   Data = retrieve_data(Symbol, StartEpoch, EndEpoch),
   Moments = quantify(Data),
   map_tuples(Data, Moments).
