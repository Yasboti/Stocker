% function returning csv data for symbol

-module(csv).
-compile(export_all).

-import(eredis, [start_link/0, q/1]).

% convert date string to epoch
dateToEpoch(Date) ->
   calendar:datetime_to_gregorian_seconds({Date, {0,0,0}}) - 62167219200.
   
% return number of rows for given symbol
csvData(Symbol, Start, End) ->
   {ok, C} = eredis:start_link(),
   StartEpoch = dateToEpoch(Start),
   EndEpoch = dateToEpoch(End),
   {ok, Data} = eredis:q(C, ["ZRANGEBYSCORE", Symbol, StartEpoch, EndEpoch]),
   [lists:concat([binary_to_list(Row),"\n"]) || Row <- Data].