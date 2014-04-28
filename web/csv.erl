% function returning csv data for symbol

-module(csv).
-compile(export_all).

-import(eredis, [start_link/0, q/1]).

% convert date string to epoch
dateToEpoch(Date) ->
   calendar:datetime_to_gregorian_seconds({Date, {0,0,0}}) - 62167219200.

% return number of rows for given symbol
csvData(Symbol) ->
   {ok, C} = eredis:start_link(),
   {ok, Data} = eredis:q(C, ["ZRANGE", Symbol, 0, -1]),
   [lists:concat([binary_to_list(Row),"\n"]) || Row <- Data].

csvData(Symbol, Start, End) ->
   {ok, C} = eredis:start_link(),
   StartEpoch = dateToEpoch(Start),
   EndEpoch = dateToEpoch(End),
   {ok, Data} = eredis:q(C, ["ZRANGEBYSCORE", Symbol, StartEpoch, EndEpoch]),
   [lists:concat([binary_to_list(Row),"\n"]) || Row <- Data].

colourData(Symbol, Start, End) ->
   Data = process:output_data(Symbol, Start, End),
   [lists:concat([
      element(1,Row), ",",
      io_lib:format("~.2f",[element(2,Row)]), ",",
      io_lib:format("~.2f",[element(3,Row)]), ",",
      io_lib:format("~.2f",[element(4,Row)]), ",",
      io_lib:format("~.2f",[element(5,Row)]), ",",
      element(6,Row),
      "\n"]
   ) || Row <- Data].
