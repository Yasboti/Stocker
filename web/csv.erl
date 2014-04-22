% function returning csv data for symbol

-module(csv).
-compile(export_all).

-import(eredis, [start_link/0, q/1]).

% return number of rows for given symbol
csvData(Symbol) ->
   {ok, C} = eredis:start_link(),
   {ok, Data} = eredis:q(C, ["ZRANGE", Symbol, 0, -1]),
   [lists:concat([binary_to_list(Row),"\n"]) || Row <- Data].