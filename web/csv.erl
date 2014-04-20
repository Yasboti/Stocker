% function returning csv data for symbol

-module(csv).
-compile(export_all).

-import(eredis, [start_link/0, q/1]).

% return number of rows for given symbol
csvData(Symbol) ->
   {ok, C} = eredis:start_link(),
   {ok, Count} = eredis:q(C, ["ZCARD", Symbol]),
   Count.